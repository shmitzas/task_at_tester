import re
import time

class TestHandler:
    __conn = None

    def __init__(self, connection):
        self.__conn = connection

    def run_tests(self, cfg):  
        passed_cmd = 0
        failed_cmd = 0
        processed_data = []
        num_r = re.compile(r'(?:\+\d{11})')
        for cmd in cfg['commands']:
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
                print(res[0])

                data['command'] = res[0]
                data['expected'] = cmd['expects']
                data['returned'] = msg

                if msg == cmd['expects']:
                    data['result'] = 'Passed'
                    passed_cmd+=1
                else:
                    data['result'] = 'Failed'
                    failed_cmd+=1

            except Exception as e:
                print(e)

            processed_data.append(data)
            
        print('\n' + 'Commands to test: ' + str(len(cfg['commands'])))
        print('\033[92m' + 'Passed: ' + str(passed_cmd) + '\033[0m')
        print('\033[91m' + 'Failed: ' + str(failed_cmd) + '\033[0m')
        
        return processed_data
