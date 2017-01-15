#!/usr/bin/python3

import time, serial
from enum import Enum
from BusPiratePy.util.Logger import Logger

class BPMode(Enum):
    Console = -1
    Uart = 1
    Uart_Bridged = 2
    I2c = 3
    Spi = 4
    OneWire = 5
    RawWire = 6
    BitBang = 7
    ADC = 8

class BPConnection(object):
    """
    This class represents a connection to the bus pirate
    it's effectively a wrapper around the serial port class
    """

    def __init__(self, port: serial.Serial = None, portname: str = "/dev/bus_pirate", speed = 115200, timeout = 1):

        # Property Definitions

        self.__log = Logger.getlogger()
        """Class Logger"""

        self.Mode = BPMode.Console
        """Mode of operation"""

        self.Attempts = 15
        """Number of attempts to make at establishing a connection"""

        self.Port = port
        """Serial Port to use"""
  
        self.MinDelay = 1
        """Minimum Delay"""

        if self.Port == None:
            self.Port = serial.Serial()
            self.Port.port = portname
            self.Port.baudrate = 115200
            self.Port.timeout = timeout

# Connection Functions

    def Open(self):
        """Open the serial port to the bus pirate"""
        if self.Port.is_open == True:
            raise Exception('Port is already open' % self.Port.port)
        try:
            self.Port.open()
        except serial.serialutil.SerialException:
            raise IOError('Could not open port %s' % self.Port.port)
        self.MinDelay = 1 / self.Port.baudrate

    def Close(self):
        """Close the serial port"""
        if self.Port.is_open == True:
            self.Port.close()

    @property
    def Connected(self):
        """If the serial port is open"""
        return self.Port.is_open

# Read Functions

# Note when reading, sometimes it's more reliable to specify a count / size of bytes to read
# This way the serial port code will wait until the number of bytes is available or the timeout occurs before returning the data
# This way you can avoid adding in waits before reads

    def Reset_Input(self):
        """Flush / Reset the input buffer"""
        self.Port.reset_input_buffer()

    def Read_Byte(self):
        """Read Bytes from the Serial Port"""
        data = self.Port.read(1)
        return data

    def Read_Bytes(self, size = 0):
        """Read Bytes from the Serial Port"""
        if size == 0: size = self.Port.inWaiting()
        data = self.Port.read(size)
        return data
 
    def Read_String(self, size = 0, encoding='UTF-8', errors='strict'):
        """Read a string from the Serial Port"""
        if size == 0: size = self.Port.inWaiting()
        data = self.Port.read(size)
        return data.decode(encoding = encoding, errors = errors)

    def Read_Response(self, expected = bytes([0x01])):
        """Read the response from the BusPirate"""
        data = self.Port.read(1)
        if data == expected: return True
        return False

# Write Functions

    def Reset_Output(self):
        """Flush / Reset the output buffer"""
        self.Port.reset_output_buffer()

        # delay is required in order to avoid this bug
        # http://dangerousprototypes.com/forum/viewtopic.php?f=4&t=4227

    def Write_Byte(self, byte, delay = True):
        """Write Byte to serial port"""
        self.Port.write(bytes([byte]))
        if delay == True: time.sleep(self.MinDelay * 10)

    def Write_Bytes(self, inputarr, delay = True):
        """Write Byte array to serial port"""
        self.Port.write(inputarr)
        if delay == True: time.sleep(self.MinDelay * 10)

    def Write_String(self, inputstr: str, encoding='UTF-8',errors='strict'):
        """Write a string to the Serial Port"""    
        data = inputstr.encode(encoding = encoding, errors = errors)
        self.Port.write(data)
        if delay == True: time.sleep(self.MinDelay * 10)

# Mode Functions

    def Reset(self):
        self.Mode_Console()
        self.Mode_Binary()

    def Mode_Binary(self):
        """Enter BitBang Mode, this also acts as a global restart to get the Buspirate into a known state"""
        if self.Connected == False:
            raise IOError("The serial port is disconnected")
        self.Reset_Input()

        for i in range(self.Attempts):

            for i in range(20):
                self.Write_Byte(0x00)
                if self.Port.inWaiting() > 0:
                    tmpbuffer = self.Read_String()
                    if tmpbuffer.startswith('BBIO'): break
                    
            self.Reset_Input()
            self.Write_Byte(0x00)
            if self.Read_String(5) == "BBIO1":
                self.Mode = BPMode.BitBang
                #TODO setup config registers for tracking
                #self.bp_config = 0x00      # configuration bits determine action of power sources and pullups
                #self.bp_port = 0x00        # out_port similar to ports in microcontrollers
                #self.bp_dir = 0x1F         # direction port similar to microchip microcontrollers.  (1) is input, (0) is output
                self.Reset_Input()
                return True
        
            # Failed to connect so try enter 10 times followed by a #
            for n in range(10):
                self.Write_Byte(0x0D)
            self.Write_Byte(ord('#'))
            self.Reset_Input()

        return False

    def Mode_Console(self):
        """This resets the BusPirate into console mode"""
        if self.Connected == False:
            raise IOError("The serial port is disconnected")
        self.Reset_Input()
        self.Reset_Output()
        self.Write_Byte(0x00)
        self.Write_Byte(0x0F)
        self.Mode = BPMode.Console
