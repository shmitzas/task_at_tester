import serial

class ConnectionHandler:
    __conn = None
    def __init__(self, cfg):
        match cfg['auth']:
            case 'serial':
                self.__conn = self.__connect_serial(cfg['auth_params']['port'], cfg['auth_params']['baudrate'])
            case 'ssh':
                self.__conn = self.__connect_ssh(cfg['auth_params'])
                
                
    def __connect_serial(self, port='ttyUSB2', baudrate=115200):
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
           
    
    def exec(self, cmd):
        self.__conn.write(str(cmd).encode())
    
    
    def res(self):
        result = self.__conn.readall().decode('utf-8').split()
        return result
    
    
    def __connect_ssh(self, cfg):
        pass