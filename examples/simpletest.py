#!/usr/bin/python

# Author: Joe Gutting
# With use of Adafruit TMP007 library for Arduino, Adafruit_GPIO.I2C & BMP Library by Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Can enable debug output by uncommenting:
#import logging
#logging.basicConfig(level=logging.DEBUG)

import time
import TMP007.TMP007 as TMP007


# Default constructor will pick a default I2C bus.
#
# For the Raspberry Pi this means you should hook up to the only exposed I2C bus
# from the main GPIO header and the library will figure out the bus number based
# on the Pi's revision.
#
# For the Beaglebone Black the library will assume bus 1 by default, which is
# exposed with SCL = P9_19 and SDA = P9_20.

sensor = TMP007.TMP007()

# You can also optionally change the TMP007 mode to one of TMP007_CFG_1SAMPLE, TMP007_CFG_2SAMPLE,
# TMP007_CFG_4SAMPLE, TMP007_CFG_8SAMPLE, TMP007_CFG_16SAMPLE.  See the TMP007
# datasheet for more details on the meanings of each mode (accuracy and power
# consumption are primarily the differences).  The default mode is TMP007_CFG_16SAMPLE.
#sensor = TMP007.TMP007(mode=TMP007.TMP007_CFG_16SAMPLE)

print 'Press Ctrl + Z to cancel...'

while True:
        dieTempC = sensor.readDieTempC()
        objTempC = sensor.readObjTempC()
        sensorVolts = sensor.readVoltage()
        print 'Die Temp:        ' + str(dieTempC) + ' C'
        print 'Obj Temp:        ' + str(objTempC) + ' C'
        print 'Voltage:         ' + str(sensorVolts) + ' uV'

        # change depending on Config.  Default is TMP007_CFG_16SAMPLE.
        # Sleep time for other sampling rates:
        # TMP007_CFG_1SAMPLE    .26s
        # TMP007_CFG_2SAMPLE    .51s
        # TMP007_CFG_4SAMPLE    1.01s
        # TMP007_CFG_8SAMPLE    2.01s
        # TMP007_CFG_16SAMPLE   4.1s

        time.sleep(4.1)
