import sys
import serial
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, \
    QTextBrowser


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


class TerminalWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Minicom")
        self.resize(800, 600)

        # Create a central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a layout for the central widget
        layout = QVBoxLayout(central_widget)

        # Create labels, line edits, and button for port and baud rate
        port_label = QLabel("Port:")
        self.port_line_edit = QLineEdit()
        baud_rate_label = QLabel("Baud Rate:")
        self.baud_rate_line_edit = QLineEdit()
        connect_button = QPushButton("Connect")
        connect_button.clicked.connect(self.connect_button_clicked)

        # Create a text edit widget for displaying terminal output
        self.terminal_output = QTextBrowser(self)

        # Add widgets to the layout
        layout.addWidget(port_label)
        layout.addWidget(self.port_line_edit)
        layout.addWidget(baud_rate_label)
        layout.addWidget(self.baud_rate_line_edit)
        layout.addWidget(connect_button)
        layout.addWidget(self.terminal_output)

    def connect_button_clicked(self):
        port = self.port_line_edit.text()
        baud_rate = int(self.baud_rate_line_edit.text())

        try:
            self.terminal_output.append(f"Connected to {port} at {baud_rate} baud rate.")
            self.serial_port_reader = SerialPortReader(port, baud_rate)
            self.serial_port_reader.new_data_received.connect(self.update_logs)
            self.serial_port_reader.start()

        except serial.SerialException as e:
            self.terminal_output.append(f"Error: {str(e)}")

    def update_logs(self, data):
        self.terminal_output.append(data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    terminal_window = TerminalWindow()
    terminal_window.show()
    sys.exit(app.exec_())
