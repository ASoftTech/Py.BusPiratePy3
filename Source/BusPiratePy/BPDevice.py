#!/usr/bin/python3

import serial
from BusPiratePy.util.Logger import Logger
from BusPiratePy.BPConnection import BPConnection

from BusPiratePy.interface.BPBitBang import BPBitBang
from BusPiratePy.interface.BPUart import BPUart
from BusPiratePy.interface.BPI2c import BPI2c
from BusPiratePy.interface.BPSpi import BPSpi
from BusPiratePy.interface.BPOneWire import BPOneWire
from BusPiratePy.interface.BPRawWire import BPRawWire
from BusPiratePy.interface.BPAux import BPAux

class BPDevice(object):

    """Represents a container for a single bus pirate device"""

    def __init__(self, conn: BPConnection = None, port: serial.Serial = None, portname: str = "/dev/bus_pirate", speed = 115200, timeout = 1):
        """Class Constructor"""

        # Property Definitions
        self.__log = Logger.getlogger()
        """Class Logger"""

        # Conection
        self.Connection = conn
        if self.Connection == None:
            self.Connection = BPConnection(port, portname, speed, timeout)

        # Interfaces
        self.BitBang = BPBitBang(self.Connection)
        """BitBang Interface"""
        self.Uart = BPUart(self.Connection)
        """Uart used for Serial I/O"""
        self.I2c = BPI2c(self.Connection)
        """I2c Interface"""
        self.Spi = BPSpi(self.Connection)
        """Spi Interface"""
        self.OneWire = BPOneWire(self.Connection)
        """OneWire Interface"""
        self.RawWire = BPRawWire(self.Connection)
        """RawWire Interface"""
        self.Aux = BPAux(self.Connection)
        """Aux Pins (pullup / power supply)"""

    # Wrapper Code

    def Open(self):
        self.Connection.Open()

    def Close(self):
        self.Connection.Close()

    @property
    def Connected(self):
        return self.Connection.Connected
