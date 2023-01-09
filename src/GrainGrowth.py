from Boundary import Boundary
from Neighborhood import Neighborhood
from Cell import Cell
import random


class GrainGrowth(object):
    xCells = int()
    yCells = int()
    cellsArraySizeX = int()
    cellsArraySizeY = int()
    xStart = int()
    xEnd = int()
    yStart = int()
    yEnd = int()
    cellSize = float()
    finished = bool()
    cellsArray = []
    cellsArray2 = []
    neigborhood = []
    neigborhoodRandomPool = []
    cellsColorsMap = {}
    boundary = Boundary()
    neighborhood = Neighborhood()

    def __init__(self, xCells=0, yCells=0, cellSize=0):
        self.xCells = xCells
        self.yCells = yCells
        self.cellSize = cellSize
        self.cellsArraySizeX = xCells + 2
        self.cellsArraySizeY = yCells + 2
        self.xStart = 1
        self.xEnd = self.cellsArraySizeX - 1
        self.yStart = 1
        self.yEnd = self.cellsArraySizeY - 1
        self.cellsArray = [
            [0]*self.cellsArraySizeY for i in range(self.cellsArraySizeX)]
        self.cellsArray2 = [
            [0]*self.cellsArraySizeY for i in range(self.cellsArraySizeX)]
        for y in range(self.cellsArraySizeY):
            for x in range(self.cellsArraySizeX):
                self.cellsArray[y][x] = Cell(-1, '#', 0, y, x)
                self.cellsArray2[y][x] = Cell(-1, '#', 0, y, x)
        self.finished = False

    def copyEdgeCells(self):
        # horizontal
        x = self.xStart
        while x < self.xEnd:
            self.cellsArray[0][x].copyFrom(
                self.cellsArray[self.yEnd - 1][x])
            self.cellsArray[self.yEnd][x].copyFrom(
                self.cellsArray[1][x])
            x += 1
        # vertical
        y = self.yStart
        while y < self.yEnd:
            self.cellsArray[y][0].copyFrom(
                self.cellsArray[y][self.xEnd - 1])
            self.cellsArray[y][self.xEnd].copyFrom(
                self.cellsArray[y][1])
            y += 1
        # corners
        self.cellsArray[0][0].copyFrom(
            self.cellsArray[self.yEnd - 1][self.xEnd - 1])
        self.cellsArray[self.yEnd][0].copyFrom(
            self.cellsArray[1][self.xEnd - 1])
        self.cellsArray[0][self.xEnd].copyFrom(
            self.cellsArray[self.yEnd - 1][1])
        self.cellsArray[self.yEnd][self.xEnd].copyFrom(
            self.cellsArray[1][1])

    def setBoundary(self, boundary):
        self.boundary = boundary
        if boundary.getSelected == 0:
            x = 0
            while x < self.cellsArraySizeX:
                self.cellsArray[0][x].setAll(-1, -1, 0, y, x)
                self.cellsArray[self.yEnd][x].setAll(
                    -1, -1, 0, self.yEnd, x)
                x += 1

            y = 0
            while y < self.cellsArraySizeY:
                self.cellsArray[y][0].setAll(-1, -1, 0, y, x)
                self.cellsArray[y][self.xEnd].setAll(
                    -1, -1, 0, y, self.xEnd)
                y += 1

    def drawCell(self, canvas, y, x, color):
        if color == '#':
            return

        x0 = (x-1)*self.cellSize
        y0 = (y-1)*self.cellSize
        x1 = x0+self.cellSize
        y1 = y0+self.cellSize
        # remove old rectangle to increase performance
        oldRect = self.cellsArray[y][x].getRectangle()
        if oldRect != None:
            canvas.delete(oldRect)
        # create new rectangle
        newRect = canvas.create_rectangle(x0, y0, x1, y1, fill=color, width=0)
        self.cellsArray[y][x].setRectangle(newRect)

    def checkNeighborhood(self, yCell, xCell):
        maskMatrix = []
        if (self.neigborhoodRandomPool != None):
            maskMatrix = self.neigborhoodRandomPool[random.randint(
                0, len(self.neigborhoodRandomPool)-1)]
        else:
            maskMatrix = self.neigborhood

        y = 0
        x = 0
        neighborhoodColor = '#'
        updateCell = False
        neighborhoodMap = {}

        for yMask in range(3):
            for xMask in range(3):
                y = yCell - 1 + yMask
                x = xCell - 1 + xMask
                if maskMatrix[yMask][xMask] == 1 and self.cellsArray[y][x].getState() == 1:
                    updateCell = True
                    neighborhoodColor = self.cellsArray[y][x].getColor()
                    if neighborhoodColor in neighborhoodMap:
                        neighborhoodMap[neighborhoodColor] = neighborhoodMap[neighborhoodColor] + 1
                    else:
                        neighborhoodMap[neighborhoodColor] = 1

        if (updateCell):
            newCellColor = max(neighborhoodMap, key=neighborhoodMap.get)
            cellId = self.cellsColorsMap[newCellColor]
            return Cell(cellId, newCellColor, 1, yCell, xCell)
        else:
            return Cell(-1, '#', 0, yCell, xCell)

    def addNewCell(self, y, x, canvas):
        if self.cellsArray[y][x].getState() != 0:
            return False

        color = self.findNewColor(y, x)
        if color != None:
            if not self.cellsColorsMap:
                self.updateCell(y, x, color, 1, canvas)
                return True
            maxIDinMap = sorted(self.cellsColorsMap.values())[
                len(self.cellsColorsMap)-1]
            self.updateCell(y, x, color, maxIDinMap + 1, canvas)
            return True
        return False

    def findNewColor(self, y, x):
        maxTry = 100
        tryCount = 0
        color = "#"+("%06x" % random.randint(0, 16777215))
        if y >= 0 and y < self.cellsArraySizeY and x >= 0 and x < self.cellsArraySizeX and self.cellsArray[y][x].getState() == 0:
            if not self.cellsColorsMap:
                return color
            while (color in self.cellsColorsMap) and (tryCount < maxTry):
                color = "#"+("%06x" %
                             random.randint(0, 16777215))
                tryCount += 1
            return color
        return None

    def updateCell(self, y, x, color, id, canvas):
        self.cellsColorsMap[color] = id
        self.cellsArray[y][x].setAll(id, color, 1, y, x)
        self.cellsArray2[y][x].setAll(id, color, 1, y, x)
        self.drawCell(canvas, y, x, color)

    def setNeigborhood(self, neigborhood):
        if neigborhood.getSelected() == 1:
            self.neigborhoodRandomPool = neigborhood.getSelectedArray()
        else:
            self.neigborhood = neigborhood.getSelectedArray()
            self.neigborhoodRandomPool = None
        self.neighborhood = neigborhood

    def start(self, canvas):
        isEmptyCell = False
        if self.boundary.getSelected() == 1:
            self.copyEdgeCells()
        y = self.yStart
        while y < self.yEnd:
            x = self.xStart
            while x < self.xEnd:
                if self.cellsArray[y][x].getState() == 0:
                    isEmptyCell = True
                    self.cellsArray2[y][x] = self.checkNeighborhood(
                        y, x)
                    self.drawCell(canvas, y, x,
                                  self.cellsArray2[y][x].getColor())
                x += 1
            y += 1

        y = 0
        while y < self.cellsArraySizeY:
            x = 0
            while x < self.cellsArraySizeX:
                self.cellsArray[y][x].copyFrom(self.cellsArray2[y][x])
                x += 1
            y += 1

        self.finished = not isEmptyCell
        return not isEmptyCell

    def setDpCell(self, p_y, p_x, canvas, p_color):
        dPId = self.cellsArray[p_y][p_x].getId()
        # if send color, change cells color = DP
        if p_color == '#':
            color = self.cellsArray[p_y][p_x].getColor()
        else:
            color = p_color

        y = self.yStart
        while y < self.yEnd:
            x = self.xStart
            while x < self.xEnd:
                if self.cellsArray[y][x].getId() == dPId:
                    # Dp cell always has ID = 0 and state = 2
                    self.cellsArray[y][x].setAll(0, color, 2, y, x)
                    self.cellsArray2[y][x].setAll(0, color, 2, y, x)
                    self.drawCell(canvas, y, x, color)
                x += 1
            y += 1

        return True

    def removeDpCells(self, canvas):
        canvas.delete("all")
        self.cellsColorsMap.clear()
        self.finished = False
        # put initial values to all cells with state != 2 and draw the Dp one more time
        y = self.yStart
        while y < self.yEnd:
            x = self.xStart
            while x < self.xEnd:
                if self.cellsArray[y][x].getState() != 2:
                    self.cellsArray[y][x].setAll(-1, '#', 0, y, x)
                    self.cellsArray2[y][x].setAll(-1, '#', 0, y, x)
                else:
                    self.drawCell(
                        canvas, y, x, self.cellsArray2[y][x].getColor())
                x += 1
            y += 1

        return True

    def isFinished(self):
        return self.finished

    def getxCells(self):
        return self.xCells

    def getyCells(self):
        return self.yCells

    def getCellSize(self):
        return self.cellSize

    def getCellsArray(self):
        return self.cellsArray

    def getCellsArraySizeX(self):
        return self.cellsArraySizeX

    def getCellsArraySizeY(self):
        return self.cellsArraySizeY

    def getXStart(self):
        return self.xStart

    def getXEnd(self):
        return self.xEnd

    def getYStart(self):
        return self.yStart

    def getYEnd(self):
        return self.yEnd

    def getXCells(self):
        return self.xCells

    def getYCells(self):
        return self.yCells
