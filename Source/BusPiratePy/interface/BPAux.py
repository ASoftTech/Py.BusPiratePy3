#!/usr/bin/python3

# TODO Test

from enum import Enum
from .BPBase import BPBase
from BusPiratePy.util.Logger import Logger
from BusPiratePy.BPConnection import BPConnection, BPMode

class AuxPins(Enum):
    ChipSelect   = 0b00000001
    AuxPin       = 0b00000010
    Pullup       = 0b00000100
    PowerSupply  = 0b00001000


class BPAux(BPBase):

    """Represents the Aux pins associated with multiple interfaces such as pullup / ChipSelect"""

    def __init__(self, conn: BPConnection):
        """Class constructor"""
        super(BPAux, self).__init__(conn)

        # Property Definitions
        self.__log = Logger.getlogger()
        """Class Logger"""
        self.RequiredMode = [BPMode.Spi, BPMode.I2c, BPMode.Uart, BPMode.OneWire, BPMode.RawWire]
        """Mode that is required for the interface to operate"""
        self.AuxRegister = 0x00
        """Current State of the Aux Pins"""

    def Write(self):
        """Write the Aux Pin Settings to the Bus Pirate"""
        tmp1 = self.AuxRegister & 0b00001111
        tmp1 = tmp1 | 0b01000000
        self._Conn.Write_Byte(tmp1)
        #self._Delay_Seconds(0.1)
        return self._Conn.Read_Response()

# Aux Pin Setup

    @property
    def PowerSupply(self):
        """Enables the Power Supply output for the +5 / +3.3V Pins and used for the pullups"""
        if (self.AuxRegister & AuxPins.PowerSupply) > 0: return True
        return False

    @PowerSupply.setter
    def PowerSupply(self, value:bool):
        if value:
            self.AuxRegister = self.Config_Register | AuxPins.PowerSupply
        else:
            self.AuxRegister = self.Config_Register & ~AuxPins.PowerSupply

    @property
    def Pullup(self):
        """Enables the Puilup resistors for the pins"""
        if (self.AuxRegister & AuxPins.Pullup) > 0: return True
        return False

    @Pullup.setter
    def Pullup(self, value:bool):
        if value:
            self.AuxRegister = self.Config_Register | AuxPins.Pullup
        else:
            self.AuxRegister = self.Config_Register & ~AuxPins.Pullup

    @property
    def ChipSelect(self):
        """Enables the ChipSelect pin"""
        if (self.AuxRegister & AuxPins.ChipSelect) > 0: return True
        return False

    @ChipSelect.setter
    def ChipSelect(self, value:bool):
        if value:
            self.AuxRegister = self.Config_Register | AuxPins.ChipSelect
        else:
            self.AuxRegister = self.Config_Register & ~AuxPins.ChipSelect

    @property
    def AuxPin(self):
        """Enables the Aux pin"""
        if (self.AuxRegister & AuxPins.AuxPin) > 0: return True
        return False

    @AuxPin.setter
    def AuxPin(self, value:bool):
        if value:
            self.AuxRegister = self.Config_Register | AuxPins.AuxPin
        else:
            self.AuxRegister = self.Config_Register & ~AuxPins.AuxPin
