#!/usr/bin/python3

from enum import Enum
from .BPBase import BPBase
from BusPiratePy.util.Logger import Logger
from BusPiratePy.BPConnection import BPConnection, BPMode

class BPOneWire(BPBase):

    """Represents a OneWire interface for the Bus Pirate"""

    def __init__(self, conn: BPConnection):
        """Class constructor"""
        super(BPOneWire, self).__init__(conn)

        # Property Definitions
        self.__log = Logger.getlogger()
        """Class Logger"""
        self.RequiredMode = [BPMode.OneWire]
        """Mode that is required for the interface to operate"""

    def Mode_Enable(self):
        """Switch the BusPirate to OneWire Mode"""
        self._Switch_Mode(4, "1W01", BPMode.OneWire)

# TODO
