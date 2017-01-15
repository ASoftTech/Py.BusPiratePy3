#!/usr/bin/python3

from enum import Enum
from .BPBase import BPBase
from BusPiratePy.util.Logger import Logger
from BusPiratePy.BPConnection import BPConnection, BPMode

class BPRawWire(BPBase):

    """Represents a RawWire interface for the Bus Pirate"""

    def __init__(self, conn: BPConnection):
        """Class constructor"""
        super(BPRawWire, self).__init__(conn)

        # Property Definitions
        self.__log = Logger.getlogger()
        """Class Logger"""
        self.RequiredMode = [BPMode.RawWire]
        """Mode that is required for the interface to operate"""

    def Mode_Enable(self):
        """Switch the BusPirate to RawWire Mode"""
        self._Switch_Mode(5, "RAW1", BPMode.RawWire)

# TODO
