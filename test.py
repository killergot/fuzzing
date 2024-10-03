from config import *

unit_to_complete = {
        '1' : command_one_auto_fuzzing,
        '2' : command_two_change_byte,
        '3' : command_tree_add_byte,
        '4' : command_four_delete_bytes,
        '5' : command_five_random_mutation,
        '6' : command_six_find_div_fields,
        '7' : command_seven_reborn_config,
        '8' : exit
    }

a = raw_input()

print(a in unit_to_complete)