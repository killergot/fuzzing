import shutil
import fileFuzzer

exe_path = "B:\\mbks\\python_2_lab\\exe\\vuln13.exe"
config_path = "B:\\mbks\\python_2_lab\\config_13"
config_path_default = "B:\\mbks\\python_2_lab\\exe\\config_13_default"
mut_folder_path = "B:\\mbks\\python_2_lab\\exe\\mutations"
dercov_path = 'C:\\Users\\max\\Downloads\\DynamoRIO-Windows-10.0.0\\bin32\\drrun.exe'
fuzzer = fileFuzzer.FileFuzzer(exe_path, config_path, mut_folder_path)

def menu_bar():
    print("1 - Auto-fuzzing")
    print("2 - Change byte\\bytes")
    print("3 - Add byte\\bytes")
    print("4 - Delete byte\\bytes")
    print("5 - Random mutation")
    print("6 - Find dividing fields")
    print("7 - Reborn config file")
    print("8 - Test programm")
    print("0 - Exit()")

def command_one_auto_fuzzing(fuzzer):
    fuzzer.auto_fuzzing()

def command_two_change_byte(fuzzer):
    start_offset = input("Enter start offset: ")
    end_offset = input("Enter end offset: ")
    print("Choose test case: ",fuzzer.test_cases)
    test_case_index = input("Enter index of byte: ")
    amount = input("Enter amount: ")
    fuzzer.change_bytes(start_offset, end_offset, test_case_index, amount)

def command_tree_add_byte(fuzzer):
    start_offset = input("Enter start offset: ")
    print("Choose test case: ",fuzzer.test_cases)
    test_case_index = input("Enter index of byte: ")
    amount = input("Enter amount: ")
    fuzzer.add_bytes(start_offset, test_case_index, amount)

def command_four_delete_bytes(fuzzer):
    start_offset = input("Enter start offset: ")
    end_offset = input("Enter end offset: ")
    fuzzer.delete_bytes(start_offset, end_offset)

def command_five_random_mutation(fuzzer):
    fuzzer.mutate_file()

def command_six_find_div_fields(fuzzer):
    fuzzer.find_dividing_fields()

def command_seven_reborn_config(_):
    try:
        shutil.copy2(config_path_default, config_path)
        print('Succesfull complete')
    except:
        print('smt wrong:/')

def command_eight_test_programm(fuzzer):
    fuzzer.test_prog()