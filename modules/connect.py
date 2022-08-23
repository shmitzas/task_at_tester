class ConnectionHandler:
    __conn = None

    def __init__(self, cfg):
        conn = self.__load_module(str(cfg['auth'])+'_connect')
        self.__conn = conn.Connection(cfg['auth_params'])

    def exec(self, cmd, result=False):
        return self.__conn.exec(cmd, result)

    def __load_module(self, name):
        try:
            module = __import__('modules.{}'.format(name),
                                fromlist=['modules'])
            return module
        except Exception as error:
            raise Exception(error)
