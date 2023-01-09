
class Neighborhood:
    types = ['Von_Neumann', 'Hexagonal_Random']

    def __init__(self, selected=0):
        self.selected = selected

    def getAll(self):
        return self.types

    def getSelected(self):
        return self.selected

    def getSelectedArray(self):
        if (self.selected == 0):
            return [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
        if (self.selected == 1):
            return [[[0, 1, 1], [1, 0, 1], [1, 1, 0]], [[1, 1, 0], [1, 0, 1], [0, 1, 1]]]
