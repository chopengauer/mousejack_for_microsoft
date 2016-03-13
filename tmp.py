#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import threading
import time
import operator

from RF24 import *
import RPi.GPIO as GPIO

import select
import tty
import termios

stat = {}

def checksum(p, ck_offset = 0):
    csum = 0
    for i in range(len(p)):
        csum = csum ^ p[i]
    return csum ^ ck_offset

address = [0xa97cd6796d, 0x5f359e5b53, 0xa97cd679cd, 0x5f359e7350]
address_index = 0
data_rate = [RF24_250KBPS, RF24_1MBPS, RF24_2MBPS]
data_rate_index = 0
crc = [0, RF24_CRC_8, RF24_CRC_16]
crc_index = 0
payload_size = 32
channel = 9
aack = False

radio = RF24(RPI_V2_GPIO_P1_22, RPI_V2_GPIO_P1_24, BCM2835_SPI_SPEED_8MHZ)
radio.begin()
radio.setChannel(70)
radio.setPALevel(RF24_PA_MAX)
radio.setAutoAck(False)
#radio.setAutoAck(True)
radio.setDataRate(RF24_2MBPS)
radio.setAddressWidth(5)
#radio.disableCRC()
radio.setCRCLength(RF24_CRC_16)
radio.setPayloadSize(20)
radio.printDetails()

radio.stopListening()
radio.openWritingPipe(address[0])

#    print hex(checksum(tmp[5:-1], 0x4a))
if 1:
    tmp = bytearray('4c044801781bcc200000787ffbff80000000003e'.decode('hex'))
    t00 = '4c04480178'
    t10 = '1b'
    t11 = '00'
    t20 = '20'
    t21 = '0000230000000000000000'
    crc = '3e'
#    4112005e1e aa28000000 2000400000 0000000e50
    '''
    r = t00 + '01'+ t11 + 'a40000787ffbff8000000000'
    r = bytearray(r.decode('hex'))
    crc = checksum(r[5:], 0x4a)
    r.append(crc)
    packet = r
    radio.write(packet)
    '''
    for j in range(0,136):
	#print j
	for i in range(28, 30):
	    r = t00 + ('%02x' % 3) + t11 + ('%02x' % j) + t21
	    #print r
	    #r = t00 + t10 + t11 + ('%02x' % j) + t21
	    r = bytearray(r.decode('hex'))
	    crc = checksum(r[5:], 0x4a)
	    r.append(crc)
	    packet = r
	    radio.write(packet)
	    time.sleep(0.01)
    #'''
