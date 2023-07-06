import serial
from PyQt5.QtCore import QThread, pyqtSignal


class SerialPortReader(QThread):
    new_data_received = pyqtSignal(str)

    def __init__(self, port, baudrate):
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.serial_port = None
        self._is_running = True

    def run(self):
        self.serial_port = serial.Serial(self.port, self.baudrate)

        while self._is_running:
            data = self.serial_port.readline().strip().decode()
            if "HUB" in data:
                decoded_data = data[7:21] + data[29:]
                self.new_data_received.emit(decoded_data)
            else:
                self.new_data_received.emit(data.replace("\r", ""))
