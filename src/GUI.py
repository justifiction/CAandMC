import tkinter as tk
from tkinter import messagebox

from Boundary import Boundary
from Facade import Facade
from Neighborhood import Neighborhood
from Nucleation import Nucleation


class GUI(object):
    def __init__(self):

        # * GUI constants
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 600
        self.MENU_WIDTH = 200
        self.MENU_HEIGHT = 600
        self.CANVAS_WIDTH = self.WINDOW_WIDTH - self.MENU_WIDTH
        self.CANVAS_HEIGHT = 600
        self.WINDOW_TITLE = "CA & MC"
        self.root = tk.Tk()
        self.buttons_frame = tk.Frame(self.root)
        # *  CA params
        self.facade = Facade(self.CANVAS_WIDTH, self.CANVAS_HEIGHT)
        self.boundary = Boundary()
        self.neighborhood = Neighborhood()
        self.nucleation = Nucleation()
        self.DP_COLOR = '#FF0000'  # RED
        self.EMPTY_CELL_COLOR = '#FFFFFF'  # WHITE

        self.root.geometry(str(self.WINDOW_WIDTH) +
                           "x" + str(self.WINDOW_HEIGHT))
        #set window color
        self.root.configure(bg='#D8BFD8')
        self.root.title(self.WINDOW_TITLE)
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)

     
        # *init entry vars
        self.dPRndAm = tk.StringVar()
        self.dPRndAm.set('3')
        self.dPSubRbValue = tk.IntVar()
        self.dPSubRbValue.set(1)  # init with 1 option
        self.homoAmountX=tk.StringVar()
        self.homoAmountX.set('2')
        self.homoAmountY=tk.StringVar()
        self.homoAmountY.set('2')
        self.randomAmount=tk.StringVar()
        self.randomAmount.set('25')
        self.sizeX=tk.StringVar()
        self.sizeX.set('100')
        self.sizeY=tk.StringVar()
        self.sizeY.set('100')
        self.iterationsValue=tk.StringVar()
        self.iterationsValue.set('5')
        self.ktValue=tk.StringVar()
        self.ktValue.set('1.2')
        # * Layout
        #       ------------------------------------
        #       |         |                        |
        #       |         |                        |
        #       |         |                        |
        #       |         |                        |
        #       |  Menu   |         Canvas         |
        #       |         |                        |
        #       |         |                        |
        #       |         |                        |
        #       |         |                        |
        #       -----------------------------------

        # left menu self.root!
        self.menuFrame = tk.Frame(
            self.root, width=self.WINDOW_WIDTH, bg='#D8BFD8', height=self.MENU_HEIGHT)
        self.menuFrame.grid(row=0, column=0)
        # right canvas self.root!
        self.canvas = tk.Canvas(
            self.root, bg=self.EMPTY_CELL_COLOR, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT)
        self.canvas.grid(row=0, column=1)

        # * buttons
        self.nucleationLabel = tk.Label(self.menuFrame, bg='#D8BFD8',text="Nucleation", font=( 
            'Arial', 10))
        self.nucleationLabel.pack(fill='x', pady=0)

        self.btnHomo = tk.Button(self.menuFrame, text="Homogeneus", font=(
            'Arial', 10), bg="White", command=self.btnHomoAction)
        self.btnHomo.pack(fill='x', pady=10)
        # frame
        self.homogeneusFrame = tk.Frame(self.menuFrame)
        self.homogeneusFrame.columnconfigure(0, weight=1)
        self.homogeneusFrame.columnconfigure(1, weight=1)
        self.homogeneusFrame.pack(fill='x', pady=0)
        self.homogeneusFrame.configure(bg='#D8BFD8')


        self.homogeneusXLabel = tk.Label(self.homogeneusFrame,text = "Amount on X axis ")
        self.homogeneusXLabel.grid(row=1, column=0)
        self.inputXHomogeneus = tk.Entry(self.homogeneusFrame, font=('Arial', 10), state= 'disabled',textvariable=self.homoAmountX)
        self.inputXHomogeneus.grid(row=1, column=1)
        self.homogeneusYLabel = tk.Label(self.homogeneusFrame,text = "Amount on Y axis ")
        self.homogeneusYLabel.grid(row=1, column=3)
        self.inputYHomogeneus = tk.Entry(self.homogeneusFrame, font=('Arial', 10), state= 'disabled',textvariable=self.homoAmountY)
        self.inputYHomogeneus.grid(row=1, column=4)

        self.btnRandom = tk.Button(self.menuFrame, text="Random", font=(
            'Arial', 10), bg="White", command=self.btnRandomAction)
        self.btnRandom.pack(fill='x', pady=10)
   # frame
        self.randomFrame = tk.Frame(self.menuFrame)
        self.randomFrame.columnconfigure(0, weight=1)
        self.randomFrame.columnconfigure(1, weight=1)
        self.randomFrame.pack(fill='x', pady=0)
        self.randomFrame.configure(bg='#D8BFD8')

        self.randomLabel = tk.Label(self.randomFrame,text = "Amount ")
        self.randomLabel.grid(row=1, column=0)
        self.inputRandom = tk.Entry(self.randomFrame, font=('Arial', 10), state= 'disabled',textvariable=self.randomAmount)
        #self.inputXHomogeneus.pack(fill='x', pady=10)
        self.inputRandom.grid(row=1, column=1)

        self.boundaryLabel = tk.Label(self.menuFrame, bg='#D8BFD8',text="Boundary conditions", font=( 
            'Arial', 10))
        self.boundaryLabel.pack(fill='x', pady=0)

        self.btnPeriodic = tk.Button(self.menuFrame, text="Periodic", font=(
            'Arial', 10), bg="White", state= 'disabled',command=self.btnPeriodicAction)
        self.btnPeriodic.pack(fill='x', pady=10)

        self.btnAbsorbing = tk.Button(self.menuFrame, text="Absorbing", font=(
            'Arial', 10), bg="White", state= 'disabled',command=self.btnAbsorbingAction)
        self.btnAbsorbing.pack(fill='x', pady=10)

        self.neighborhoodLabel = tk.Label(self.menuFrame, bg='#D8BFD8',text="Neighborhood", font=( 
            'Arial', 10))
        self.neighborhoodLabel.pack(fill='x', pady=0)

        self.btnVonNeumann = tk.Button(self.menuFrame, text="Von Neumann", font=(
            'Arial', 10), bg="White", state= 'disabled',command=self.btnVonNeumannAction)
        self.btnVonNeumann.pack(fill='x', pady=10)

        self.btnHexRandom = tk.Button(self.menuFrame, text="Hex-Random", font=(
            'Arial', 10), bg="White", state= 'disabled',command=self.btnHexRandomAction)
        self.btnHexRandom.pack(fill='x', pady=10)

        # * Dual Phase
        # label
        self.dPLabel = tk.Label(self.menuFrame, bg='#E6E6FA',text="Dual Phase", font=( 
            'Arial', 10))
        self.dPLabel.pack(fill='x', pady=0)
        # frame
        self.dPFrame = tk.Frame(self.menuFrame)
        self.dPFrame.columnconfigure(0, weight=1)
        self.dPFrame.columnconfigure(1, weight=1)
        self.dPFrame.pack(fill='x', pady=0)
        self.dPFrame.configure(bg='#E6E6FA')
        # TODO center radio buttons
        # RadioButtons
        self.dPRadioBtn = tk.Radiobutton(self.dPFrame,
                                         text="DP", bg='#E6E6FA',
                                         variable=self.dPSubRbValue,
                                         value=1,state= 'disabled',
                                         font=(
                                             'Arial', 10))
        self.dPRadioBtn.grid(row=0, column=0)
        self.subRadioBtn = tk.Radiobutton(self.dPFrame,
                                          text="SUB", bg='#E6E6FA',
                                          variable=self.dPSubRbValue,
                                          value=2,state= 'disabled',
                                          font=(
                                              'Arial', 10))
        self.subRadioBtn.grid(row=0, column=1)
        # entry
        self.dPEntry = tk.Entry(self.dPFrame, font=(
            'Arial', 10), state= 'disabled',textvariable=self.dPRndAm)
        self.dPEntry.grid(row=1, column=1)
        # rnd btn
        self.dPRndBtn = tk.Button(self.dPFrame, text="Random", font=(
            'Arial', 10), bg="White",state= 'disabled', command=self.btnDpRndAction)
        self.dPRndBtn.grid(row=1, column=2, ipadx=10)
        # # remove btn
        self.dPRemoveBtn = tk.Button(self.dPFrame, state= 'disabled',text="Remove rest cells", font=(
            'Arial', 10), bg="White", command=self.btnDpRemoveAction)
        self.dPRemoveBtn.grid(row=2, columnspan=2)

        # frame
        self.sizeFrame = tk.Frame(self.menuFrame)
        self.sizeFrame.columnconfigure(0, weight=1)
        self.sizeFrame.columnconfigure(1, weight=1)
        self.sizeFrame.pack(fill='x', pady=0)
        self.sizeFrame.configure(bg='#D8BFD8')

        self.sizeLabel = tk.Label(self.sizeFrame,text = "Size ")
        self.sizeLabel.grid(row=0, column=0)
        self.sizeXLabel = tk.Label(self.sizeFrame,text = "x ")
        self.sizeXLabel.grid(row=1, column=0)
        self.inputXSize = tk.Entry(self.sizeFrame, font=('Arial', 10), textvariable=self.sizeX)
        self.inputXSize.grid(row=1, column=1)
        self.sizeYLabel = tk.Label(self.sizeFrame,text = "y ")
        self.sizeYLabel.grid(row=1, column=3)
        self.inputYSize = tk.Entry(self.sizeFrame, font=('Arial', 10), textvariable=self.sizeY)
        self.inputYSize.grid(row=1, column=4)

        self.btnSet = tk.Button(self.menuFrame, text="Set", font=(
            'Arial', 10), bg="White", state= 'disabled',command=self.btnSetAction)
        self.btnSet.pack(fill='x', pady=10)

        self.btnStart = tk.Button(self.menuFrame, text="Start", font=(
            'Arial', 10), bg="White", state= 'disabled',command=self.btnStartAction)
        self.btnStart.pack(fill='x', pady=10)
