from SoletraSolverGUI import SoletraSolverGUI
import time
import os

# Main
if __name__ == "__main__":

    # solver = SoletraSolver('pt_BR', os.getcwd()+'\dictionaries')
    solver = SoletraSolverGUI()

    solver.MainLoop()

    # # Obtem letras centrais
    # centrais = input('Letras Centrais: ')
    # solver.SetCentralLetters(centrais)

    # # Obtem letras laterais
    # laterais = input('Letras Auxiliares: ')
    # solver.SetSideLetters(laterais)

    # op = True
    # while(op):
    #     num = input('Quantas letras? (entre qualquer caracter para cancelar): ')
    #     if not num.isnumeric():
    #         op = False
    #     else:
    #         print("Obtendo lista de palavras possíveis...")
    #         if int(num) < 7:
    #             t1 = time.time()
    #             palavras = solver.FindCombinations(int(num))    # Para palavras de até 6 letras, utilizar método tradicional
    #             t2 = time.time()
    #             print("Tempo de execucao: " + str(t2-t1) + " s")
    #         else:
    #             t1 = time.time()
    #             palavras = solver.FindCombinationsMP(int(num))  # Para palavras de 7 letras ou mais, usar multiprocessing
    #             t2 = time.time()
    #             print("Tempo de execucao: " + str(t2-t1) + " s")
    #         resp = input('Analise finalizada! Iniciar preenchimento? -> ')
    #         if resp.lower() == 's':
    #             time.sleep(5)
    #             solver.TypeWords(palavras)
    #         else:
    #             op = False
