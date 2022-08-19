from modules.test_handler import TestHandler
from modules.connect import ConnectionHandler
from modules.cfg_handler import ConfigHandler
from modules.csv_saver import CSVHandler
import os
import sys

# Disable modem manager
os.system('sudo systemctl stop ModemManager.service')

cfg = None
conn = None
tests = None
results = None

config_filename = 'config.json'

def init_modules():
    global cfg, conn, tests, results
    cfg = ConfigHandler(config_filename)
    conn = ConnectionHandler(cfg.get_param(sys.argv[1].upper()))
    tests = TestHandler(conn)
    
def main():
    init_modules()
    tests.run_tests()


if __name__ == '__main__':
    main()