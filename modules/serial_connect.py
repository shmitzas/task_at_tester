import serial
import time


class Connection:
    __conn = None
    __port = None
    __baudrate = None

    def __init__(self, auth, parser):
        try:
            if parser.p:
                self.__port = parser.p
            else:
                self.__port = auth['port']
            if parser.br:
                self.__baudrate = parser.br
            else:
                self.__baudrate = auth['baudrate']
        except:
            print('Serial login credentials are invalid')
            exit()
        if not self.__open_connection():
            print('Unable to establish Serial connection')
            exit()

    def __open_connection(self):
        try:
            __conn = serial.Serial(
                port='/dev/' + self.__port,
                baudrate=self.__baudrate,
                bytesize=serial.EIGHTBITS,
                xonxoff=False,
                rtscts=False,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=1,
                write_timeout=1
            )
            self.__conn = __conn
            return True
        except:
            return None

    def exec(self, cmd, result):
        acceptable_results = [
            'OK', 'ERROR', 'NO CARRIER'
        ]
        try:
            self.__conn.write((str(cmd) + '\r').encode())
            if result:
                time_limit = time.time()+180
                while time.time() < time_limit:
                    res = self.__conn.readall().decode('utf-8').split()
                    try:
                        msg = str(res[-1]).replace('\n', '')
                    except:
                        pass
                    if msg in acceptable_results:
                        return msg
                    time.sleep(5)
                return msg
        except Exception as error:
            print(error)
            exit()

    def retry_connection(self):
        counter = 0
        limit = 3
        while counter < limit:
            time.sleep(5)
            if self.__open_connection():
                break
            counter += 1
            time.sleep(5)
        if counter < limit:
            return True
        else:
            return False

    def close_connection(self):
        if self.__conn:
            self.__conn.close()
