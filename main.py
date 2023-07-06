import sys

from PyQt5.QtWidgets import QApplication

from Controller.terminalController import TerminalController
from Model.terminalModel import TerminalModel
from View.terminalView import TerminalView

if __name__ == '__main__':
    app = QApplication(sys.argv)
    terminal_model = TerminalModel()
    terminal_view = TerminalView()
    terminal_controller = TerminalController(terminal_model, terminal_view)
    terminal_controller.connect()
    sys.exit(app.exec_())
