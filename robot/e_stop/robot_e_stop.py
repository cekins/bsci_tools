#!/home/ekinsc/bsci-tools/robot/e_stop/.venv/bin/python3
"""Emergency stop script for robot"""
import serial
import time

from datetime import datetime

import robot

from serial.tools import list_ports

# PORTS
PID = 29987
VID = 6790

# SERIAL
BAUDRATE = 9600
WRITE_RATE = 0.2
ENCODING = 'utf-8'
TERMINATOR = '\r'.encode(ENCODING)
CONNECTION_MESSAGE = 'CONNECTED'.encode(ENCODING) + TERMINATOR
STOP_RESPONSE = 'STOP'.encode(ENCODING) + TERMINATOR

# ROBOT
HOSTNAME = '10.0.2.21'

# GET PORTS
ports = list_ports.comports()
for port in ports:
    if port.vid == VID and port.pid == PID:
        break
else:
    raise RuntimeError('No arduino found')

# CONNECT TO SERIAL
with serial.Serial(port.device, BAUDRATE) as con:
    with robot.GalilRobot(HOSTNAME) as rb:
        last_write_time = 0
        while True:
            if time.time() - last_write_time > WRITE_RATE:
                con.write(CONNECTION_MESSAGE)
                rb.send_command('WH')  # use query command to test if connection is maintained
            if con.in_waiting:
                if con.read_until(TERMINATOR) == STOP_RESPONSE:
                    rb.send_command('ST')
                    rb.send_command('IHT=-3')
                    rb.send_command('ST')
                    print(f'{datetime.now().strftime("%H:%M:%S")} STOPPED')
