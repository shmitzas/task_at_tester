import re


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
                msg = res[-2]

                data['Command'] = cmd['command']
                data['Expected'] = cmd['expects']
                data['Returned'] = msg

                if msg == cmd['expects']:
                    data['Result'] = 'Passed'
                else:
                    data['Result'] = 'Failed'

            except Exception as e:
                print('saaaaaaaa')
                print(e)

            processed_data.append(data)
        return processed_data
