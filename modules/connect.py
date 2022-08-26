class ConnectionHandler:
    __conn = None

    def __init__(self, cfg, parser):
        conn = self.__load_module(str(cfg['auth'])+'_connect')
        self.__conn = conn.Connection(cfg['auth_params'], parser)

    def exec(self, cmd, result=False):
        return self.__conn.exec(cmd, result)

    def close(self):
        self.__conn.close_connection()

    def retry_connection(self):
        return self.__conn.retry_connection()

    def __load_module(self, name):
        try:
            module = __import__('modules.{}'.format(name),
                                fromlist=['modules'])
            return module
        except:
            print('Unable to load module: "{}"'.format(name))
            exit()
