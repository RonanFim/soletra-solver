from tkinter import *
from tkinter import filedialog as fd
import time
from SoletraSolver import SoletraSolver
from KeyboardController import KeyboardController

# ============== Constants ======================
WIDTH = 625
HEIGHT = 300
TITLE = "Soletra Solver"
BGCOLOR = "#79b7c7"
SINGLE = 1
MULTI = 2


class SoletraSolverGUI:

    # ============== Private Variables ==============
    __DEBUG = False
    __root = None
    __solver = None


    # ============== Constructor ==============
    def __init__(self, debug=False) -> None:
        self.__root = Tk()
        self.__root.geometry(str(WIDTH) + 'x' + str(HEIGHT))
        self.__root.minsize(WIDTH, HEIGHT)
        self.__root.maxsize(WIDTH, HEIGHT)
        self.__root.title(TITLE)
        self.__DEBUG = debug
        self.__solver = None
        self.__CreateElements()
        self.__ConfigGrids()
        self.__Customize()


    # ============ Private Methods ============
        
    def __CreateFrames(self) -> None:
        self.__fTopRight = Frame(self.__root)
        self.__fLeft     = Frame(self.__root)
        self.__fBotRight = Frame(self.__root)
        self.__fDictPath = Frame(self.__fTopRight)
        self.__fSelAlgor = Frame(self.__fBotRight)
        self.__fButtons  = Frame(self.__fBotRight)
    
    def __CreateLabels(self) -> None:
        self.__lCentral    = Label(self.__fTopRight, text="Letras Centrais:")
        self.__lAux        = Label(self.__fTopRight, text="Letras Auxiliares:")
        self.__lNumChars   = Label(self.__fTopRight, text="Núm. de Caracteres:")
        self.__lAlgorithm  = Label(self.__fSelAlgor, text="Selecione o Algoritmo:")
        self.__lDictPath   = Label(self.__fDictPath, text="Path do arquivo de dicionário:")
        self.__lMessages   = Label(self.__root, text="Status: ")
    
    def __CreateTexts(self) -> None:
        self.__tCentral    = Text(self.__fTopRight, height= 1, width= 25)
        self.__tAux        = Text(self.__fTopRight, height= 1, width= 25)
        self.__tNumChars   = Text(self.__fTopRight, height= 1, width= 5)
        self.__tDictFile   = Text(self.__fDictPath, height= 1, width= 25)
        self.__tFinalWords = Text(self.__fLeft, height= 13, width= 25)
    
    def __CreateButtons(self) -> None:
        self.__bDictFile = Button(self.__fDictPath, text= "Selecionar Arquivo...", command=self.__SelectDictButtonFunc)
        self.__bGenerate = Button(self.__fButtons, text= "Iniciar", command=self.__StartButtonFunc)
        self.__bStop     = Button(self.__fButtons, text= "Parar", command=self.__StopButtonFunc)
        self.__bType     = Button(self.__fButtons, text= "Digitar Palavras", command=self.__TypeButtonFunc)

    def __CreateRadioButtons(self) -> None:
        self.__rbOption = IntVar()
        self.__rbSingleProc = Radiobutton(self.__fSelAlgor, text= "Single Process", variable=self.__rbOption, value=SINGLE)
        self.__rbMultiProc  = Radiobutton(self.__fSelAlgor, text= "Multi Process", variable=self.__rbOption, value=MULTI)

    def __CreateElements(self) -> None:
        self.__CreateFrames()
        self.__CreateLabels()
        self.__CreateTexts()
        self.__CreateButtons()
        self.__CreateRadioButtons()
    
    def __ConfigGridDictPath(self) -> None:
        self.__lDictPath.grid(row= 0, column= 0, sticky=W, columnspan=3)
        self.__bDictFile.grid(row= 1, column= 0, sticky=W)
        self.__tDictFile.grid(row= 1, column= 1, sticky=W, columnspan=2, padx=15)
    
    def __ConfigGridSelectAlg(self) -> None:
        self.__lAlgorithm.grid(row= 0, column= 0, sticky=W)
        self.__rbSingleProc.grid(row= 1, column= 0, sticky=W, padx= 10)
        self.__rbMultiProc.grid(row= 2, column= 0, sticky=W, padx= 10)
    
    def __ConfigGridButtons(self) -> None:
        self.__bGenerate.grid(row= 0, column= 0)
        self.__bStop.grid(row= 0, column= 1)
        self.__bType.grid(row= 1, column= 0, columnspan=2, padx= 10, pady= 10)
    
    def __ConfigGridTopRight(self) -> None:
        self.__lCentral.grid(row= 0, column= 0, sticky= W)
        self.__lAux.grid(row= 1, column= 0, sticky= W)
        self.__lNumChars.grid(row= 2, column= 0, sticky= W)
        self.__tCentral.grid(row= 0, column= 1, sticky= W)
        self.__tAux.grid(row= 1, column= 1, sticky= W)
        self.__tNumChars.grid(row= 2, column= 1, sticky= W)
        self.__fDictPath.grid(row= 3, column= 0, columnspan=3, pady=5)
    
    def __ConfigGridLeft(self) -> None:
        self.__tFinalWords.grid(row= 1, column= 0)
    
    def __ConfigGridBotRight(self) -> None:
        self.__fButtons.grid(row= 0, column= 0)
        self.__fSelAlgor.grid(row= 0, column= 1)
    
    def __ConfigGridFinal(self) -> None:
        self.__fLeft.grid(row= 0, column= 0, rowspan=2, padx= 15, pady= 10)
        self.__fTopRight.grid(row= 0, column= 1, padx= 15, pady= 10)
        self.__fBotRight.grid(row= 1, column= 1, padx= 5, pady= 5)
        self.__lMessages.grid(row= 2, column= 0, columnspan=2, sticky=SW)

    def __ConfigGrids(self) -> None:
        self.__ConfigGridDictPath()
        self.__ConfigGridSelectAlg()
        self.__ConfigGridButtons()
        self.__ConfigGridTopRight()
        self.__ConfigGridLeft()
        self.__ConfigGridBotRight()
        self.__ConfigGridFinal()
    
    def __ChangeBackgroundColor(self, color, container) -> None:
        container.config(bg=color)
        for child in container.winfo_children():
            if child.winfo_children():
                # child has children, go through its children
                self.__ChangeBackgroundColor(color, child)
            elif type(child) is Entry:
                child.config(highlightbackground=color)
                child.config(fg=color, insertbackground=color)
            elif type(child) is Frame:
                child.config(bg=color)
            elif type(child) is Label:
                child.config(bg=color)
            elif type(child) is Radiobutton:
                child.config(bg=color)
    
    def __ChangeFont(self, container):
        for child in container.winfo_children():
            if child.winfo_children():
                # child has children, go through its children
                self.__ChangeFont(child)
            elif type(child) is Label:
                child.configure(font=("Calibri", 12))
            elif type(child) is Radiobutton:
                child.configure(font=("Calibri", 12))
            elif type(child) is Text:
                child.configure(font=("Calibri", 12))
            elif type(child) is Button:
                child.configure(font=("Verdana", 14))

    def __Customize(self) -> None:
        # Change bg color of all elements
        self.__ChangeBackgroundColor(BGCOLOR, self.__root)
        # bGenerate.configure(bg="green")
        # Change fonts
        self.__ChangeFont(self.__root)
        self.__bDictFile.configure(font=("Verdana", 9))
        self.__lMessages.configure(foreground="White")

    def __CreateSolverFromPath(self, filepath: str) -> None:
        fileSplit = filepath.split('/')
        print(fileSplit)
        filename = fileSplit[-1].split('.')[0]
        print(filename)
        path = ''.join(str(item)+'\\' for item in fileSplit[:-1])
        print(path)
        self.__solver = SoletraSolver(filename, path)
    
    def __FillBoxWithList(self, wordsList: list) -> None:
        self.__tFinalWords.delete(1.0, END)
        for word in wordsList:
            self.__tFinalWords.insert(END, word + '\n')

    def __SetStatusMsg(self, message: str, color: str) -> None:
        self.__lMessages.configure(foreground=color, text=message)
        self.__root.update()
        
    
    # Debug print
    def __Log(self, log):
        if self.__DEBUG:
            print(log)
    

    # =========== CallBack Functions ===========

    def __SelectDictButtonFunc(self):
            filetypes = (
                ('dict files', '*.dic'),
                ('dict files', '*.aff'),
                ('All files', '*.*')
            )

            filepath = fd.askopenfilename(
                title='Selecione arquivo de dicionário',
                initialdir='/',
                filetypes=filetypes
            )
            print(filepath)
            self.__tDictFile.delete(1.0, END)
            self.__tDictFile.insert(INSERT, filepath)
            

    def __StartButtonFunc(self):
        path = self.__tDictFile.get(1.0, END)
        print(path)
        self.__CreateSolverFromPath(path)
        if self.__solver == None:
            print("nao tem solver!")
            return
        option = self.__rbOption.get()
        if option not in [SINGLE, MULTI]:
            print("Algoritmo não selecionado!")
            return
        centralLet = self.__tCentral.get(1.0, END)
        auxLet = self.__tAux.get(1.0, END)
        try:
            numChars = int(self.__tNumChars.get(1.0, END))
            print(numChars)
        except ValueError:
            print("Número de Caracteres incorreto!")
            return
        if numChars < 3:
            print("Número de Caracteres menor que 3")
            return
        self.__SetStatusMsg("Status: Encontrando palavras...", "Yellow")
        self.__solver.SetCentralLetters(centralLet)
        self.__solver.SetSideLetters(auxLet)
        wordsFound = []
        if option == SINGLE:
            wordsFound = self.__solver.FindCombinations(numChars)
        elif option == MULTI:
            wordsFound = self.__solver.FindCombinationsMP(numChars)
        self.__FillBoxWithList(wordsFound)
        self.__SetStatusMsg("Status: Finalizado!", "Green")

    def __StopButtonFunc(self):
        pass

    def __TypeButtonFunc(self):
        self.__SetStatusMsg("Status: Digitando palavras...", "Yellow")
        typer = KeyboardController()
        words = self.__tFinalWords.get(1.0, END)
        wordsList = list(filter(None, words.split('\n')))
        typer.TypeWords(wordsList)
        self.__SetStatusMsg("Status: Finalizado!", "Green")


    # ============ Public Methods ==============
        
    def MainLoop(self):
        self.__root.mainloop()
