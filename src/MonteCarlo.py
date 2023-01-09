import math
from Boundary import Boundary
from Neighborhood import Neighborhood
from Cell import Cell
from GrainGrowth import GrainGrowth
import random


class MonteCarlo:
    iterations = int()
    iterationNow = int()
    kt = float()

    xCells = int()
    yCells = int()
    cellSize = float()
    cellsArray = []
    cellsArraySizeX = int()
    cellsArraySizeY = int()
    xStart = int()
    xEnd = int()
    yStart = int()
    yEnd = int()
    finished = bool()
    neigborhood = []
    neigborhoodRandomPool = []
    boundary = Boundary()
    neighborhood = Neighborhood()
    cellsList = []

    def cellsArray2DToList(self, cellsArray, xStart, xEnd, yStart, yEnd):
        cellsList = []
        y = yStart
        while y < yEnd:
            x = xStart
            while x < xEnd:
                if cellsArray[y][x].getState() == 1:
                    cellsList.append(cellsArray[y][x])
                x += 1
            y += 1
        return cellsList

    def __init__(self, grainGrowth=None, iterations=0, kt=0):
     
        self.iterations = iterations
        self.kt = kt
        self.xCells = grainGrowth.getXCells()
        self.yCells = grainGrowth.getYCells()
        self.cellSize = grainGrowth.getCellSize()
        self.cellsArray = grainGrowth.getCellsArray()
        self.cellsArraySizeX = grainGrowth.getCellsArraySizeX()
        self.cellsArraySizeY = grainGrowth.getCellsArraySizeY()
        self.xStart = grainGrowth.getXStart()
        self.xEnd = grainGrowth.getXEnd()
        self.yStart = grainGrowth.getYStart()
        self.yEnd = grainGrowth.getYEnd()
        self.iterationNow = 0
        self.finished = False
        self.cellsList = self.cellsArray2DToList(
            self.cellsArray, self.xStart, self.xEnd, self.yStart, self.yEnd)

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
        oldRect = self.cellsArray[y][x].getRectangle()
        if oldRect != None:
            canvas.delete(oldRect)
        newRect = canvas.create_rectangle(x0, y0, x1, y1, fill=color, width=0)
        self.cellsArray[y][x].setRectangle(newRect)

    def checkNeighborhoodMonteCarlo(self, cell, cellsArray):
        maskMatrix = []
        if (self.neigborhoodRandomPool != None):
            maskMatrix = self.neigborhoodRandomPool[random.randint(
                0, len(self.neigborhoodRandomPool)-1)]
        else:
            maskMatrix = self.neigborhood

        y = 0
        x = 0
        neighborhoodCellsList = []
        for yMask in range(3):
            for xMask in range(3):
                y = cell.getY() - 1 + yMask
                x = cell.getX() - 1 + xMask
                if maskMatrix[yMask][xMask] == 1 and self.cellsArray[y][x].getState() == 1:
                    neighborhoodCellsList.append(cellsArray[y][x])

        return neighborhoodCellsList

    def computeEnergy(self, cell, neighborhood_cells_list):
        energy = 0
        for c in neighborhood_cells_list:
            if c.id != cell.getId():
                energy += 1
        return energy

    def setNeigborhood(self, neigborhood):
        if neigborhood.getSelected() == 1:
            self.neigborhoodRandomPool = neigborhood.getSelectedArray()
        else:
            self.neigborhood = neigborhood.getSelectedArray()
            self.neigborhoodRandomPool = None
        self.neighborhood = neigborhood

    def start(self, canvas):
        if self.iterationNow >= self.iterations:
            return True

        if self.boundary.getSelected() == 1:
            self.copyEdgeCells()

        listCopy = self.cellsList.copy()
        cellIndex = int()
        neighborhoodCellIndex = int()
        oldEnergy = float()
        newEnergy = float()
        neighborhoodCellsList = []
        neigborhoodRandomCell = []
        isOnlyOneGrain = True
        id = listCopy[0].getId()

        while len(listCopy) > 0:
            # get random cell form list
            cellIndex = random.randint(0, len(listCopy) - 1)
            cell = listCopy[cellIndex]
            # get all cell's neighbors
            neighborhoodCellsList = self.checkNeighborhoodMonteCarlo(
                cell, self.cellsArray)

            # calc energy now
            oldEnergy = self.computeEnergy(cell, neighborhoodCellsList)
            self.cellsArray[cell.getY()][cell.getX()] = Cell(
                cell.getId(), cell.getColor(), 1, cell.getY(), cell.getX(), oldEnergy)
            # get random neighbor
            neighborhoodCellIndex = random.randint(
                0, len(neighborhoodCellsList) - 1)
            neigborhoodRandomCell = neighborhoodCellsList[neighborhoodCellIndex]
            # calc new energy
            newEnergy = self.computeEnergy(
                neigborhoodRandomCell, neighborhoodCellsList)
            deltaEnergy = newEnergy - oldEnergy
            if deltaEnergy <= 0 or (random.uniform(0, 1) <= math.exp(((-1)*deltaEnergy) / self.kt)):
                # set new energy
                newCell = Cell(neigborhoodRandomCell.getId(
                ), neigborhoodRandomCell.color, 1, cell.getY(), cell.getX(), newEnergy)
                self.cellsArray[newCell.getY()][newCell.getX()] = newCell
                self.drawCell(canvas, newCell.getY(), newCell.getX(),
                              newCell.getColor())

            if cell.getId() != id:
                isOnlyOneGrain = False
            # remove cell from list to not take it again
            del listCopy[cellIndex]

        self.iterationNow += 1
        return isOnlyOneGrain

    def getXCells(self):
        return self.xCells

    def getYCells(self):
        return self.yCells

    def getCellsArray(self):
        return self.cellsArray
