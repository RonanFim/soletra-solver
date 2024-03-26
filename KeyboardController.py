from pynput.keyboard import Key, Controller
import time
from threading import Lock

class KeyboardController:

    # ============ private vars ===============
    __keyboardController = None

    # ============ Constructor ================
    def __init__(self) -> None:
        self.__keyboardController = Controller()
        self.__stopTypingLock = Lock()
        self.__stopTypingSignal = False
    
    def WriteStopSignal(self, value: bool) -> None:
        self.__stopTypingLock.acquire()
        self.__stopTypingSignal = value
        self.__stopTypingLock.release()
    
    def ReadStopSignal(self) -> bool:
        self.__stopTypingLock.acquire()
        value = self.__stopTypingSignal
        self.__stopTypingLock.release()
        return value

    # Type the list of words
    def TypeWords(self, wordsList: list) -> None:
        self.WriteStopSignal(False)
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
            if self.ReadStopSignal():
                return
