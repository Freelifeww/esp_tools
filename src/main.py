#!/usr/bin/env python
#
# ESP8266 & ESP32 ROM Bootloader Utility
# Copyright (C) 2014-2016 Fredrik Ahlberg, Angus Gratton, Espressif Systems (Shanghai) PTE LTD, other contributors as noted.
# https://github.com/Freelifeww/esp_tools
#
# This program is based on the burning script of Lexin continue to further interface 
# related efuse burning and file burning operation, to achieve a key operation to complete 
# the burning you want, do not repeatedly input different commands

import argparse
import io
import json
import os
import struct
import sys
import time

espefuse_cmd = [
    ('espefuse.py -p %s summary'),
    ('espefuse.py -p %s burn_efuse DISABLE_DL_CACHE 1'),
    ('espefuse.py -p %s burn_efuse JTAG_DISABLE 1'),
    ('espefuse.py -p %s burn_efuse DISABLE_DL_ENCRYPT 1'),
    ('espefuse.py -p %s burn_efuse DISABLE_DL_DECRYPT 1'),
    ('espefuse.py -p %s burn_efuse FLASH_CRYPT_CONFIG 15'),
    ('espefuse.py -p %s burn_efuse FLASH_CRYPT_CNT 1'),
    ('espefuse.py -p %s write_protect_efuse FLASH_CRYPT_CNT'),
    ('espefuse.py -p %s burn_key flash_encryption burn_key.BLK1.bin'),
    ('espefuse.py -p %s summary'),
]

esptool_cmd = [
    ('esptool.py -p %s -b 460800 --before default_reset --after no_reset write_flash --flash_mode dio --flash_size detect --flash_freq 40m 0x1000 flash.4096.bin 0xF000 flash.61440.bin 0x15000 flash.86016.bin 0x20000 flash.131072.bin 0x3d8000 flash.4030464.bin')
]

input_prinf_cmd = [
    ('serial','Please enter the device connection serial port name such as COM1 \n Type "COM1" (all capitals) to continue.'),
    ('sucess','Project burning successful any button to end the burning window'),
    ('fail','Project burning error, please save log, press any key to end'),
]

def input_serial_com(input_string):
    for cmd_string in input_prinf_cmd:
        #if cmd_string[0] == input_string
        print(cmd_string[1])
    sys.stdout.flush()  #required for Pythons which disable line buffering, ie mingw in mintty
    try:
        user_input_str = raw_input()  # raw_input renamed to input in Python 3
    except NameError:
        user_input_str = input()
    return user_input_str
    
"""
def input_sucess_com():
    print("Project burning successful any button to end the burning window")
    sys.stdout.flush()  #required for Pythons which disable line buffering, ie mingw in mintty
    try:
        com_str = raw_input()  # raw_input renamed to input in Python 3
    except NameError:
        com_str = input()
    return com_str

def input_file_com():
    print("Project burning error, please save log, press any key to end")
    sys.stdout.flush()  #required for Pythons which disable line buffering, ie mingw in mintty
    try:
        com_str = raw_input()  # raw_input renamed to input in Python 3
    except NameError:
        com_str = input()
    return com_str
"""

def err_exit(ret,str):
    if ret != 0 :
        print("%s err exit" % str)
        input_serial_com(input_prinf_cmd[0])
        sys.exit(ret)
    print("%s success" % str)

#need write efuse data string
def efuse_tools_cmd(com_number):
    for cmd_string in espefuse_cmd:
        cmd_string = (cmd_string % com_number)
        print(cmd_string)
        ret = os.system(cmd_string)
        err_exit(ret,cmd_string)

#need write file data string
def esp_file_tools_cmd(com_number):
    for cmd_string in esptool_cmd:
        cmd_string = (cmd_string % com_number)
        print(cmd_string)
        ret = os.system(cmd_string)
        err_exit(ret,cmd_string)

def main(custom_commandline=None):
    com_number = input_serial_com(input_prinf_cmd[0])
    #esp_file_tools_cmd(com_number)
    #efuse_tools_cmd(com_number)
    #input_sucess_com()

def _main():
    try:
        main()
    except esptool.FatalError as e:
        print('\ntool main a fatal error occurred: %s' % e)
        sys.exit(2)

if __name__ == '__main__':
    _main()
