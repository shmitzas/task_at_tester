import re
import serial


class TestHandler:
    __conn = None

    def __init__(self, connection):
        self.__conn = connection

    def run_tests(self, cfg):
        passed_cmd = 0
        failed_cmd = 0
        processed_data = []
        for cmd in cfg['commands']:
            data, result = self.test_command(cmd)
            processed_data.append(data)

            if result:
                passed_cmd += 1
            else:
                failed_cmd += 1

        self.__print_results(len(cfg['commands']), passed_cmd, failed_cmd)

        return processed_data

    def test_command(self, cmd):
        num_r = re.compile(r'(?:\+\d{11})')
        data = {}
        result = False
        try:
            if 'args' in cmd.keys():
                if re.search(num_r, str(cmd['command'])) != None:
                    self.__conn.exec(str(cmd['command']))
                    try:
                        self.__conn.exec(str(cmd['args'][0]))
                        msg = self.__conn.exec(chr(26), True)
                    except:
                        print('\033[91m' + 'Error:' + '\033[0m' +
                              'Arguments for command "{}" are incorrect!'.format(str(cmd['command'])))
            else:
                msg = self.__conn.exec(str(cmd['command']), True)

            print(cmd['command'], msg, end='\033[K\r')
            
            data['command'] = cmd['command']
            data['expected'] = cmd['expects']
            data['returned'] = msg

            if msg == cmd['expects']:
                data['result'] = 'Passed'
                result = True
            elif msg == '':
                self.__conn.close()
                retry = self.__conn.retry_connection()

                if retry == False:
                    print('\033[91m' + 'Connection closed' + '\033[0m')
                    data['result'] = 'Failed'
                    result = False

                else:
                    data, result = self.test_command(cmd)
            else:
                data['result'] = 'Failed'
                result = False
        except serial.SerialException:
            self.__conn.close()
            retry = self.__conn.retry_connection()

            if retry == False:
                print('\033[91m' + 'Connection closed' + '\033[0m')
                data['result'] = 'Failed'
                result = False
            else:
                data, result = self.test_command(cmd)
        except:
            data['result'] = 'Failed'
            result = False
            print('\033[91m' + 'Error:' + '\033[0m' + ' Incorrect command!' +
                  '\nCommand: {}'.format(str(cmd['command'])))
        return data, result

    def __print_results(self, to_test, passed, failed):
        print('\n\n' + 'Commands to test: ' + str(to_test))
        print('\033[92m' + 'Passed: ' + str(passed) + '\033[0m')
        print('\033[91m' + 'Failed: ' + str(failed) + '\033[0m')
