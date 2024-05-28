import os 
import sys
import subprocess
import csv
import re
import requests
import datetime
import json
import pexpect
#from assist_scripts.lab2 import read_file #read lotto_record.bin
#from assist_scripts.hw2 import read_file as read_file_hw2 #read emp_record.bin
#from assist_scripts import countAlphabate as freqAlpha_fin3

minus_score_json = {}

time_stamp = []
name = []
id = []
url = []
'''
#hw1 arg
target_folder = 'hw1'
deadline = '2022-03-08T13:00'
output_file_list = ['lotto.txt']
'''
'''
#qz1 arg
target_folder = 'qz1'
deadline = '2022-03-10T00:00'
output_file_list = ['lotto[0001].txt', 'lotto[0002].txt', 'lotto[0003].txt', 'lotto[0004].txt']
not_output_file_extension = [r'.*\.c', r'.*\.out']
'''
'''
#lab1 arg
target_folder = 'lab1'
deadline = '2022-03-10T17:10'
'''
'''
#lab2 arg
target_folder = 'lab2'
deadline = '2022-03-17T17:10'
'''
'''
#hw2 arg
target_folder = 'hw2'
deadline = '2022-03-22T12:00'
'''
'''
#qz2 arg
target_folder = 'qz2'
deadline = '2022-03-22T14:00'
'''
##hw3 hw4 paper work
'''
#hw3 arg
target_folder = 'hw3'
deadline = '2022-03-29T00:00'
'''
'''
#lab3 arg
target_folder = 'lab3'
deadline = '2022-03-31T17:10'
'''
'''
#hw4 arg
target_folder = 'hw4'
deadline = '2022-04-05T00:00'
'''
'''
#qz3 
target_folder = 'qz3'
deadline = '2022-04-08T00:00'
'''
'''
#lab4 arg
target_folder = 'lab4'
deadline = '2022-04-14T17:10'
'''
'''
#hw5 arg
target_folder = 'hw5'
deadline = '2022-04-19T00:00'
'''
'''
#qz4 arg
target_folder = 'qz4'
deadline = '2022-04-19T15:10'
'''
'''
#lab5 arg
target_folder = 'lab5'
deadline = '2022-04-25T15:10'
'''
'''
#lab6 arg
target_folder = 'lab6'
deadline = '2022-05-03T15:10'
'''
'''
#hw6 arg
target_folder = 'hw6'
deadline = '2022-05-15T00:00'
'''
'''
#qz5 arg
target_folder = 'qz5'
deadline = '2022-05-19T17:10'
'''
'''
#hw7 arg
target_folder = 'hw7'
deadline = '2022-06-01T00:00'
'''
'''
#qz6 arg
target_folder = 'qz6'
deadline = '2022-05-31T15:10'
'''
'''
#hw8 arg
target_folder = 'hw8'
deadline = '2022-06-08T00:00'
'''
'''
#hw9 arg
target_folder = 'hw9'
deadline = '2022-06-14T00:00'
'''
'''
#qz7 arg
target_folder = 'qz7'
deadline = '2022-06-14T15:10'
'''
#final1 arg
target_folder = 'fin1'
deadline = '2022-06-23T17:00'

log_record_row = ['','','','','','']
log_record = [['id','git_clone','comiple','execute','delay','score']] #2d list, every d: id, git_clone, compile, execute

root_path = '/media/syh/1tb_disk/cs110/auto_judge_program'
#csv_path = './cs101_problem.csv'
csv_path = './cs101_lab0_mod.csv' # csv format: time_stamp,name,id,url
#csv_path = 'dir_name_error.csv'
#csv_path = 'mod_std_1_50_new.csv'
#csv_path = 'mod_std_3637.csv'
url_pattern = r'https:\/\/github\.com\/[a-zA-Z0-9\.\-\_]+\/[a-zA-Z0-9\.\-\_]+'
repo_root_pattern = r'.*cs101.*'

clone_cm = 'git clone '
merge_cm = 'git merge '
pull_cm = 'git pull'
check_log_latest_commit_cm = f'git log -1 --date=format:%Y-%m-%dT%H:%M --pretty=format:"%cd" -- {target_folder}' 

next_std_flag = False
recover_from_tmp_flag = False


def load_token():
    with open('github_personal_token.txt', 'r') as token_file:
        token = token_file.readline()
    return token

def url_parse(url):
    owner = url.split('/')[-2]
    repo = url.split('/')[-1].split('.git')[0]
    print(owner, repo)
    return owner, repo
