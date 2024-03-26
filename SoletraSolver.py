import itertools
from hunspell import Hunspell
from unidecode import unidecode
import time
import multiprocessing as mp


class SoletraSolver:

    # ============== Private Variables ==============
    __dictName = ""
    __dictPath = ""
    __centralLetters = None
    __sideLetters = None
    __DEBUG = False



    # ============== Constructor ==============
    def __init__(self, dictName:str, dictPath:str, debug=False) -> None:
        self.__dictName = dictName
        self.__dictPath = dictPath
        self.__DEBUG = debug
        self.__termSignalLock = mp.Lock()



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
    

    def WriteTerminateSignal(self, value: bool) -> None:
        self.__termSignalLock.acquire()
        self.__terminateSignal = value
        self.__termSignalLock.release()
    
    def ReadTerminateSignal(self) -> bool:
        self.__termSignalLock.acquire()
        value = self.__terminateSignal
        self.__termSignalLock.release()
        return value

 
    def FindCombinations(self, numChars) -> list:
        """
        Return a list of all possible words, according to the dictionary, given the number os characters
        """
        letters = self.__centralLetters + self.__sideLetters

        # Find all possible combinations of letters
        self.__Log('antes do comb...')
        combinationsIter = itertools.product(letters, repeat=numChars)
        self.__Log('...depois do comb')

        # From all possible combinations, filter the ones who follow the game rules:
        # 1- Contains the central letter
        # 2- Word exists on dictionary (spell())
        combFiltered = []
        try:
            hs = Hunspell(self.__dictName, hunspell_data_dir=self.__dictPath)
        except:
            raise FileExistsError
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
        """
        Return a list of all possible words, according to the dictionary, given the number os characters
        Divide the word in half, fixing the letter in the middle, which must be one of the letters of the game
        E.g.: a word of 7 letters can be expressed as:
            ---x---
        , where x is one of the game letters (central or side).
        The algorithm will generate combinations of 3 letters only (fast to compute) and then test all
        possible combination, using the middle letter. It will be created one independent process to each middle letter.
        For exemple, with this configuration:
            central letter: a
            side letters:   b, c
            number of characters: 5
        The algorithm will do:
        --x-- : combinations of 2 letters: [aa, ab, ac, ba, bb, bc, ca, cb, cc]
        Process 1:
        middle letter: a
        aaaaa, aaaab, aaaac, aaaba, aaabb, ......,  ccacc
        Process 2:
        middle letter: b
        aabaa, aabab, aabac, aabba, aabbb, ......,  ccbcc
        Process 3:
        middle letter: c
        aacaa, aacab, aacac, aacba, aacbb, ......,  ccccc
        If the number of chars is even, the word will be divided like that:
        ----x-----
        """
        letters = self.__centralLetters + self.__sideLetters

        if (numChars % 2) == 0:  # Even
            self.__Log('antes do comb...')
            combinationsList = [''.join(item) for item in list(itertools.product(letters, repeat=(numChars-2)//2))]
            combinationsList2 = [''.join(item) for item in list(itertools.product(letters, repeat=numChars//2))]
            self.__Log('...depois do comb')            
        else:   # Odd
            # Find all possible combinations of letters
            self.__Log('antes do comb...')
            combinationsList = [''.join(item) for item in list(itertools.product(letters, repeat=numChars//2))]
            combinationsList2 = combinationsList
            self.__Log('...depois do comb')

        sharedQueue = mp.Queue()
        processes = [mp.Process(target=MultiprocessRun, args=(combinationsList, combinationsList2, self.__centralLetters, lett, self.__dictName, self.__dictPath, sharedQueue)) for lett in letters]
        for proc in processes:
            self.__Log("inicia processo...")
            proc.start()
        self.WriteTerminateSignal(False)
        try:
            while not self.ReadTerminateSignal():
                for proc in processes:
                    if not proc.is_alive():
                        proc.close()
                        self.__Log("...encerrou processo")
                        processes.remove(proc)
                if len(processes) <= 0:
                    break
                time.sleep(0.5)
            if len(processes) > 0:
                raise KeyboardInterrupt
        except KeyboardInterrupt:
            for proc in processes:
                proc.kill()
            print()
            print('-> Programa interrompido antes do fim da análise!!')
        
        combFiltered = [sharedQueue.get() for x in range(sharedQueue.qsize())]
        print()
        print('Palavras encontradas:')
        print(combFiltered)
        print()
        
        # Strip accents from the word, then remove repeated words ('para', 'pará'), then put in alphabetic order
        filtered2 = [self.__StripAccents(word) for word in combFiltered]
        tryLst = sorted(set(filtered2))
        return tryLst
    


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
def MultiprocessRun(combLst, combLst2, centralLetters, central, dictName, dictPath, queue):
    hs = Hunspell(dictName, hunspell_data_dir=dictPath)
    for item in combLst:
        for item2 in combLst2:
            combStr = item + central + item2
            for centralCh in centralLetters:
                if (centralCh in combStr) and (hs.spell(combStr)):
                    # print(combStr)
                    queue.put(combStr)
