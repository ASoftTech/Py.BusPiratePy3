#!/usr/bin/python3

# TODO
# 1. Test  
# 2. Check the enum values for the baud rate  
# confirm the midi setting, and that 0b1010 = 115200, also what about other values?
# 2. Baud Rate Fixed
# 3. Baud Rate Adj

from enum import Enum
from BusPiratePy.interface.BPBase import BPBase
from BusPiratePy.util.Logger import Logger
from BusPiratePy.BPConnection import BPConnection, BPMode

class SPortBits(Enum):
    InversePolarity  = 0b00000001
    StopBits         = 0b00000010
    PinOutput        = 0b00010000

class DataParityBits(Enum):
    Data8_ParityNone = 0b00000000
    Data8_ParityEven = 0b00000100
    Data8_ParityOdd  = 0b00001000
    Data9_ParityNone = 0b00001100

class BaudRate(Enum):
    B300 = 0b0000
    B1200 = 0b0001
    B2400 = 0b0010
    B4800 = 0b0011
    B9600 = 0b0100
    B19200 = 0b0101
    B31250 = 0b0110
    B38400 = 0b0111
    B57600 = 0b1000
    B115200 = 0b1010
    MIDI = 0b0110

class BPUartConfig(BPBase):
    """Represents a serial port Uart configuration for the Bus Pirate"""

    def __init__(self, parent: BPBase):
        """Class constructor"""

        # Property Definitions
        self.__log = Logger.getlogger()
        """Class Logger"""
        self.Parent = parent
        """Parent Serial Port class"""
        self.RequiredMode = [BPMode.Uart]
        """Mode that is required for the interface to operate"""
        self.SerialRegister = 0x00
        """Configuration Bits for the Uart"""

    def Write(self):
        """Write the Serial Port Settings to the Bus Pirate"""
        tmp1 = self.SerialRegister & 0b00011111
        tmp1 = tmp1 | 0b10000000
        self._Conn.Write_Byte(tmp1)
        #self._Delay_Seconds(0.1)
        return self._Conn.Read_Response()

# Uart Configuration Options


    @property
    def InversePolarity(self):
        """This affects if a 0 translates to a Gnd voltage level or Positive / High Impedence
           Note with older firmwares only the Rx Inbound pin is inverted
           http://dangerousprototypes.com/forum/viewtopic.php?f=4&t=4427"""
        if (self.SerialRegister & SPortBits.InversePolarity) > 0: return True
        return False

    @InversePolarity.setter
    def InversePolarity(self, value:bool):
        if value:
            self.SerialRegister = self.SerialRegister | SPortBits.InversePolarity
        else:
            self.SerialRegister = self.SerialRegister & ~SPortBits.InversePolarity


    @property
    def StopBits(self):
        """The number of stop bits to use (default is 1)"""
        if (self.SerialRegister & SPortBits.StopBits) > 0: return 2
        return 1

    @StopBits.setter
    def StopBits(self, value:int):
        if value < 1 or value > 2:
            raise ValueError("Number of stop bits can only be 1 or 2")
        if value != 1:
            self.SerialRegister = self.SerialRegister | SPortBits.StopBits
        else:
            self.SerialRegister = self.SerialRegister & ~SPortBits.StopBits


    @property
    def PinOutput(self):
        """If to use Pin Output, False = HiZ, True = 3.3V"""
        if (self.SerialRegister & SPortBits.PinOutput) > 0: return True
        return False

    @PinOutput.setter
    def PinOutput(self, value:bool):
        if value:
            self.SerialRegister = self.SerialRegister | SPortBits.PinOutput
        else:
            self.SerialRegister = self.SerialRegister & ~SPortBits.PinOutput


    @property
    def DataParity(self):
        """Set the number of Data bits and Parity"""
        reg = self.SerialRegister & 0b00001100
        ret = DataParityBits(reg)
        return ret

    @DataParity.setter
    def DataParity(self, value:DataParityBits):
        reg = self.SerialRegister & ~(0b00001100)
        reg = reg | value
