class TerminalController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def connect(self):
        self.view.show()
