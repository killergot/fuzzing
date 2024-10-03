import filecmp

print(filecmp.cmp('config_13', 'exe\\config_13', shallow=False))