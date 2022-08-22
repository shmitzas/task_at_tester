import serial

class Connection:
    def connect(self, port='ttyUSB2', baudrate=115200):
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
        return __conn