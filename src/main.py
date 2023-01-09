
from Boundary import Boundary
from Facade import Facade
from Neighborhood import Neighborhood
from GUI import GUI

def main():
    yMax = 100
    xMax = 100
    neighborhood = Neighborhood(0)  # Von_Neumann
    boundary = Boundary(0)  # Absorbing
    xCells = 10
    yCells = 10
    cellSize = 2
    onXaxis = 2
    onYaxis = 2
    amount = 2
    MAX_ITERATION_RANDOM = 100
    canvas = 0  # TODO

    facade = Facade(yMax, xMax)
    facade.setParameters(
        xCells, yCells, cellSize, neighborhood, boundary)
    facade.setHomogeneusNucl(onXaxis, onYaxis, canvas)
   

    iterationCnt = 0
    while not facade.start(canvas):
        iterationCnt += 1
        resultArray = facade.getGrainGrowth().getCellsArray()
        print(resultArray)
        print(iterationCnt)

    GUI();


main()
