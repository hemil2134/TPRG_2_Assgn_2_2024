'''
TPRG 2131 Fall 2024 Assignment 2.
Dec, 2024
Hemil Prajapati (100942152).
This program is strictly my own work. Any material
beyond course learning materials that is taken from
the Web or other sources is properly cited, giving.
credit to the original author(s).
'''

# This server runs on Pi, sends Pi's your 4 arguments from the vcgencmds, sent as Json object.

# details of the Pi's vcgencmds - https://www.tomshardware.com/how-to/raspberry-pi-benchmark-vcgencmd
# more vcgens on Pi 4, https://forums.raspberrypi.com/viewtopic.php?t=245733
# more of these at https://www.nicm.dev/vcgencmd/

import socket
import os, time
import json

# Create a socket to listen for client connections
s = socket.socket()
host = '' # Server's IP address
port = 5000  # Port number for the server
s.bind((host, port))
s.listen(5)

# Function to get the Pi's temperature
def measure_temp():
    t = os.popen('vcgencmd measure_temp').readline() #gets from the os, using vcgencmd - the core-temperature
    temp = float(t.replace("temp=","").replace("'C\n",""))
    return temp

# Function to get the Pi's core voltage
def measure_volts_core():
    v = os.popen('vcgencmd measure_volts core').readline()
    volts = float(v.replace("volt=", "").replace("volts=", "").replace("V\n", "").strip())
    return volts

# Function to get the Pi's SDRAM voltage
def measure_volts_sdram_i():
    vsd = os.popen('vcgencmd measure_volts sdram_p').readline()
    vsdvolts = float(vsd.replace("volt=", "").replace("volts=", "").replace("V\n", "").strip())
    return vsdvolts

# Function to get the amount of memory available for the ARM CPU
def memory_arm():
    ma = os.popen('vcgencmd get_mem arm').readline()
    ma2 = float(ma.replace("arm=","").replace("M\n",""))
    return ma2

# Function to get the clock speed of the ARM CPU
def clock_frequency_arm():
    cfa = os.popen('vcgencmd measure_clock arm').readline()
    cfa2 = float(cfa.replace("frequency(48)=",""))
    return cfa2

# Main server loop
while True:
    try:
        # Wait for a client to connect
        c, addr = s.accept()
        print ('Got connection from',addr)
         # Create a string with all the collected data
        data = (
            f"\nTemperature: {measure_temp()}, "
            f"\nVoltage Core: {measure_volts_core()}, "
            f"\nVoltage SDRAM: {measure_volts_sdram_i()}, "
            f"\nMemory ARM: {memory_arm()}, "
            f"\nClock Frequency ARM: {clock_frequency_arm()}"
        )
        # Encode the data as bytes and send it to the client
        res = data.encode('utf-8')
        c.send(res) 
        c.close() # Close the connection with the client
    except KeyboardInterrupt:
        # Stop the server when Ctrl+C is pressed
        print("\nServer shutting down...")
        s.close()
        break
