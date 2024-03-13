import itertools
from hunspell import Hunspell
from unidecode import unidecode
import time
import multiprocessing as mp
from pynput.keyboard import Key, Controller


class SoletraSolver:

    # ============== Private Variables ==============
    __dictName = ""
    __dictPath = ""
    __centralLetters = None
    __sideLetters = None
    __DEBUG = False
    __keyboardController = None



    # ============== Constructor ==============
    def __init__(self, dictName:str, dictPath:str, debug=False) -> None:
        self.__dictName = dictName
        self.__dictPath = dictPath
        self.__DEBUG = debug
        self.__keyboardController = Controller()



    # ============== Public Methods ==============

    # Salve the central letters in list
    def SetCentralLetters(self, centrals) -> None:
        self.__centralLetters = [character.lower() for character in centrals if character.isalpha()]

   
    # Salve the side letters in list
    def SetSideLetters(self, sides) -> None:
        self.__sideLetters = [character.lower() for character in sides if character.isalpha()]


    # Return central letters list
    def GetCentralLetters(self) -> list:
        return self.__centralLetters


    # Return side letters list
    def GetSideLetters(self) -> list:
        return self.__sideLetters

 
    # Return a list of all possible words, according to the dictionary, given the number os characters
    def FindCombinations(self, numChars) -> list:

        letters = self.__centralLetters + self.__sideLetters

        # Find all possible combinations of letters
        self.__Log('antes do comb...')
        combinationsIter = itertools.product(letters, repeat=numChars)
        self.__Log('...depois do comb')

        # From all possible combinations, filter the ones who follow the game rules:
        # 1- Contains the central letter
        # 2- Word exists on dictionary (spell())
        combFiltered = []
        hs = Hunspell(self.__dictName, hunspell_data_dir=self.__dictPath)
        try:
            for combination in combinationsIter:
                combStr = ''.join(combination)
                self.__Log('Combination str: ' + combStr)
                for centralCh in self.__centralLetters:
                    if (centralCh in combStr) and (hs.spell(combStr)):
                        combFiltered.append(combStr)
        except KeyboardInterrupt:
            print()
            print('-> Programa interrompido antes do fim da análise!!')
        self.__Log('depois da iteracao')

        print()
        print('Palavras encontradas:')
        print(combFiltered)
        print()

        # Strip accents from the word, then remove repeated words ('para', 'pará'), then put in alphabetic order
        filtered2 = [self.__StripAccents(word) for word in combFiltered]
        tryLst = sorted(set(filtered2))
        return tryLst


    # Like FindCombinations(), but multiprocessing
    def FindCombinationsMP(self, numChars) -> list:

        letters = self.__centralLetters + self.__sideLetters

        if (numChars % 2) == 0:  # Par
            centrals = [''.join(item) for item in list(itertools.product(letters, repeat=2))]
            self.__Log('antes do comb...')
            combinationsList = [''.join(item) for item in list(itertools.product(letters, repeat=(numChars-2)//2))]
            self.__Log('...depois do comb')            
        else:   # Impar
            centrals = letters.copy()
            # Find all possible combinations of letters
            self.__Log('antes do comb...')
            combinationsList = [''.join(item) for item in list(itertools.product(letters, repeat=numChars//2))]
            self.__Log('...depois do comb')

        sharedQueue = mp.Queue()
        processes = [mp.Process(target=MultiprocessRun, args=(combinationsList, self.__centralLetters, lett, self.__dictName, self.__dictPath, sharedQueue)) for lett in centrals]
        for proc in processes:
            print("inicia processo...")
            proc.start()
        for proc in processes:
            proc.join()
            print("...encerrou processo")
        
        combFiltered = [sharedQueue.get() for x in range(sharedQueue.qsize())]
        print()
        print('Palavras encontradas:')
        print(combFiltered)
        print()
        
        # Strip accents from the word, then remove repeated words ('para', 'pará'), then put in alphabetic order
        filtered2 = [self.__StripAccents(word) for word in combFiltered]
        tryLst = sorted(set(filtered2))
        return tryLst


    # Type the list of words
    def TypeWords(self, wordsList) -> None:
        for word in wordsList:
            for chr in word:
                # press key and release after 10ms
                self.__keyboardController.press(chr)
                time.sleep(0.01)
                self.__keyboardController.release(chr)
                # wait 150ms to press next key
                time.sleep(0.15)
            # In the end of the word, press ENTER key and wait 500ms to the next word
            self.__keyboardController.press(Key.enter)
            time.sleep(0.01)
            self.__keyboardController.release(Key.enter)
            time.sleep(1)
    


    # ============== Private Methods ==============

    # Strip accents from the words (except the 'ç')
    def __StripAccents(self, word) -> str:
        if 'ç' not in word:
            return unidecode(word)
        
        strippedWord = ''
        for ch in word:
            if ch == 'ç':
                strippedWord += ch
            else:
                strippedWord += unidecode(ch)
        return strippedWord
    

    # Debug print
    def __Log(self, log):
        if self.__DEBUG:
            print(log)



# Multiprocess function
def MultiprocessRun(combLst, centralLetters, central, dictName, dictPath, queue):
    hs = Hunspell(dictName, hunspell_data_dir=dictPath)
    for item in combLst:
        for item2 in combLst:
            combStr = item + central + item2
            for centralCh in centralLetters:
                if (centralCh in combStr) and (hs.spell(combStr)):
                    print(combStr)
                    queue.put(combStr)
