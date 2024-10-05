import os

# drrun.exe -t drcov -logdir B:\mbks\python_2_lab\exe\mutations\drc  -- B:\\mbks\\python_2_lab\\exe\\vuln13.exe

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
        run_dercov(folder_path,exe_path)

def save_config(conf_file_path,mut_folder_path,iteration):
        fd = open(conf_file_path, "rb")
        stream = fd.read()
        fd.close()

        fd = open(mut_folder_path + "\\" + "config_mutation_" + str(iteration), "wb")
        fd.write(stream)
        fd.close()

def run_dercov(folder_path,exe_path):
    os.system('C:\\Users\\max\\Downloads\\DynamoRIO-Windows-10.0.0\\bin32\\drrun.exe' + ' -t drcov -logdir '+ folder_path +' -- ' + exe_path)