import ctypes
import subprocess
import time
import sys

from config import exe_path

# Access rights constants
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_READ = 0x0010
THREAD_GET_CONTEXT = 0x0008
THREAD_SUSPEND_RESUME = 0x0002

# Context flags
CONTEXT_FULL = 0x00010007

# Snapshot constants for threads
TH32CS_SNAPTHREAD = 0x00000004

# Structure for the CONTEXT, containing registers and flags
class CONTEXT(ctypes.Structure):
    _fields_ = [
        ("ContextFlags", ctypes.c_ulong),
        ("Dr0", ctypes.c_ulong),
        ("Dr1", ctypes.c_ulong),
        ("Dr2", ctypes.c_ulong),
        ("Dr3", ctypes.c_ulong),
        ("Dr6", ctypes.c_ulong),
        ("Dr7", ctypes.c_ulong),
        ("FloatSave", ctypes.c_ulong * 32),  # Simplified for the example
        ("SegGs", ctypes.c_ulong),
        ("SegFs", ctypes.c_ulong),
        ("SegEs", ctypes.c_ulong),
        ("SegDs", ctypes.c_ulong),
        ("Edi", ctypes.c_ulong),
        ("Esi", ctypes.c_ulong),
        ("Ebx", ctypes.c_ulong),
        ("Edx", ctypes.c_ulong),
        ("Ecx", ctypes.c_ulong),
        ("Eax", ctypes.c_ulong),
        ("Ebp", ctypes.c_ulong),
        ("Eip", ctypes.c_ulong),
        ("SegCs", ctypes.c_ulong),
        ("EFlags", ctypes.c_ulong),
        ("Esp", ctypes.c_ulong),
        ("SegSs", ctypes.c_ulong),
        ("ExtendedRegisters", ctypes.c_ulong * 512),  # Simplified for the example
    ]

kernel32 = ctypes.windll.kernel32
psapi = ctypes.windll.psapi
kernel32.OpenProcess.restype = ctypes.c_void_p
kernel32.OpenThread.restype = ctypes.c_void_p
kernel32.SuspendThread.restype = ctypes.c_ulong
kernel32.ResumeThread.restype = ctypes.c_long
kernel32.GetThreadContext.restype = ctypes.c_long
kernel32.CloseHandle.restype = ctypes.c_long

class THREADENTRY32(ctypes.Structure):
    _fields_ = [
        ("dwSize", ctypes.c_ulong),
        ("cntUsage", ctypes.c_ulong),
        ("th32ThreadID", ctypes.c_ulong),
        ("th32OwnerProcessID", ctypes.c_ulong),
        ("tpBasePri", ctypes.c_long),
        ("tpDeltaPri", ctypes.c_long),
        ("dwFlags", ctypes.c_ulong),
    ]

def get_thread_ids(pid):
    snapshot = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, 0)
    if snapshot == -1:
        print("Failed to create thread snapshot.")
        sys.exit(1)

    thread_entry = THREADENTRY32()
    thread_entry.dwSize = ctypes.sizeof(THREADENTRY32)

    threads = []

    if kernel32.Thread32First(snapshot, ctypes.byref(thread_entry)):
        while True:
            if thread_entry.th32OwnerProcessID == pid:
                threads.append(thread_entry.th32ThreadID)
            if not kernel32.Thread32Next(snapshot, ctypes.byref(thread_entry)):
                break

    kernel32.CloseHandle(snapshot)
    return threads

if __name__ == "__main__":
    proc = subprocess.Popen([exe_path])
    time.sleep(1)  

    pid = 10580
    print("Process PID:", pid)

    thread_ids = get_thread_ids(pid)
    if not thread_ids:
        print("No threads found for the process.")
        sys.exit(1)

    thread_id = thread_ids[0]
    print("Using Thread ID:", thread_id)

    h_thread = kernel32.OpenThread(THREAD_GET_CONTEXT | THREAD_SUSPEND_RESUME, False, thread_id)
    if not h_thread:
        print("Failed to open thread. Error code:", kernel32.GetLastError())
        sys.exit(1)

    suspend_count = kernel32.SuspendThread(h_thread)
    if suspend_count == -1:
        print("Failed to suspend the thread.")
        kernel32.CloseHandle(h_thread)
        sys.exit(1)

    context = CONTEXT()
    context.ContextFlags = CONTEXT_FULL

    if not kernel32.GetThreadContext(h_thread, ctypes.byref(context)):
        print("Failed to get thread context. Error code:", kernel32.GetLastError())
        kernel32.ResumeThread(h_thread)
        kernel32.CloseHandle(h_thread)
        sys.exit(1)

    print("EIP: 0x{0:08X}".format(context.Eip))
    print("EAX: 0x{0:08X}".format(context.Eax))
    print("EBX: 0x{0:08X}".format(context.Ebx))
    print("ECX: 0x{0:08X}".format(context.Ecx))
    print("EDX: 0x{0:08X}".format(context.Edx))
    print("ESI: 0x{0:08X}".format(context.Esi))
    print("EDI: 0x{0:08X}".format(context.Edi))
    print("ESP: 0x{0:08X}".format(context.Esp))
    print("EBP: 0x{0:08X}".format(context.Ebp))
    print("EFlags: 0x{0:08X}".format(context.EFlags))

    if kernel32.ResumeThread(h_thread) == -1:
        print("Failed to resume the thread.")

    kernel32.CloseHandle(h_thread)
