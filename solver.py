from SoletraSolver import SoletraSolver
import time
import os

# Main
if __name__ == "__main__":

    solver = SoletraSolver('pt_BR', os.getcwd()+'\dictionaries')

    # Obtem letras centrais
    centrais = input('Letras Centrais: ')
    solver.SetCentralLetters(centrais)

    # Obtem letras laterais
    laterais = input('Letras Auxiliares: ')
    solver.SetSideLetters(laterais)

    op = True
    while(op):
        num = input('Quantas letras? (entre qualquer caracter para cancelar): ')
        if not num.isnumeric():
            op = False
        else:
            print("Obtendo lista de palavras possíveis...")
            palavras = solver.FindCombinations(int(num))
            resp = input('Analise finalizada! Iniciar preenchimento? -> ')
            if resp.lower() == 's':
                time.sleep(5)
                solver.TypeWords(palavras)
            else:
                op = False
