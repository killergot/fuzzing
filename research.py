import os
import re

# drrun.exe -t drcov -logdir B:\mbks\python_2_lab\exe\mutations  -- B:\\mbks\\python_2_lab\\exe\\vuln13.exe

def create_folder(folder_path):
    if not os.path.exists(folder_path):
        try:
            os.makedirs(folder_path)
            return True
        except:
            return False
    else:
        return True

def mark_res(conf_file_path,mut_folder_path,iteration,exe_path):
    folder_path = mut_folder_path + '\\num_' + str(iteration)
    if create_folder(folder_path):
        save_config(conf_file_path,folder_path,iteration)
        

def save_config(conf_file_path,mut_folder_path,iteration):
        fd = open(conf_file_path, "rb")
        stream = fd.read()
        fd.close()

        fd = open(mut_folder_path + "\\" + "config_mutation_" + str(iteration), "wb")
        fd.write(stream)
        fd.close()

def run_dercov(folder_path,exe_path):
    os.system('C:\\Users\\max\\Downloads\\DynamoRIO-Windows-10.0.0\\bin32\\drrun.exe' + ' -t drcov -dump_text -logdir '+ folder_path +' -- ' + exe_path)
    return analize_coverage(folder_path)

def analize_coverage(folder_path):
    temp = os.listdir(folder_path)[1]
    fd = open(folder_path+'\\'+temp)
    count_str = 0
    count_base_block = 0
    for i in fd:
        count_str += 1
        if count_str > 18:
            number = re.search(r'\d+', i).group()
            if number in ['0','1']:
                count_base_block +=1
    
    fd.close()
    if not 'num' in folder_path:
        os.remove(folder_path+'\\'+temp)
    return count_base_block


if __name__ == '__main__':
    run_dercov("B:\\mbks\\python_2_lab\\exe\\mutations\\base","B:\\mbks\\python_2_lab\\exe\\vuln13.exe")
    print(analize_coverage("B:\\mbks\\python_2_lab\\exe\\mutations"))

