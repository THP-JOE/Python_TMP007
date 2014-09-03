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

import logging
import time

import Adafruit_GPIO.I2C as I2C

# registers
TMP007_VOBJ             = 0x00
TMP007_TDIE             = 0x01
TMP007_CONFIG           = 0x02
TMP007_TOBJ             = 0x03
TMP007_STATUS           = 0x04
TMP007_STATMASK         = 0x05

# configure bytes
TMP007_CFG_RESET        = 0x8000
TMP007_CFG_MODEON       = 0x1000
TMP007_CFG_1SAMPLE      = 0x0000
TMP007_CFG_2SAMPLE      = 0x0200
TMP007_CFG_4SAMPLE      = 0x0400
TMP007_CFG_8SAMPLE      = 0x0600
TMP007_CFG_16SAMPLE     = 0x0800
TMP007_CFG_ALERTEN      = 0x0100
TMP007_CFG_ALERTF       = 0x0080
TMP007_CFG_TRANSC       = 0x0040

# interrupt configure
TMP007_STAT_ALERTEN     = 0x8000
TMP007_STAT_CRTEN       = 0x4000

# I2C address and device ID
TMP007_I2CADDR          = 0x40
TMP007_DEVID            = 0x1F


class TMP007(object):
        def __init__(self, mode=TMP007_CFG_16SAMPLE, address=TMP007_I2CADDR,
                                                         busnum=I2C.get_default_bus()):

                self._logger = logging.getLogger('TMP007')

                # Check that mode is valid.
                if mode not in [TMP007_CFG_1SAMPLE, TMP007_CFG_2SAMPLE, TMP007_CFG_4SAMPLE, TMP007_CFG_8SAMPLE, TMP007_CFG_16SAMPLE]:
                        raise ValueError('Unexpected mode value {0}.  Set mode to one of TMP007_CFG_1SAMPLE, TMP007_CFG_2SAMPLE, TMP007_CFG_4SAMPLE, TMP007_CFG_8SAMPLE or TMP007_CFG_16SAMPLE'.format(mode))
                self._mode = mode
                # Create I2C device.
                self._device = I2C.Device(address, busnum)
                # Load calibration values.
                self._load_calibration()

        # load calibration to sensor
        def _load_calibration(self):
                #load calibration               
                self._device.write16(TMP007_CONFIG, I2C.reverseByteOrder(TMP007_CFG_MODEON | TMP007_CFG_ALERTEN | TMP007_CFG_TRANSC | self._mode))
                #set alert status
                self._device.write16(TMP007_STATMASK, I2C.reverseByteOrder(TMP007_STAT_ALERTEN |TMP007_STAT_CRTEN))

        # read Die Temp in C
        def readDieTempC(self):
                raw = self._device.readU16BE(TMP007_TDIE)
                v = raw/4
                v *= 0.03125
                raw >>= 2
                Tdie = raw
                Tdie *= 0.03125 # convert to celsius
                self._logger.debug('Die temperature {0} C'.format(Tdie))
                return Tdie

        # read Obj Temp in C
        def readObjTempC(self):
                raw = self._device.readU16BE(TMP007_TOBJ)
                raw >>=2
                Tobj = raw
                Tobj *= 0.03125 # convert to celsius
                self._logger.debug('Obj temperature {0} C'.format(Tobj))
                return Tobj

        # read voltage
        def readVoltage(self):
                raw = self._device.readU16BE(TMP007_VOBJ);
                raw *= 156.25 # convert to nV
                raw /= 1000 # convert to uV
                self._logger.debug('Voltage {0} uV'.format(raw))
                return raw

