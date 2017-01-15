#!/usr/bin/python3

# TODO
# 1. Test
# 2. Additional Congig settings
# 3. Read / Write to Uart

import time
from .BPBase import BPBase
from .config.BPUartConfig import BPUartConfig
from BusPiratePy.util.Logger import Logger
from BusPiratePy.BPConnection import BPConnection, BPMode

class BPUart(BPBase):
    """Represents a serial port Uart interface for the Bus Pirate"""

    def __init__(self, conn: BPConnection):
        """Class constructor"""
        super(BPUart, self).__init__(conn)

        # Property Definitions
        self.__log = Logger.getlogger()
        """Class Logger"""
        self.RequiredMode = [BPMode.Uart]
        """Mode that is required for the interface to operate"""
        self.Config = BPUartConfig(conn)
        """Configuration for the Port"""

    def Mode_Enable(self):
        """Switch the BusPirate to Uart Mode"""
        self._Switch_Mode(3, "ART1",  BPMode.Uart)

    def Rx_Enable(self, enable:bool):
        """Enable the receiving of data from the Uart Pins"""
        self._Check_Mode()
        if enable == True:
            self._Conn.Write_Byte(0b00000010)
        else:
            self._Conn.Write_Byte(0b00000011)

        # Sometimes after enabling the rx input a rouge 0x00 shows up in the input buffer which can affect the response
        self._Delay_Seconds(0.1)
        response = self._Conn.Read_Response()
        self._Conn.Reset_Input()
        return response

    def BridgeMode_Enable(self):
        """Enable Bridge mode for echoing serial in and out, a full reset is required to exit"""
        self._Check_Mode()
        self._Conn.Write_Byte(0b00001111)
        self._Delay_Seconds(0.1)
        self._Conn.Mode = BPMode.Uart_Bridged
        return self._Conn.Read_Response()
