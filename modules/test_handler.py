import re
import time

class TestHandler:
    __conn = None

    def __init__(self, connection):
        self.__conn = connection

    def run_tests(self, cfg):  
        processed_data = []
        num_r = re.compile(r'(?:\+\d{11})')
        for cmd in cfg['commands']:
            print(cmd['command'])
            data = {}
            try:
                if 'args' in cmd.keys():
                    if re.search(num_r, str(cmd['args'])) != None:
                        self.__conn.exec((str(cmd['command']) + '="' + str(cmd['args'][0]) + '"\r'))
                    else:
                        self.__conn.exec((str(cmd['command']) + '=' + str(cmd['args'][0]) + '\r'))
                    try:
                        for arg in cmd['args'][1::]:
                            self.__conn.exec(str(arg))
                            self.__conn.exec(chr(26))
                    except Exception as e:
                        pass
                else:
                    self.__conn.exec((str(cmd['command']) + '\r'))
                res = self.__conn.res()
                msg = res[-1]

                data['command'] = cmd['command']
                data['expected'] = cmd['expects']
                data['returned'] = msg

                if msg == cmd['expects']:
                    data['result'] = 'Passed'
                else:
                    data['result'] = 'Failed'

            except Exception as e:
                print(e)

            processed_data.append(data)
        
        return processed_data
