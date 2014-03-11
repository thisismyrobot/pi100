import os
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
    """ TTS notifications
    """
    os.system('echo "{}" | festival --tts'.format(text))

def record(text):
    with open('log.txt', 'a') as f:
        f.write('{}\n'.format(text))


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
    notify('pi 100 loaded')

    # Main loop
    lastspeed = -1
    launchtime = None
    while True:
        # Get current speed
        speed = getspeed(ser)

        # If just stopped, arm for launch
        if speed == 0 and lastspeed > 0:
            notify('Armed for launch')

        # If just launched but not hit 100 yet
        elif lastspeed == 0 and speed > 0:
            launchtime = time.time()
            notify('Launch recorded')

        # If just crossed 100 from a launch
        elif launchtime is not None and speed >= 100:
            endtime = time.time()
            duration = round(endtime - launchtime, 3)
            notify('Zero to one hundred recorded at {} seconds'.format(duration))
            record('0-100: {}'.format(duration))

            # Reset
            launchtime = None

        # If not hitting 100 in 20 seconds...
        elif launchtime is not None and time.time() - launchtime > 20:
            notify('Cancelling launch timer')
            launchtime = None

        lastspeed = speed
