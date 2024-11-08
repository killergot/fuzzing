import random
import subprocess
import myDebugger
from research import save_config,mark_res,run_dercov,analize_coverage


class FileFuzzer:
    def __init__(self, exe_path, conf_file_path,mut_folder_path,col_bb):
        self.conf_file_path = conf_file_path
        self.mut_folder_path = mut_folder_path
        self.exe_path = exe_path
        self.offset = 1
        self.iteration = 1
        self.running = False
        self.col_bb = col_bb

        self.test_cases = ["\x00", "\x80", "\x7f", "\xff",
                           "\x7f\xff", "\x80\x00", "\x7f\xfe", "\xff\xff",
                           "\x7f\xff\xff", "\x80\x00\x00", "\x7f\xff\xfe", "\xff\xff\xff",
                           "\x7f\xff\xff\xff", "\x80\x00\x00\x00", "\x7f\xff\xff\xfe", "\xff\xff\xff\xff",
                           "%s%n%s%n%s%n", "\x3B", "\n", "\x2F"]

        #                          ';'      ' '     '.'      ','
        self.dividing_fields = [b'\x3B', b'\x20', b'\x2E', b'\x2C',
                                b'\x21', b'\x3F', b'\x3A', b'\x2F']
        #                          '!'     '?'      ':'       '/'

        with open(conf_file_path, 'rb') as fd:
            self.stream = fd.read()
            fd.close()

    def auto_fuzzing(self):
        error = False
        interactive_swith = int(raw_input('If u want use interactive debugger press 1. (Not press 0)'))
        what_we_do = int(raw_input('If u want push byte press 1. If u want use random mutation press 0'))
        bb_current = self.col_bb
        while not error:
            counter = 0
            for _ in self.test_cases:
                if what_we_do == 0:
                    self.change_bytes(self.offset, self.offset, counter, 1)
                else:
                    self.add_bytes_in_end(100)
                print("File mutation #", self.iteration)
                print("Current offset: ", self.offset)
                print("Test case`s index: ", counter)

                # New debugging thread
                status,bb = self.test_prog()
                
                if status != 0:
                    mark_res(self.conf_file_path,self.mut_folder_path,self.iteration,self.exe_path)
                    myDebugger.simple_debugger([self.exe_path],interactive_swith)
                    error = True
                    break
                
                if bb > bb_current:
                    fd = open(self.conf_file_path, "wb")
                    fd.write(self.stream)
                    fd.close()

                self.iteration += 1
                counter += 1

            self.offset += 100

    def test_prog(self):
        print("Launch program...")
        proc = subprocess.Popen([self.exe_path],stdout=None)
        status = subprocess.Popen.wait(proc)
        bb = run_dercov("B:\\mbks\\python_2_lab\\exe\\mutations",self.exe_path)

        print("Program finished with status "), status
        return [status, bb]

    def mutate_file(self, rand_range=1000):

        fd = open(self.conf_file_path, "rb")
        stream = fd.read()
        fd.close()

        rand_index = random.randint(0, len(self.test_cases) - 1)
        test_case = self.test_cases[rand_index]
        rand_len = random.randint(1, rand_range)

        # Now take the test case and repeat it
        test_case = test_case * rand_len

        print("File mutation #", self.iteration)
        print("Current offset: ", self.offset)
        print("Test case`s index: ", rand_index) 
        print("Test length: ", len(test_case)) 

        fuzz_file = stream[0:self.offset]
        fuzz_file += bytes(test_case)
        fuzz_file += stream[self.offset:]

        fd = open(self.conf_file_path, "wb")
        fd.write(fuzz_file)
        fd.close()

        # Upgrade the offset
        self.offset += len(test_case)
        self.iteration += 1

    def find_dividing_fields(self):

        exist = False

        fd = open(self.conf_file_path, "rb")
        fd_text = fd.read()
        fd.close()
        fd_size = len(fd_text)

        for fd_iterator in range(0, fd_size):
            for iterator in range(0, len(self.dividing_fields)):
                if fd_text[fd_iterator] == self.dividing_fields[iterator]:
                    exist = True
                    print( "Dividing field found - ", str(self.dividing_fields[iterator]))
                    print( "Offset: ", fd_iterator)

        if exist is False:
            print('No one found field')

    def change_bytes(self, start_offset, end_offset, index, amount):
        self.delete_bytes(start_offset, end_offset)
        self.add_bytes(start_offset, index, amount)

    def add_bytes(self, file_offset, index, amount):

        fd = open(self.conf_file_path, "rb")
        stream = fd.read()
        fd.close()

        # if file_offset > len(stream):
        #     file_offset = len(stream)

        new_bytes = self.test_cases[index] * amount

        fuzz_file = stream[0:file_offset]
        fuzz_file += bytes(new_bytes)
        fuzz_file += stream[file_offset:]

        fd = open(self.conf_file_path, "wb")
        fd.write(fuzz_file)
        fd.close()
    
    def add_bytes_in_end(self,amount):
        fd = open(self.conf_file_path, "rb")
        stream = fd.read()
        fd.close()

        new_bytes = self.test_cases[3] * amount

        fuzz_file = stream
        fuzz_file += bytes(new_bytes)

        fd = open(self.conf_file_path, "wb")
        fd.write(fuzz_file)
        fd.close()

    def delete_bytes(self, start_offset, end_offset):

        fd = open(self.conf_file_path, "rb")
        stream = fd.read()
        fd.close()

        if end_offset > len(stream):
            end_offset = len(stream)

        fuzz_file = stream[0:start_offset]
        fuzz_file += stream[end_offset + 1:]

        fd = open(self.conf_file_path, "wb")
        fd.write(fuzz_file)
        fd.close()
