#!/usr/bin/python3

from enum import Enum
from .BPBase import BPBase
from BusPiratePy.util.Logger import Logger
from BusPiratePy.BPConnection import BPConnection, BPMode

class BPI2c(BPBase):

    """Represents a I2c interface for the Bus Pirate"""

    def __init__(self, conn: BPConnection):
        """Class constructor"""
        super(BPI2c, self).__init__(conn)

        # Property Definitions
        self.__log = Logger.getlogger()
        """Class Logger"""
        self.RequiredMode = [BPMode.I2c]
        """Mode that is required for the interface to operate"""

    def Mode_Enable(self):
        """Switch the BusPirate to I2c Mode"""
        self._Switch_Mode(2, "I2C1", BPMode.I2c)

# TODO