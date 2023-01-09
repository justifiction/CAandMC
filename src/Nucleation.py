class Nucleation:
    types = ['Homogeneus', 'Random']

    def __init__(self, selected=0):
        self.selected = selected

    def getAll(self):
        return self.types

    def getSelected(self):
        return self.selected
