import time
import paramiko


class Connection:

    __ssh_client = None

    def __init__(self, auth):
        addr = auth['address']
        username = auth['username']
        password = auth['password']
        if not self.__open_connection(addr, username, password):
            raise Exception("Unable to connect to SSH server")

    def __close_connection(self):
        if self.__ssh_client:
            self.__ssh_client.close()

    def __open_connection(self, addr, username, password):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(addr, 22, username, password)
            self.__ssh_client = client.invoke_shell()
            time.sleep(1)
            self.__ssh_client.send('socat /dev/tty,raw,echo=0,escape=0x03 /dev/ttyUSB3,raw,setsid,sane,echo=0,nonblock ; stty sane\r')
            time.sleep(1)
            return True
        except:
            return None

    def exec(self, command, result):
        self.__ssh_client.send(str(command) + '\r')
        time.sleep(1)
        if result:
            return self.__ssh_client.recv(-1).decode('utf-8').split('\n\n')

    def __del__(self):
        self.__close_connection()
