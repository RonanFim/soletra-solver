from SoletraSolver import SoletraSolver
import time

# Main
if __name__ == "__main__":

    solver = SoletraSolver('pt_BR', 'C:\AreaTransf\soletraSolver')

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
            palavras = solver.FindCombinations(int(num))
            print(palavras)
            resp = input('Analise finalizada! Iniciar preenchimento? -> ')
            if resp.lower() == 's':
                time.sleep(5)
                solver.TypeWords(palavras)
            else:
                op = False
