import view
import model

class Controller():
    def __init__(self):
        self.view = view.View()
        self.model = model.NetDataModel()
