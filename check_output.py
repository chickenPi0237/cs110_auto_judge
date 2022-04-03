import os
import subprocess


print("this is inside python")
print('\"C:\\Program Files (x86)\\Dev-Cpp\\MinGW64\\bin\\gcc.exe\" \"C:\\Users\\kevin_laptop\\Documents\\github_test\\cs101_test\\helloworld.c\" -o temp2.exe')
cs = 'C:\\"Program Files (x86)"\\Dev-Cpp\\MinGW64\\bin\\gcc.exe "C:\\Users\\kevin_laptop\\Documents\\github_test\\cs101_test\\helloworld.c" -o temp2.exe'
os.system(cs)
#a=subprocess.check_output("C:\\Users\\kevin_laptop\\Documents\\github_test\\cs101_test\\temp.exe",stderr=subprocess.STDOUT,shell=True)
a=subprocess.check_output(".\\temp2.exe",stderr=subprocess.STDOUT,shell=True)
a=a.decode('utf-8')
print(a+' 465')
print("this is inside python")