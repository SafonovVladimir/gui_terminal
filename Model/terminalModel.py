import serial

from Utility.serialPortReader import SerialPortReader


class TerminalModel:
    def __init__(self):
        self.serial_port_reader = None

    def connect(self, port, baud_rate):
        try:
            self.serial_port_reader = SerialPortReader(port, baud_rate)
            return True
        except serial.SerialException as e:
            return str(e)

    def send_command(self, command):
        if self.serial_port_reader:
            self.serial_port_reader.serial_port.write(command.encode() + b"\r\n")
