from curses import baudrate
from sqlite3 import connect
import serial


class Connection:
    __conn = None

    def __init__(self, auth):
        port = auth['port']
        baudrate = auth['baudrate']
        self.__connect(port, baudrate)

    def __connect(self, port='ttyUSB2', baudrate=115200):
        try:
            __conn = serial.Serial(
                port='/dev/' + port,
                baudrate=baudrate,
                bytesize=serial.EIGHTBITS,
                xonxoff=False,
                rtscts=False,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=1,
                write_timeout=5
            )
            self.__conn = __conn
        except Exception as error:
            raise Exception(error)

    def exec(self, cmd, result):
        self.__conn.write(str(str(cmd) + '\r').encode())
        if result:
            return self.__conn.readall().decode('utf-8').split()
