# Table of Contents

- [Table of Contents](#table-of-contents)
- [Introduction](#introduction)
  - [Purpose of this Document](#purpose-of-this-document)
- [Structural Aspects](#structural-aspects)
  - [Command-line arguments](#command-line-arguments)
  - [Inner-workings of modules](#inner-workings-of-modules)
    - [main](#main)
    - [cfg_handler](#cfg_handler)
      - [Configuration file example](#configuration-file-example)
    - [connect](#connect)
      - [serial_connect](#serial_connect)
      - [ssh_connect](#ssh_connect)
    - [test_handler](#test_handler)
    - [csv_saver](#csv_saver)

</br>

# Introduction

## Purpose of this Document

The purpose of this document is to provide the necessary technical information on how to use this program.
The purpose of this program is to automate testing of AT commands for any device that uses AT commands.

# Structural Aspects

## Command-line arguments
  - To see all available arguments 
  ```--help```
  - Arguments for **Serial connection**:
    - By using this argument, you can change **port** that is used when establishing **Serial** connection with a device
    `--p`
    -  By using this argument, you can change **baudrate** that is used when establishing **Serial** connection with a device
    `--br`
  - Arguments for **SSH connection**:
    -  By using this argument, you can change **IP address** that is used when establishing **SSH** connection with a device
    `--ip`
    -  By using this argument, you can change **port** that is used when establishing **SSH** connection with a device
    `--sp`
    -  By using this argument, you can change **username** that is used when establishing **SSH** connection with a device
    `--u`
    -  By using this argument, you can change **password** that is used when establishing **SSH** connection with a device
    `--psw`

  - In this example, a Serial connection is being established with different port and baudrate than defined in configuration file
  ```python3 main.py <device_name> --p ttyUSB3 --br 112900```
</br>

## Inner-workings of modules

### main

- Handles order in which modules are executed

- Module execution order:
  1. All modules are initialized
  2. Tests all commands from configuration file that are assigned to device that was specified at launch
  3. Passes test results to `csv_saver`

- Modules used:
  - test_handler
  - connect
  - cfg_handler
  - csv_saver
  - argparse

### cfg_handler

- Handles reading of configuration file and passing it back to main script

- Modules used:
  - json
  - os

#### Configuration file example

- A configuration file is formatted as json file
- Configuration file must be named ==config.json==
- For every device, there are a few things that **must** be defined in order for automated tests to work
  1. Device name
  2. Connection type
     1. serial
     2. ssh
  3. Authentication parameters
     1. For *serial* connection:
        1. Port
        2. Baudrate
     2. For *ssh* connection:
        1. IP address
        2. Port
        3. Username
        4. Password
  4. List of commands
     1. Command
     2. Expected returned value
     3. Extra arguments (optional)

- Here is an example of a device configuration which uses SSH connection type:

```
{
"RUTX11": {
        "auth": "ssh",
        "auth_params": {
            "username": "root",
            "password": "Admin123",
            "address": "192.168.1.1",
            "port": 22
        },
        "commands": [
            {
                "command": "ATE1",
                "expects": "OK"
            },
            {
                "command": "AT+CMGF=1",
                "expects": "OK"
            },
            {
                "command": "AT+COPS=?",
                "expects": "OK"
            },
            {
                "command": "AT+CMGS=\"+37060000000\"",
                "args": [
                    "test text"
                ],
                "expects": "OK"
            }
        ]
    }
}
```

- Here is an example of a device configuration which uses Serial connection type:

```
{
"TRM250": {
        "auth": "serial",
        "auth_params": {
            "port": "ttyUSB2",
            "baudrate": 115200
        },
        "commands": [
            {
                "command": "ATE1",
                "expects": "OK"
            },
            {
                "command": "AT+CMGF=1",
                "expects": "OK"
            },
            {
                "command": "AT+CMGS=\"+37060000000\"",
                "args": [
                    "test text"
                ],
                "expects": "OK"
            }
        ]
    }
}
```

- Here is an example of having multiple devices in one configuration file:

```
{
    "RUTX11": {
        "auth": "ssh",
        "auth_params": {
            "username": "root",
            "password": "Admin123",
            "address": "192.168.1.1",
            "port": 22
        },
        "commands": [
            {
                "command": "ATE1",
                "expects": "OK"
            },
            {
                "command": "AT+CMGF=1",
                "expects": "OK"
            },
            {
                "command": "AT+COPS=?",
                "expects": "OK"
            },
            {
                "command": "AT+CMGS=\"+37060000000\"",
                "args": [
                    "test text"
                ],
                "expects": "OK"
            }
        ]
    },
    "TRM250": {
        "auth": "serial",
        "auth_params": {
            "port": "ttyUSB2",
            "baudrate": 115200
        },
        "commands": [
            {
                "command": "ATE1",
                "expects": "OK"
            },
            {
                "command": "AT+CMGF=1",
                "expects": "OK"
            },
            {
                "command": "AT+CMGS=\"+37060000000\"",
                "args": [
                    "test text"
                ],
                "expects": "OK"
            }
        ]
    }
}
```


### connect

- Handles all connection related actions:
  - Automatically determines whether to establish Serial or SSH connection based on connection type defined in configuration file
  - Establishes connection to device
  - Handles command execution
  - Retrieves data about the device that is being tested
  - Handles loss of connection

#### serial_connect

- Extends "connect" module's functionality by adapting it's action handling specifically for Serial connection

- Modules used:
  - Serial
  - Time

#### ssh_connect

- Extends "connect" module's functionality by adapting it's action handling specifically for SSH connection

- Modules used:
  - Paramiko
  - Time

### test_handler

- Executes every command described in configuration file
- Checks for returned values and compares them with expected results
- Counts how many commands passed and failed
- Returns list of all commands along with their test results back to main module

- Modules used:
  - Re
  - Serial

### csv_saver

- Formats device information to `csv` compliant string
- Formats information about every command tested to `csv` compliant string
- Writes device information and tests results to a `.csv` file
- Example of how tests results are named:
  `RUTX11_2022-8-29-9-52_test.csv`
  1. Device name
  2. Year
  3. Month
  4. Day
  5. Hour 
  6. Minute

  **NOTE: Date is depends on time and date of result saving runtime**

  - Example of how formatted result file looks like
  
| Model: RUTX11        | Manufacturer: Quectel | Board: EG06 | Revision: EG06ELAR04A04M4G |
|----------------------|-----------------------|-------------|----------------------------|
| Command              | Expected              | Returned    | Result                     |
| ATE1                 | OK                    | OK          | Passed                     |
| AT+CMGF=1            | OK                    | OK          | Passed                     |
| AT+COPS=?            | OK                    | OK          | Passed                     |
| AT+CMGS=+37060000000 | OK                    | OK          | Passed                     |