# frame
        self.monteCarloFrame = tk.Frame(self.menuFrame)
        self.monteCarloFrame.columnconfigure(0, weight=1)
        self.monteCarloFrame.columnconfigure(1, weight=1)
        self.monteCarloFrame.pack(fill='x', pady=0)
        self.monteCarloFrame.configure(bg='#D8BFD8')

        self.sizeLabel = tk.Label(self.monteCarloFrame,text = "Monte Carlo ")
        self.sizeLabel.grid(row=0, column=0)
        self.iterationsLabel = tk.Label(self.monteCarloFrame,text = "iterations ")
        self.iterationsLabel.grid(row=1, column=0)
        self.inputIterations = tk.Entry(self.monteCarloFrame, font=('Arial', 10),state= 'disabled', textvariable=self.iterationsValue)
        self.inputIterations.grid(row=1, column=1)
        self.inputKtLabel = tk.Label(self.monteCarloFrame,text = "kt ")
        self.inputKtLabel.grid(row=1, column=3)
        self.inputKt = tk.Entry(self.monteCarloFrame, font=('Arial', 10), state= 'disabled',textvariable=self.ktValue)
        self.inputKt.grid(row=1, column=4)

        self.btnMonteCarlo = tk.Button(self.menuFrame, text="Monte Carlo", font=(
            'Arial', 10), bg="White", state= 'disabled',command=self.btnMonteCarloAction)
        self.btnMonteCarlo.pack(fill='x', pady=10)
        self.btnEnergy = tk.Button(self.menuFrame, state= 'disabled',text="Energy", font=(
            'Arial', 10), bg="White", command=self.btnEnergy)
        self.btnEnergy.pack(fill='x', pady=10)

        self.root.mainloop()
        

    # * buttons actions
    def btnHomoAction(self):
        self.nucleation = Nucleation(0)
        self.btnHomo.configure(bg="grey")
        self.btnRandom.configure(bg="White")
        self.inputRandom.configure(state= 'disabled')
        self.inputXHomogeneus.configure(state= 'normal')
        self.inputYHomogeneus.configure(state= 'normal')
        self.btnAbsorbing.configure(state= 'normal')
        self.btnPeriodic.configure(state= 'normal')

    def btnRandomAction(self):
        self.nucleation = Nucleation(1)
        self.btnRandom.configure(bg="grey")
        self.btnHomo.configure(bg="White")
        self.inputRandom.configure(state= 'normal')
        self.inputXHomogeneus.configure(state= 'disabled')
        self.inputYHomogeneus.configure(state= 'disabled')
        self.btnAbsorbing.configure(state= 'normal')
        self.btnPeriodic.configure(state= 'normal')

    def btnPeriodicAction(self):
        self.boundary = Boundary(1)
        self.btnPeriodic.configure(bg="grey")
        self.btnAbsorbing.configure(bg="White")
        self.btnVonNeumann.configure(state= 'normal')
        self.btnHexRandom.configure(state= 'normal')

    def btnAbsorbingAction(self):
        self.boundary = Boundary(0)
        self.btnAbsorbing.configure(bg="grey")
        self.btnPeriodic.configure(bg="White")
        self.btnVonNeumann.configure(state= 'normal')
        self.btnHexRandom.configure(state= 'normal')

    def btnVonNeumannAction(self):
        self.neighborhood = Neighborhood(0)
        self.btnVonNeumann.configure(bg="grey")
        self.btnHexRandom.configure(bg="White")
        self.btnSet.configure(state= 'normal')

    def btnHexRandomAction(self):
        self.neighborhood = Neighborhood(1)
        self.btnHexRandom.configure(bg="grey")
        self.btnVonNeumann.configure(bg="White")
        self.btnSet.configure(state= 'normal')

    def btnDpRndAction(self):
        # TODO validate amount to integer only and > 0
        try:
            self.btnEnergy.configure(state='disabled')
            self.btnMonteCarlo.configure(state='disabled')
            self.btnHomo.configure(state='normal')
            self.btnRandom.configure(state='normal')
            amount = int(self.dPRndAm.get())
            maxIt = 300

            opt = self.dPSubRbValue.get()
            if opt == 1:
                resAmount = self.facade.setDpCells(
                    amount, maxIt, self.DP_COLOR, self.canvas)
            else:
                resAmount = self.facade.setDpCells(
                    amount, maxIt, '#', self.canvas)
            self.dPRemoveBtn.configure(state= 'normal')

            messagebox.showinfo(
                title="Info", message=str(resAmount))
        except ValueError:
            messagebox.showinfo(
                    title="Error", message="Input is not an integer! Provide it again")
        except RuntimeError as e:
            messagebox.showinfo(title="Error", message=(e))

    def btnDpRemoveAction(self):
        res = self.facade.removeDp(self.canvas)
        self.btnSet.configure(state= 'normal')
        #self.btnStart.configure(state= 'normal')

    def btnSetAction(self):
        try:
            MAX_ITERATION_RANDOM = 100
            xCells = int(self.sizeX.get())
            yCells = int(self.sizeY.get())
            onXaxis = int(self.homoAmountX.get())
            onYaxis = int(self.homoAmountY.get())
            amount = int(self.randomAmount.get())
            

            # calc cell size
            if xCells > yCells:
                cellSize = int(self.CANVAS_WIDTH/xCells)
            else:
                cellSize = int(self.CANVAS_HEIGHT/yCells)

            if not self.facade.isGrainGrowth():
                self.facade.initGrainGrowth(xCells, yCells, cellSize)

            self.facade.setNeigborhood(self.neighborhood)
            self.facade.setBoundary(self.boundary)

            # create nucleons
            if self.nucleation.getSelected() == 0:
                self.facade.setHomogeneusNucl(onXaxis, onYaxis, self.canvas)
            elif self.nucleation.getSelected() == 1:
                self.facade.setRandomNucl(
                    amount, MAX_ITERATION_RANDOM, self.canvas)
            self.btnStart.configure(state= 'normal')
            self.inputYSize.configure(state= 'disabled')
            self.inputXSize.configure(state= 'disabled')
        except ValueError:
            messagebox.showinfo(
                    title="Error", message="Input is not an integer! Provide it again")
        except RuntimeError as e:
            messagebox.showinfo(title="Error", message=(e))
            raise 

    def btnStartAction(self):
        self.btnSet.configure(state= 'disabled')
        self.btnStart.configure(state= 'disabled')
        self.btnHexRandom.configure(state= 'disabled')
        self.btnVonNeumann.configure(state= 'disabled')
        self.btnPeriodic.configure(state= 'disabled')
        self.btnAbsorbing.configure(state= 'disabled')
        self.btnHomo.configure(state= 'disabled')
        self.btnRandom.configure(state= 'disabled')
        self.inputRandom.configure(state= 'disabled')
        self.inputXHomogeneus.configure(state= 'disabled')
        self.inputYHomogeneus.configure(state= 'disabled')
        while True:
            isFinished = self.facade.start(self.canvas)
            self.root.update()
            if isFinished:
                messagebox.showinfo(
                    title="Info", message="Grain growth finished!")
                self.btnMonteCarlo.configure(state= 'normal')
                self.dPRadioBtn.configure(state= 'normal')
                self.subRadioBtn.configure(state= 'normal')
                self.dPEntry.configure(state= 'normal')
                self.dPRndBtn.configure(state= 'normal')
                self.inputIterations.configure(state= 'normal')
                self.inputKt.configure(state= 'normal')
                break

    def btnMonteCarloAction(self):
        try:
            iterations = int(self.iterationsValue.get())#10
            kt =float(self.ktValue.get())# 1

            if not self.facade.isMonteCarlo():
                self.facade.initMonteCarlo(
                    self.facade.getGrainGrowth(), iterations, kt)

            self.facade.setNeigborhoodMC(self.neighborhood)
            self.facade.setBoundaryMC(self.boundary)

            while True:
                isFinished = self.facade.startMonteCarlo(self.canvas)
                self.root.update()
                if isFinished:
                    messagebox.showinfo(
                        title="Info", message="MonteCarlo finished!")
                    self.btnEnergy.configure(state='normal')
                    break
        except ValueError:
            messagebox.showinfo(
                    title="Error", message="Iterations must be integer type and kt float 0.1-6! Provide it again")
        except RuntimeError as e:
            messagebox.showinfo(title="Error", message=(e))

    def btnEnergy(self):
        self.facade.drawEnergy(self.canvas)
        self.root.update()
        


GUI()
