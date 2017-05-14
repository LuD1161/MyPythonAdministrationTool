import ctypes
import os
import sys
import json
from hashlib import md5

import shutil

import psutil


def architecture():
    is_64bit = sys.maxsize > 2 ** 32
    if is_64bit:
        return u"64-bit Found"
    else:
        return u"32-bit Found"


ErrorMsg = architecture() + u"\nInstallation failed, Autoremoving files"
Title = u"Error Running !"


def messageBox(ErrorMsg, Title):
    ctypes.windll.user32.MessageBoxW(0, ErrorMsg, Title, 0x00000011)


def md5Hash(fname):  # Use this  to check successful transfer of data
    hash_md5 = md5()  # From http://stackoverflow.com/questions/3431825/generating-an-md5-checksum-of-a-file
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def locate_usb():
    import win32file
    drive_list = []
    drivebits = win32file.GetLogicalDrives()
    for d in range(1, 26):
        mask = 1 << d
        if drivebits & mask:
            # here if the drive is at least there
            drname = '%c:\\' % chr(ord('A') + d)
            t = win32file.GetDriveType(drname)
            if t == win32file.DRIVE_REMOVABLE:
                drive_list.append(drname)
    return drive_list


def createShortcut(scriptPath, description, destPath, shortcutPath):
    windir = os.getenv('WINDIR')
    with winshell.shortcut(destPath) as link:
        # link.path = a+"\\Shortcuts\\checking.py"
        link.path = scriptPath

        # get the original des  cription from the file/folder
        link.description = description

        # 1st arg : Actual File location
        # 2nd arg : icon to remove , appending .lnk in script
        link.arguments = shortcutPath + " " + destPath
        folder = os.path.isdir(destPath)
        if folder:
            link.icon_location = (windir + "\\System32\\shell32.dll", 3)
        else:
            link.icon_location = (destPath)


rpath = sys.argv[1]
upath = sys.argv[2]


def OpenFolderInUsb(upath):
    shutil.move(rpath, upath)
    os.remove(upath + ".lnk")
    os.startfile(upath)


def getStatus():
    listData = ['Host Name', 'OS Name', 'OS Version', 'OS Manufacturer', 'OS Configuration', 'OS Build Type',
                'Product ID', 'Registered Owner', 'Registered Organization', 'Original Install Date',
                'System Boot Time', 'System Manufacturer', 'System Model', 'System Type', 'Processor(s)', 'Time Zone',
                'Total Physical Memory', 'Domain', 'Logon Server']
    cache = os.popen2("SYSTEMINFO")
    source = cache[1].read()
    d = source.split('\n')
    di = []
    values = {}
    final = {}
    for a in d:
        di.append(a.split(':'))
    for a in di:
        values[a[0]] = a[1:]

    for a in listData:
        final[a] = values[a][0].strip()

    from psutil import disk_partitions

    a = disk_partitions()
    di = []
    values = {}
    for data in a:
        values['device'] = data[0]
        values['mountpoint'] = data[1]
        values['fstype'] = data[2]
        values['opts'] = data[3]
        di.append(values)

    final['disks'] = json.dumps(di)
    final['cpu_freq'] = psutil.cpu_freq()[0]
    final['memory'] =psutil.virtual_memory()[0]/1e6 # In MB
    sysDetails = json.dumps(final)
    return sysDetails
