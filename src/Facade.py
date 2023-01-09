from GrainGrowth import GrainGrowth
from MonteCarlo import MonteCarlo
import random


class Facade(object):
    def __init__(self, yMax, xMax):
        self.xMax = xMax
        self.yMax = yMax
        self.grainGrowth = None
        self.monteCarlo = None
        self.isEnergyVis = False

    def initGrainGrowth(self, xCells, yCells, cellSize):
        if xCells <= 0 or xCells > self.xMax or yCells <= 0 or yCells > self.yMax:
            raise RuntimeError("Wrong Size!")
        self.grainGrowth = GrainGrowth(xCells, yCells, cellSize)

    def isGrainGrowth(self):
        return not self.grainGrowth == None

    def setNeigborhood(self, neighborhoodEnum):
        if self.grainGrowth == None:
            raise RuntimeError("Grain Growth is not initialized!")
        self.grainGrowth.setNeigborhood(neighborhoodEnum)

    def setBoundary(self, boundary):
        if self.grainGrowth == None:
            raise RuntimeError("Grain Growth is not initialized!")
        self.grainGrowth.setBoundary(boundary)



    def start(self, canvas):
        return self.grainGrowth.start(canvas)

    def setHomogeneusNucl(self, onXaxis, onYaxis, canvas):
        if onXaxis <= 0 or onXaxis > self.grainGrowth.getxCells() or onYaxis <= 0 or onYaxis > self.grainGrowth.getyCells():
            raise RuntimeError("Wrong Parameters!")
        xStep = int(self.grainGrowth.getxCells() / onXaxis)
        xstart = int(((self.grainGrowth.getxCells() - 1) -
                      xStep * (onXaxis - 1)) / 2)
        yStep = int(self.grainGrowth.getyCells() / onYaxis)
        ystart = int(((self.grainGrowth.getyCells() - 1) -
                      yStep * (onYaxis - 1)) / 2)

        for x in range(onXaxis):
            for y in range(onYaxis):
                self.grainGrowth.addNewCell(
                    (y * yStep) + ystart + 1, (x * xStep) + xstart + 1, canvas)

    def setRandomNucl(self, amount, maxIterationRandom, canvas):
        if amount < 0:
            raise RuntimeError("Nucleons amount must be > 0!")
        if amount > self.grainGrowth.getxCells():
            raise RuntimeError("Too many nucleons provided!")
        
        iteration = 0
        x = int()
        y = int()
        while amount > 0 and iteration < maxIterationRandom:
            x = random.randint(1, self.grainGrowth.getxCells())
            y = random.randint(1, self.grainGrowth.getyCells())
            if self.grainGrowth.addNewCell(y, x, canvas):
                amount -= 1
                iteration = 0
            else:
                iteration += 1
        return amount

    def getGrainGrowth(self):
        return self.grainGrowth

    def setDpCells(self, amount, maxIt, color, canvas):
        if amount < 0:
            raise RuntimeError("Nucleons amount must be > 0!")
        if amount > self.grainGrowth.getxCells():
            raise RuntimeError("Too many nucleons provided!")

        if (self.grainGrowth == None) or (not self.grainGrowth.isFinished()):
            return amount

        iteration = 0
        x = int()
        y = int()
        while amount > 0 and iteration < maxIt:
            x = random.randint(1, self.grainGrowth.getxCells())
            y = random.randint(1, self.grainGrowth.getyCells())
            if self.grainGrowth.setDpCell(y, x, canvas, color):
                amount -= 1
                iteration = 0
            else:
                iteration += 1
        return amount

    def removeDp(self, canvas):
        if (self.grainGrowth == None) or (not self.grainGrowth.isFinished()):
            return False

        return self.grainGrowth.removeDpCells(canvas)

# ------------------------------
# MONTE CARLO
    def initMonteCarlo(self, grainGrowth, iterations, kt):
        if (self.grainGrowth == None) or (not self.grainGrowth.isFinished()):
            raise RuntimeError("Grain growth must be finished!")
        if iterations <= 0 or iterations > 100 or kt < 0.1 or kt > 6:
            raise RuntimeError("Wrong amounts!")
        self.monteCarlo = MonteCarlo(grainGrowth, iterations, kt)

    def isMonteCarlo(self):
        return not self.monteCarlo == None

    def startMonteCarlo(self, canvas):
        return self.monteCarlo.start(canvas)

    def drawEnergy(self, canvas):
        if self.monteCarlo == None:
            return False

        # black scale in hex
        colorScale = ['#cccccc',
                      '#b3b3b3',
                      '#999999',
                      '#808080',
                      '#666666',
                      '#4d4d4d',
                      '#333333',
                      '#1a1a1a',
                      '#000000']

        for x in range(self.monteCarlo.getXCells()):
            for y in range(self.monteCarlo.getYCells()):
                energy = int(self.monteCarlo.getCellsArray()[y][x].getEnergy())
                if energy > 0:
                    if self.isEnergyVis:
                        self.monteCarlo.drawCell(
                            canvas, y, x, self.monteCarlo.getCellsArray()[y][x].getColor())
                    else:
                        self.monteCarlo.drawCell(
                            canvas, y, x, colorScale[energy])

        self.isEnergyVis = not self.isEnergyVis

        return True

    def setNeigborhoodMC(self, neighborhoodEnum):
        if self.monteCarlo == None:
            raise RuntimeError("Monte Carlo is not initialized!")
        self.monteCarlo.setNeigborhood(neighborhoodEnum)

    def setBoundaryMC(self, boundary):
        if self.grainGrowth == None:
            raise RuntimeError("Monte Carlo is not initialized!")
        self.monteCarlo.setBoundary(boundary)
