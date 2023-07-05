import sys
import serial
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextBrowser


class SerialPortReader(QThread):
    new_data_received = pyqtSignal(str)

    def __init__(self, port, baudrate):
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.serial_port = None

    def run(self):
        self.serial_port = serial.Serial(self.port, self.baudrate)

        while True:
            data = self.serial_port.readline().strip().decode()
            decoded_data = data[7:21] + data[34:]
            self.new_data_received.emit(decoded_data)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Minicom")
        self.resize(800, 600)
        self.text_browser = QTextBrowser(self)
        self.setCentralWidget(self.text_browser)

        self.serial_port_reader = SerialPortReader("/dev/ttyUSB0", 115200)
        self.serial_port_reader.new_data_received.connect(self.update_logs)
        self.serial_port_reader.start()

    def update_logs(self, data):
        self.text_browser.append(data)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    # window.showFullScreen()
    window.show()
    sys.exit(app.exec())
