# This server runs on Pi, sends Pi's your 4 arguments from the vcgencmds, sent as Json object.

# details of the Pi's vcgencmds - https://www.tomshardware.com/how-to/raspberry-pi-benchmark-vcgencmd
# more vcgens on Pi 4, https://forums.raspberrypi.com/viewtopic.php?t=245733
# more of these at https://www.nicm.dev/vcgencmd/

import socket
import os, time
import json

s = socket.socket()
host = '' 
port = 5000
s.bind((host, port))
s.listen(5)


def measure_temp():
    t = os.popen('vcgencmd measure_temp').readline()
    temp = float(t.replace("temp=","").replace("'C\n",""))
    return temp

def measure_volts_core():
    v = os.popen('vcgencmd measure_volts core').readline()
    volts = float(v.replace("volt=", "").replace("volts=", "").replace("V\n", "").strip())
    return volts

def measure_volts_sdram_i():
    vsd = os.popen('vcgencmd measure_volts sdram_p').readline()
    vsdvolts = float(vsd.replace("volt=", "").replace("volts=", "").replace("V\n", "").strip())
    return vsdvolts

def memory_arm():
    ma = os.popen('vcgencmd get_mem arm').readline()
    ma2 = float(ma.replace("arm=","").replace("M\n",""))
    return ma2

def clock_frequency_arm():
    cfa = os.popen('vcgencmd measure_clock arm').readline()
    cfa2 = float(cfa.replace("frequency(48)=",""))
    return cfa2


while True:
    try:
        c, addr = s.accept()
        print ('Got connection from',addr)
        data = (
            f"\nTemperature: {measure_temp()}, "
            f"\nVoltage Core: {measure_volts_core()}, "
            f"\nVoltage SDRAM: {measure_volts_sdram_i()}, "
            f"\nMemory ARM: {memory_arm()}, "
            f"\nClock Frequency ARM: {clock_frequency_arm()}"
        )
        res = data.encode('utf-8')
        c.send(res) 
        c.close() 
    except KeyboardInterrupt:
        print("\nServer shutting down...")
        s.close()
        break
