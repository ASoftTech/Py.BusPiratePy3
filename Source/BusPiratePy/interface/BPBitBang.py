#!/usr/bin/python3

from enum import Enum
from .BPBase import BPBase
from BusPiratePy.util.Logger import Logger
from BusPiratePy.BPConnection import BPConnection, BPMode

class BPBitBang(BPBase):

    """Represents a BitBang interface for the Bus Pirate"""

    def __init__(self, conn: BPConnection):
        """Class constructor"""
        super(BPBitBang, self).__init__(conn)

        # Property Definitions
        self.__log = Logger.getlogger()
        """Class Logger"""
        self.RequiredMode = [BPMode.BitBang]
        """Mode that is required for the interface to operate"""

    def Mode_Enable(self):
        """Switch the BusPirate to BitBang Mode"""
        self._Switch_Mode(0, "BBIO1", BPMode.BitBang)

# TODO
