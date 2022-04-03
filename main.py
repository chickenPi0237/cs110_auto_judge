import os 
import sys
import subprocess
import csv
import re
import requests
import datetime
import json
import pexpect

minus_score_json = {}

time_stamp = []
name = []
id = []
url = []

target_folder = 'hw1'
deadline = '2022-03-06T15:55'

log_record_row = ['','','','','']
log_record = [['id','git_clone','comiple','execute','delay']] #2d list, every d: id, git_clone, compile, execute

root_path = 'C:\\Users\kevin_laptop\\Documents\\code\\program\\cs101_github_hw'
csv_path = '.\\cs101_lab0.csv' # csv format: time_stamp,name,id,url
url_pattern = r'https:\/\/github\.com\/[a-zA-Z0-9\.\-\_]+\/[a-zA-Z0-9\.\-\_]+'
repo_root_pattern = r'.*cs101.*'

clone_cm = 'git clone '
merge_cm = 'git merge '
pull_cm = 'git pull'
check_log_latest_commit_cm = f'git log -1 --date=format:%Y-%m-%dT%H:%M --pretty=format:"%cd" -- {target_folder}' 



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
    #c_file = 'main.c'
    compile_line = f'C:\\"Program Files (x86)"\\Dev-Cpp\\MinGW64\\bin\\gcc.exe -std=c11 {c_file} -o a.out'
    print(compile_line)
    #compile_line = f'dir'
    #os.system(compile_line)
    if 0 == subprocess.call(compile_line, shell=True):
        return 1
    else:
        return 0


 
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
    proc = pexpect.spawn('.\\a.tou', timeout=15)
    index = proc.expect(['.*'], timeout=5)
    if index == 0:
        proc.interact()
    
    
 
def write_log_file(path, file_name, table):
    #print(table)
    time_format = '%Y-%m-%dT-%H-%M'
    file_name += datetime.datetime.now().strftime(time_format)
    print(os.path.join(path, file_name+'.csv'))
    with open(os.path.join(path, file_name+'.csv'), 'w', newline='') as log_file :
        writer = csv.writer(log_file)
        
        writer.writerows(table)
'''
def reg_match(string, reg, type):
    if type == 1:
        if re.fullmatch(repo_root_pattern, sgring):
            return string
        else:
            return
'''        

        

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

    #iterate github link list
    for row in zip(time_stamp,name,id,url):
        #reset log_record_row
        log_record_row = ['','','','','']
        
        std_folder = os.path.join('.\\hw',row[2])
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
                os.chdir(os.path.join('.\\', repo))
                print('clone fail, maybe repo is already exist , try pull')
                if 0 == subprocess.call(pull_cm):
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
                os.chdir(os.path.join('.\\hw', row[2], repo, target_folder))
            except:
                log_record_row[1] = 'cant change dir to target folder'
                log_record.append(log_record_row)
                continue
            print(os.getcwd())
            if auto_compile('main.c', target_folder) != 1:
                print('auto compile fail at std ', row[2])
                log_record_row[2]='auto compile fail'
            else:
                log_record_row[2]='auto comile success'
                #execute_code()
            os.chdir(root_path)
            
            log_record.append(log_record_row)
            
            write_log_file('.\\', 'log_test_hw1_', log_record)
            
            
        #input('1 timee')
'''
 目前繳交時間解決方式
 https://api.github.com/repos/YuChiehChuang/cs101/commits?path=lab1/
 ref :
 https://docs.github.com/en/rest/reference/commits#get-a-commit
 https://docs.github.com/en/rest/reference/repos#create-or-update-file-contents
 https://superuser.com/questions/1406875/how-to-get-the-latest-commit-date-of-a-file-from-a-given-github-reposotiry
 抓取特定資料夾下的commit時間
 時間格式套件
 https://stackoverflow.com/questions/2150739/iso-time-iso-8601-in-python
'''