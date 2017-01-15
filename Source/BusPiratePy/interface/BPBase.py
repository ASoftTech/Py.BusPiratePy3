#!/usr/bin/python3

import time
from BusPiratePy.util.Logger import Logger
from BusPiratePy.BPConnection import BPConnection, BPMode

class BPBase:

    """Base class for interfaces used by the Bus Pirate"""

    def __init__(self, conn: BPConnection):
        """Class constructor"""

        # Property Definitions
        self._Conn = conn
        """Connection Class"""
        self.RequiredMode = [BPMode.Console]
        """Mode that is required for the interface to operate"""

# Delay Functions

    def _Delay_Factor(self, fac):
        """Delay based on a factor of the baud rate"""
        time.sleep(self._Conn.MinDelay * fac)

    def _Delay_Seconds(self, secs):
        """Delay in seconds"""
        time.sleep(secs)

# Connection Functions

    def _Check_Connected(self):
        """Check we're connected to a serial port"""
        if self._Conn.Connected == False:
            raise IOError("The serial port is disconnected")

# Mode Functions

    def _Check_Mode(self):
        """Check to make sure the mode is set correctly for the interface in use"""
        if self._Conn.Mode not in self.RequiredMode:
            raise ValueError("The current mode is not {0}".format(self.RequiredMode))

    def _Switch_Mode(self, modeid: int, response: str, mode: BPMode):
        """Switch Binary Modes"""

        # If the mode is Uart_Bridged then there's not much we can do
        if self._Conn.Mode == BPMode.Uart_Bridged:
            raise Exception("Unable to exit Uart Bridged Mode, unplug and replug the device to reset")

        # Make sure we're in Binary Mode
        if self._Conn.Mode == BPMode.Console:
            self._Conn.Mode_Binary()
            self._Delay_Factor(10)

        # Switch to whichever mode is selected
        self._Conn.Reset_Input()
        self._Conn.Reset_Output()
        self._Conn.Write_Byte(modeid)
        self._Delay_Factor(1000)
        reply = self._Conn.Read_String(len(response))
        if reply != response:
            raise Exception("Unable to change binary mode, expected: {0}, response: {1}".format(response, reply))
        self._Conn.Mode = mode
