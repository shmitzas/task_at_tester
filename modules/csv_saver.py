import csv
import datetime


class CSVHandler:
    __date = datetime.datetime.now()
    
    def __init__(self):
        pass

    def save(self, data):
        fields = ['Router', 'Command', 'Expected', 'Result']
        filename = './results/' +str(self.__date.year) + '_' + str(self.__date.month) + '_' + str(self.__date.day) + '_' + str(self.__date.hour) + '_' + str(self.__date.minute) + '_test.csv'
        
        try:
            with open(filename, 'w') as f:
                write = csv.writer(f)
                write.writerow(fields)
                write.writerows(data)
            f.close()
        except Exception as e:
            print(e)  
        