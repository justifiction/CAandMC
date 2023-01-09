
class Cell(object):
    id = int()
    x = int()
    y = int()
    color = str()
    state = int()
    energy = float()

    def __init__(self, id=-1, color='#', state=-1, y=-1, x=-1, energy=0):
        self.id = id
        self.color = color
        self.state = state
        self.x = x
        self.y = y
        self.energy = energy
        self.rectangle = None

    def copyFrom(self, cell):
        self.id = cell.getId()
        self.color = cell.getColor()
        self.state = cell.getState()

    def setAll(self, id, color, state, y, x):
        self.id = id
        self.color = color
        self.state = state
        self.x = x
        self.y = y

    def getColor(self):
        return self.color

    def getState(self):
        return self.state

    def getId(self):
        return self.id

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getEnergy(self):
        return self.energy

    def setRectangle(self, rect):
        self.rectangle = rect

    def getRectangle(self):
        return self.rectangle

    def __str__(self):
        return '{'+str(self.y) + ',' + str(self.x) + ',' + str(self.state) + ',' + str(self.id) + ',' + self.color + '}'
