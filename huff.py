# Pedro José de Araújo Siqueira Lima - 190036541
# Teoria da Informação - Projeto Final

import argparse
from pathlib import Path

# -- Função Principal --

def main():

    # Pegando o comando utilizado
    command = getCommand()

    # Realizando a função correta
    match command[0]:
        case 'compact':
            compact(command[1])
        case 'decompact':
            decompact(command[1])

# -- Funções --

# Função que pega o comando usado pelo usuário 
def getCommand():
    parser = argparse.ArgumentParser()
    commands = parser.add_mutually_exclusive_group(required=True)

    commands.add_argument("-c", "--compactar", 
                        dest="compact",
                        action="store",
                        help="compacta um arquivo")

    commands.add_argument("-d", "--decompactar", 
                        dest="decompact", 
                        action="store", 
                        help="decompacta um arquivo")

    args = parser.parse_args()

    if args.compact != None:     return ("compact", args.compact)
    elif args.decompact != None: return ("decompact", args.decompact)

# Função que compacta um arquivo qualquer
def compact(file):
    # Verificando se arquivo escolhido é um .huff
    if file.endswith('.huff'):
        return print('Erro. Arquivo escolhido já é um .huff')

    # Algoritmo de Huffman
    print(huffman(open(file, "r", encoding="utf8").read()))

# Função de descompacta um arquivo .huff
def decompact(file):
    # Verificando se arquivo escolhido é um .huff
    if not file.endswith('.huff'):
        return print('Erro. Arquivo escolhido não é um .huff')
    
    print(file)

# Função que realiza o algoritmo de codificação de Huffman
def huffman(str):
    # Pegando a frequência de cada dígito
    freq = {}
    for i in str:
        if i in freq:
            freq[i] += 1
        else:
            freq[i] = 1

    freq = sorted(freq.items(), key=lambda x:x[1], reverse=True)
    
    return freq

# --
if __name__ == '__main__':
    main()