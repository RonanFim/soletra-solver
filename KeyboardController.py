from pynput.keyboard import Key, Controller
import time

class KeyboardController:

    # ============ private vars ===============
    __keyboardController = None

    # ============ Constructor ================
    def __init__(self) -> None:
        self.__keyboardController = Controller()
    
    # Type the list of words
    def TypeWords(self, wordsList: list) -> None:
        time.sleep(5)
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
