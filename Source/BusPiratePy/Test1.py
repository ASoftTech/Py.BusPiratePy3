#!/usr/bin/python3

from BusPiratePy.BPDevice import BPDevice

class Test1(object):

    def main(self):
        dev1 = BPDevice(portname = "COM6")
        dev1.Open()
        dev1.Uart.Mode_Enable()
        x1 = dev1.Uart.Rx_Enable(True)
        x1 = dev1.Uart.Rx_Enable(False)
        dev1.Close()

if __name__ == "__main__":
    Test1().main()
