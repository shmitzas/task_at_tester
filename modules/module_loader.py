class ModuleLoader:
    __module = None
    def __init__(self, name):
        self.__module = self.__load_module(name)
        if not self.__module:
            raise Exception('Unable to load "{}" module'.format(name))
    
    def __load_module(self, name):
        module = __import__(__import__('modules.{}'.format(name), fromlist=['modules']))
        return module