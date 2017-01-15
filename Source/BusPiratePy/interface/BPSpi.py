#!/usr/bin/python3

from enum import Enum
from .BPBase import BPBase
from BusPiratePy.util.Logger import Logger
from BusPiratePy.BPConnection import BPConnection, BPMode

class BPSpi(BPBase):

    """Represents a SPI interface for the Bus Pirate"""

    def __init__(self, conn: BPConnection):
        """Class constructor"""
        super(BPSpi, self).__init__(conn)

        # Property Definitions
        self.__log = Logger.getlogger()
        """Class Logger"""
        self.RequiredMode = [BPMode.Spi]
        """Mode that is required for the interface to operate"""

    def Mode_Enable(self):
        """Switch the BusPirate to Spi Mode"""
        self._Switch_Mode(1, "SPI1", BPMode.Spi)

# TODO
