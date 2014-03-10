import datetime
import collections
import serial
import string
import sys
import time


### Settings

# Port for the ODBC connector
COM = '/dev/ttyUSB0'

### Helpers

def getspeed(ser):
    """ Helper to get the speed in KPH, using a pre-created serial connection.
    """
    # Code to send to get KPH
    HEX = '0D'

    # Result length in bytes
    RESULT_LEN = 17

    # prepare the outgoing request
    req = '01{0}'.format(HEX)

    # flush input buffer
    ser.flushInput()

    # send the request
    ser.write('{0}\r'.format(req))

    # read the data bytes
    data = ser.read(RESULT_LEN)

    # get the actual returned OBD info for the PID
    res = data.split(' ')[2:-1]

    # parse the result into a speed
    kph = ord(chr(int(res[0], 16)))

    return kph

def notify(text):
    """ Will become TTS notifications...
    """
    # Test using beeps - TTS later
    if text = 'pi 100 is loaded':
        for i in range(3):
            sys.stdout.write('\a')
            time.sleep(0.5)

if __name__ == '__main__':
    ### Hardware initialisation

    # Connect to the serial port
    ser = serial.Serial(COM, timeout=1, baudrate=9600, xonxoff=True)

    ### Configure the ODBC board

    # reset device
    ser.write('ATZ\r')
    time.sleep(5)

    # set timeout to 40ms
    ser.write('ATST 10\r')
    time.sleep(1)

    # set adaptive timing to aggressive
    ser.write('ATAT2\r')
    time.sleep(1)

    # Notify that loaded
    notify('pi 100 is loaded')
