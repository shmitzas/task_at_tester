from asyncore import write
import csv
import datetime


class CSVHandler:
    __date = datetime.datetime.now()

    def __init__(self):
        pass

    def save(self, data):
        header = 'Command, Expected, Returned, Result'
        filename = './results/' + str(data[-1]) + '_' + str(self.__date.year) + '-' + str(self.__date.month) + '-' + str(
            self.__date.day) + '-' + str(self.__date.hour) + '-' + str(self.__date.minute) + '_test.csv'

        try:
            with open(filename, 'w') as f:
                
                f.write(header+'\n')
                for item in data[:-1]:
                    f.write(self.formatter(item)+'\n')
            f.close()
        except Exception as e:
            print(e)
            
    def formatter(self, test):
        return str(test['command']) + ',' + str(test['expected']) + ',' + str(test['returned']) + ',' + str(test['result'])