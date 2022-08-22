class ConnectionHandler:
    __conn = None
    def __init__(self, cfg):
        
        conn = self.__load_module(str(cfg['auth'])+'_connect')
        self.__conn = conn.Connection().connect(cfg['auth_params']['port'], cfg['auth_params']['baudrate'])
    
    def exec(self, cmd):
        self.__conn.write(str(cmd).encode())
    
    def res(self):
        result = self.__conn.readall().decode('utf-8').split()
        return result
    
    def __load_module(self, name):
        module = __import__('modules.{}'.format(name), fromlist=['modules'])
        return module