#api way but can do by local log, check check_latest_commit_log
def check_latest_commit(owner, repo, folder_path):
    session = requests.Session()
    request_url = f'https://api.github.com/repos/{owner}/{repo}/commits?path={folder_path}/'
    #check remain request_url = 'https://api.github.com/rate_limit'
    token = load_token()
    session.auth = ('chickenPi', token)
    #auth = session.post(request_url)
    response = session.get(request_url)
    print(response.headers)
    if response.status_code != 200:
        print('maybe github server is broke or limited by api request')
    else:
        response_dict = response.json()
        #check
        print(json.dumps(response.json(), indent=4))
        try:
            latest_commit_time = response_dict[0]['commit']['author']['date'][:-4] #ori 2022-03-10T09:00:19Z
        except:
            print('cant check latest commit')
            log_record_row[1]='cant check latest commit'
        print('test commit time ', latest_commit_time)
        return latest_commit_time
        
def check_latest_commit_log():
    proc = subprocess.Popen(check_log_latest_commit_cm, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    line = proc.stdout.readline()
    #print('here',line)
    line = line.decode()
    #print('here',line)
    return line
        
def delay_commit_minus(std_commit_time, deadline):
    time_format = '%Y-%m-%dT%H:%M'
    print("latest commit time: ",std_commit_time)
    std_commit_time_obj = datetime.datetime.strptime(std_commit_time, time_format)
    deadline_obj = datetime.datetime.strptime(deadline, time_format)
    
    delta = std_commit_time_obj - deadline_obj
    day_delta = datetime.timedelta(days=1)
    #print('test delta ',divmod(delta, day_delta))
    #print('test delta ',delta, day_delta)
    delay_in_day, remainder = divmod(delta, day_delta)
    #print('test delta', delay_in_day, remainder)
    
    if delay_in_day < 0:
        return 0
    elif delay_in_day == 0 and remainder.seconds == 0 :
        return 0
    elif delay_in_day == 0 and remainder.seconds > 0 : 
        return 5*(delay_in_day+1)
    elif delay_in_day > 0:
        return 5*(delay_in_day+1)

#use expect to replace this function
def auto_compile(c_file, target_folder):
    #compile_line = f'C:\\"Program Files (x86)"\\Dev-Cpp\\MinGW64\\bin\\gcc.exe -std=c11 {c_file} -o a.out'
    compile_line = f'g++ -std=c++11 {c_file} -o a.out'
    print(compile_line)
    #compile_line = f'dir'
    #os.system(compile_line)
    if 0 == subprocess.call(compile_line, shell=True):
        return 1
    else:
        return 0

def compile_code():
    target_c = input('chose .c file to compile :')
    if auto_compile(target_c, target_folder) != 1:
        print('auto compile fail at std ', row[2])
        log_record_row[2]='auto compile fail'
    else:
        log_record_row[2]='auto compile success'


 
def execute_code():
    #!!!!replace by pexpect
    '''
    execute_line = '.\\a.out'
    proc = subprocess.Popen([execute_line], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE , shell=True)
    try :
        out, err = proc.communicate(timeout=15, input)
        print(out)
        print(out.decode('big5'))
        keyin = input('py: ')
        out, err = proc.communicate(input=keyin)
    except subprocess.TimeoutExpired:
        proc.kill()
        log_record_row[3]='execute timeout'
    
    log_record_row[3]='execute success'
    #print(out.decode())
    '''
    #pexpect way
    proc = pexpect.spawn('./a.out', timeout=15)
    index = proc.expect(['.*'], timeout=5)
    if index == 0:
        proc.interact()
        return 1
        #proc.sendline('4')
    else:
        return 0

def find_output_file():
    file_open_count = 0
    not_in_extension_flag = True
    files = os.listdir('./')
    for file_name in files:
        for extension in not_output_file_extension:
            if re.match(extension, file_name) == None:
                not_in_extension_flag = True
            else:
                not_in_extension_flag = False
                break
        if not_in_extension_flag:
            file_open_count += show_txt(file_name)
                
    return file_open_count

def read_all_output_file():
    file_open_count = 0
    for output_file_name in output_file_list:
        file_open_count += show_txt(output_file_name)
    return file_open_count

def show_file_in_current_folder():
    subprocess.call('ls -l ./', shell=True)

def show_bin(file_name):
    print(' ')
    print(f'---------reading {file_name}---------')
    cm_line = f'xxd {file_name}'
    if 0 == subprocess.call(cm_line, shell=True):
        return 1
    else:
        return 0
    print(' ')

def show_txt(file_name):
    print(' ')
    print(f'---------reading {file_name}---------')
    cm_line = f'cat {file_name}'
    if 0 == subprocess.call(cm_line, shell=True):
        return 1
    else:
        return 0
    print(' ')
def show_txt_tail(file_name):
    print(' ')
    print(f'---------reading {file_name}---------')
    cm_line = f'tail -n 20 {file_name}'
    if 0 == subprocess.call(cm_line, shell=True):
        return 1
    else:
        return 0
    print(' ')

def read_structure_bin_setup():
    #print('bin setup ',os.getcwd())
    subprocess.call('mkdir ./tmp', shell=True)
    subprocess.call(f'cp /home/ubuntu/python_auto_judge/assist_scripts/{target_folder}/* ./tmp/', shell=True)
def read_structure_bin_clean():
    subprocess.call('rm -r ./tmp', shell=True)
def read_way(chosen_file_name):
    read_way_command = input('How to read file? (1)txt (2)one value bin (3)structure bin (4)show alphabet freq:')
    if read_way_command == '1':
        read_way_command_2 = input('Full text or tail? (1)full (2)tail :')
        if read_way_command_2 == '1':
            show_txt(chosen_file_name)
        elif read_way_command_2 == '2':
            show_txt_tail(chosen_file_name)
    elif read_way_command == '2':
        show_bin(chosen_file_name)
    elif read_way_command == '3':
        main_file_name = input('enter main file name :')
        read_structure_bin_setup()
        current_path = os.getcwd()
        os.chdir('./tmp')
        read_file_hw2.read_bin_data('../'+chosen_file_name, main_file_name)
        os.chdir(current_path)
        #read_structure_bin_clean()
    elif read_way_command == '4':
        f = open(chosen_file_name)
        fs = freqAlpha_fin3.file_stat()
        fs.freqFile(f)
        fs.show_dict()
        f.close()
    else:
        print('wrong read way command, enter again.')
    
    
 
def write_log_file(path, file_name, table):
    #print(table)
    time_format = '%Y-%m-%dT-%H-%M'
    file_name += datetime.datetime.now().strftime(time_format)
    if not os.path.isdir(path):
        os.mkdir(path)
    print(os.path.join(path, file_name+'.csv'))
    with open(os.path.join(path, file_name+'.csv'), 'w', newline='') as log_file :
        writer = csv.writer(log_file)
        
        writer.writerows(table)
def write_tmp_log_file(path, file_name, table):
    #print(table)
    #time_format = '%Y-%m-%dT-%H-%M'
    #file_name += datetime.datetime.now().strftime(time_format)
    if not os.path.isdir(path):
        os.mkdir(path)
    print(os.path.join(path, file_name+'.csv'))
    with open(os.path.join(path, file_name+'.csv'), 'w', newline='') as log_file :
        writer = csv.writer(log_file)
        
        writer.writerows(table)
def recover_from_tmp(target_folder, log_record):
    csv_path = f'./log/{target_folder}/tmp.csv'
    with open(csv_path, newline='', encoding='utf-8') as csv_file:
        table = csv.reader(csv_file, delimiter=',')
        header = next(table)
        for row in table:
            log_record.append(row)
        print(log_record)
'''
def reg_match(string, reg, type):
    if type == 1:
        if re.fullmatch(repo_root_pattern, sgring):
            return string
        else:
            return
'''        
def interact_judge():
    show_file_in_current_folder()
    interact_command = input('what to do? pls enter (1)compile file (2)execute app (3)read app output file (4)score :')
    if interact_command == '1':
        compile_code()
    elif interact_command == '2':
        execute_code()
    elif interact_command == '3':
        chosen_file = input('pls enter file name :')
        read_way(chosen_file)
    elif interact_command == '4':
        score = input('(auto_judge) given score : ')
        log_record_row[5] = score
        return True
    else:
        print('wrong interact_command, enter again.')
        

if __name__ == '__main__':

    #test platform
    #print(sys.platform)
    #input('wait')



    #read student github links csv
    with open(csv_path, newline='', encoding='utf-8') as csv_file:
        table = csv.reader(csv_file, delimiter=',')
        header = next(table)
        for row in table:
            time_stamp.append(row[0])
            name.append(row[1])
            id.append(row[2].upper())
            url.append(row[3])
    if input('recover from tmp?(1)/(0)') == '1':
        recover_from_tmp_flag = True
        recover_from_tmp(target_folder, log_record)

    input('rec over')
    #iterate github link list
    for row in zip(time_stamp,name,id,url):
        #reset log_record_row
        log_record_row = ['','','','','','']
        #recover from tmp skip
        if recover_from_tmp_flag:
            if log_record[-1][0] == row[2]:
                recover_from_tmp_flag = False
            continue
        
        std_folder = os.path.join('./hw',row[2])
        print(std_folder)
        
        #log record
        log_record_row[0] = row[2]
        
        owner, repo = url_parse(row[3])
        
        if not os.path.exists(std_folder) and re.fullmatch(url_pattern, row[3]):
            print(row[3])
            os.mkdir(std_folder)
            
        elif not re.fullmatch(url_pattern, row[3]):
            print('url wrong : ',row[2],row[3])
            
            #log record 
            log_record_row[1]='wrong url, cant clone'
            log_record_row[2]=''
            log_record_row[3]=''
            log_record.append(log_record_row)
            
            continue
        #check commit time and calcuate delay score
        #std_time = check_latest_commit(owner, repo, target_folder)
        
            
        #If folder is empty, clone repo and compile
        if not os.listdir(std_folder):
            os.chdir(std_folder)
            os.system(clone_cm+row[3])
            os.chdir(root_path)
        else:
            #call fetch and merge
            os.chdir(std_folder)
            if 0 == subprocess.call(clone_cm+row[3], shell=True):
                print('clone success')
                log_record_row[1]='clone success'
                
            else:
                #git clone fail, folder already exists, git merge 
                os.chdir(os.path.join('.', repo))
                print('clone fail, maybe repo is already exist , try pull')
                print(os.getcwd())
                if 0 == subprocess.call(pull_cm, shell=True):
                    log_record_row[1]='pull success'
                else:
                    log_record_row[1]='pull fail'
                #os.system(merge_cm)
 
            std_time = check_latest_commit_log()
            if std_time == '':
                log_record_row[4] = 'Nan'
            else :
                #print('minus score ', delay_commit_minus(std_time, deadline))
                log_record_row[4]=delay_commit_minus(std_time, deadline)  
            
            os.chdir(root_path)
            #change pwd to target folder to start compile
            #test check parameter
            try :
                print('test check parameter, ',os.getcwd() ,row[2] ,repo ,target_folder)
                os.chdir(os.path.join('./hw', row[2], repo, target_folder))
            except:
                log_record_row[1] = 'cant change dir to target folder'
                log_record.append(log_record_row)
                continue
            print(os.getcwd())
            #auto way (not finished)
            '''if auto_compile('main.c', target_folder) != 1:
                print('auto compile fail at std ', row[2])
                log_record_row[2]='auto compile fail'
            else:
                log_record_row[2]='auto compile success'
                if execute_code() == 1:
                    log_record_row[3] = 'execute success'
                    if read_all_output_file() == len(output_file_list):
                        ## note: need to check all output file by eyes 
                        score = input('(auto_judge) given score : ')
                        log_record_row[5] = score
                    elif find_output_file() != 0:
                        print('output file name not right')
                        score = input('(auto_judge) given score : ')
                        log_record_row[5] = score
                    else:
                        log_record_row[3] = 'no output file'
                else:
                    log_record_row[3] = 'execute fail'
            '''
            #interact way
            while not next_std_flag:
                next_std_flag = interact_judge()
            os.chdir(root_path)
            next_std_flag = False
            log_record.append(log_record_row)
            
        
            
            
        #input('1 timee')
        write_tmp_log_file(f'./log/{target_folder}', 'tmp', log_record)
    csv_name = csv_path.split('.')[0]
    write_log_file(f'./log/{target_folder}', f'log_test_{target_folder}_{csv_name}_', log_record)
'''
 
 https://api.github.com/repos/YuChiehChuang/cs101/commits?path=lab1/
 ref :
 https://docs.github.com/en/rest/reference/commits#get-a-commit
 https://docs.github.com/en/rest/reference/repos#create-or-update-file-contents
 https://superuser.com/questions/1406875/how-to-get-the-latest-commit-date-of-a-file-from-a-given-github-reposotiry

 https://stackoverflow.com/questions/2150739/iso-time-iso-8601-in-python
'''