from modules.test_handler import TestHandler
from modules.connect import ConnectionHandler
from modules.cfg_handler import ConfigHandler
from modules.csv_saver import CSVHandler
import os
import sys

# Disable modem manager
os.system('systemctl stop ModemManager.service')

cfg = None
conn = None
tests = None
results = None

config_filename = 'config.json'

def init_modules():
    global cfg, conn, tests, csv_saver, router
    try:
        router = sys.argv[1].upper()
        cfg = ConfigHandler(config_filename)
        conn = ConnectionHandler(cfg.get_param(router))
        tests = TestHandler(conn)
        csv_saver = CSVHandler()
    except Exception as error:
        raise Exception(error)
    
def main():
    init_modules()
    print('Running tests for:', router, '\n')
    results = tests.run_tests(cfg.get_param(router))
    results.append(router)
    csv_saver.save(results)

if __name__ == '__main__':
    main()