import serial
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton, QTextBrowser

from Utility.serialPortReader import SerialPortReader


class TerminalView(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Minicom")
        self.resize(1600, 1200)

        # Create a central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a layout for the central widget
        layout = QVBoxLayout(central_widget)

        # Create labels, line edits, and button for port and baud rate
        self.input = QLineEdit(self)
        port_label = QLabel("Port:")
        self.port_line_edit = QLineEdit()
        baud_rate_label = QLabel("Baud Rate:")
        self.baud_rate_line_edit = QLineEdit()
        connect_button = QPushButton("Connect")
        connect_button.clicked.connect(self.connect_button_clicked)
        self.input.returnPressed.connect(self.send_command)

        # Create a text edit widget for displaying terminal output
        self.terminal_output = QTextBrowser(self)

        # Add widgets to the layout
        layout.addWidget(port_label)
        layout.addWidget(self.port_line_edit)
        layout.addWidget(baud_rate_label)
        layout.addWidget(self.baud_rate_line_edit)
        layout.addWidget(connect_button)
        layout.addWidget(self.terminal_output)
        layout.addWidget(self.input)

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

    def send_command(self):
        command = self.input.text()
        self.serial_port_reader.serial_port.write(command.encode() + b"\r\n")
        self.terminal_output.append(f"> {command}")
        self.input.clear()
