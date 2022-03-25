# author:wangwei
# time: 2022/3/24
from __future__ import division, print_function

import argparse
import io
import json
import os
import struct
import sys
import time

#efuse status write
espefuse_tools = 'espefuse.py -p'
espefuse_cmds_summary = 'summary'
espefuse_cmds_burn_efuse = 'burn_efuse'
espefuse_cmds_burn_key = 'burn_key'
espefuse_cmds_burn_key_file = 'flash_encryption'
espefuse_cmds_burn_key_file_name = 'burn_key.BLK1.bin'
espefuse_cmds_jtag_disable_1 = 'JTAG_DISABLE 1'
espefuse_cmds_encrypt_disable_1 = 'DISABLE_DL_ENCRYPT 1'
espefuse_cmds_decrypt_disable_1 = 'DISABLE_DL_DECRYPT 1'
espefuse_cmds_cache_disable_1 = 'DISABLE_DL_CACHE 1'
espefuse_cmds_flash_crypt_cnt_1 = 'FLASH_CRYPT_CNT 1'
espefuse_cmds_flash_crypt_config_15 = 'FLASH_CRYPT_CONFIG 15'
espefuse_cmds_write_protect_efuse = 'write_protect_efuse'
espefuse_cmds_flash_cnt = 'FLASH_CRYPT_CNT'

#file write

def input_serial_com():
    print("Please enter the device connection serial port name such as COM1")
    print("Type 'COM1' (all capitals) to continue.")
    sys.stdout.flush()  #required for Pythons which disable line buffering, ie mingw in mintty
    try:
        com_str = raw_input()  # raw_input renamed to input in Python 3
    except NameError:
        com_str = input()
    return com_str

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


def err_exit(ret,str):
    if ret != 0 :
        print("%s err exit" % str)
        input_file_com()
        sys.exit(ret)
    print("%s success" % str)

#need write efuse data string
def efuse_write_all(com_number):
    esptool_str = ('%s %s %s' % (espefuse_tools,com_number,espefuse_cmds_summary)) 
    print("%s ....." %esptool_str)
    ret = os.system(esptool_str)
    err_exit(ret,esptool_str)

    esptool_str = ('%s %s %s %s' % (espefuse_tools,com_number,espefuse_cmds_burn_efuse,espefuse_cmds_cache_disable_1)) 
    print("%s ....." %esptool_str)
    ret = os.system(esptool_str)
    err_exit(ret,esptool_str)

    esptool_str = ('%s %s %s %s' % (espefuse_tools,com_number,espefuse_cmds_burn_efuse,espefuse_cmds_jtag_disable_1)) 
    print("%s ....." %esptool_str)
    ret = os.system(esptool_str)
    err_exit(ret,esptool_str)

    esptool_str = ('%s %s %s %s' % (espefuse_tools,com_number,espefuse_cmds_burn_efuse,espefuse_cmds_encrypt_disable_1)) 
    print("%s ....." %esptool_str)
    ret = os.system(esptool_str)
    err_exit(ret,esptool_str)

    esptool_str = ('%s %s %s %s' % (espefuse_tools,com_number,espefuse_cmds_burn_efuse,espefuse_cmds_decrypt_disable_1)) 
    print("%s ....." %esptool_str)
    ret = os.system(esptool_str)
    err_exit(ret,esptool_str)

    esptool_str = ('%s %s %s %s' % (espefuse_tools,com_number,espefuse_cmds_burn_efuse,espefuse_cmds_flash_crypt_config_15)) 
    print("%s ....." %esptool_str)
    ret = os.system(esptool_str)
    err_exit(ret,esptool_str)

    esptool_str = ('%s %s %s %s' % (espefuse_tools,com_number,espefuse_cmds_burn_efuse,espefuse_cmds_flash_crypt_cnt_1)) 
    print("%s ....." %esptool_str)
    ret = os.system(esptool_str)
    err_exit(ret,esptool_str)

    esptool_str = ('%s %s %s %s' % (espefuse_tools,com_number,espefuse_cmds_write_protect_efuse,espefuse_cmds_flash_cnt)) 
    print("%s ....." %esptool_str)
    ret = os.system(esptool_str)
    err_exit(ret,esptool_str)

    esptool_str = ('%s %s %s %s %s' % (espefuse_tools,com_number,espefuse_cmds_burn_key,espefuse_cmds_burn_key_file,espefuse_cmds_burn_key_file_name)) 
    print("%s ....." %esptool_str)
    ret = os.system(esptool_str)
    err_exit(ret,esptool_str)

    esptool_str = ('%s %s %s' % (espefuse_tools,com_number,espefuse_cmds_summary)) 
    print("%s ....." %esptool_str)
    ret = os.system(esptool_str)
    err_exit(ret,esptool_str)
    print("..........eufuse all write sucess..............")

#need write file data string
def esp_file_write_all(com_number):
    esptool_str = ('esptool.py -p %s -b 460800 --before default_reset --after no_reset write_flash --flash_mode dio --flash_size detect --flash_freq 40m 0x1000 flash.4096.bin 0xF000 flash.61440.bin 0x15000 flash.86016.bin 0x20000 flash.131072.bin 0x3d8000 flash.4030464.bin' % com_number)
    print("%s ....." %esptool_str)
    ret = os.system(esptool_str)
    err_exit(ret,esptool_str)

def main(custom_commandline=None):
    com_number = input_serial_com()
    esp_file_write_all(com_number)
    print("..........eufuse file write sucess..............")
    efuse_write_all(com_number)
    input_sucess_com()

def _main():
    try:
        main()
    except esptool.FatalError as e:
        print('\ntool main a fatal error occurred: %s' % e)
        sys.exit(2)

if __name__ == '__main__':
    _main()
