import re


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
                        self.__conn.exec(
                            str(cmd['command']) + '="' + str(cmd['args'][0]+'"'))
                    else:
                        self.__conn.exec(
                            str(cmd['command']) + '=' + str(cmd['args'][0]))
                    try:
                        for arg in cmd['args'][1::]:
                            self.__conn.exec(str(arg))
                            res = self.__conn.exec(chr(26), True)
                    except Exception as err:
                        pass
                else:
                    res = self.__conn.exec(str(cmd['command']), True)
                msg = str(res[-1]).replace('\n', '')
                
                print(cmd['command'], msg)

                data['command'] = cmd['command']
                data['expected'] = cmd['expects']
                data['returned'] = msg

                if msg == cmd['expects']:
                    data['result'] = 'Passed'
                    passed_cmd += 1
                else:
                    data['result'] = 'Failed'
                    failed_cmd += 1

            except Exception as error:
                print(error)

            processed_data.append(data)

        print('\n' + 'Commands to test: ' + str(len(cfg['commands'])))
        print('\033[92m' + 'Passed: ' + str(passed_cmd) + '\033[0m')
        print('\033[91m' + 'Failed: ' + str(failed_cmd) + '\033[0m')

        return processed_data
