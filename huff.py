# Pedro José de Araújo Siqueira Lima - 190036541
# Teoria da Informação - Projeto Final

import argparse, bisect
from pathlib import Path

# -- Classe de nós para criação da árvore binária --

# Classe
class Node:
    # Definições básicas
    def __init__(self, char, val, code='', left=None, right=None):
        self.char = char
        self.val = val
        self.code = code
        self.left = left    
        self.right = right

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
    h = huffman(open(file, "r", encoding="utf8").read())

# Função de descompacta um arquivo .huff
def decompact(file):
    # Verificando se arquivo escolhido é um .huff
    if not file.endswith('.huff'):
        return print('Erro. Arquivo escolhido não é um .huff')
    
    print(file)

# Função que realiza o algoritmo de codificação de Huffman
def huffman(string):
    # Pegando a frequência de cada dígito
    freq = {}
    for i in string:
        if i in freq:
            freq[i] += 1
        else:
            freq[i] = 1

    freq = sorted(freq.items(), key=lambda x:x[1], reverse=True)
    
    # Convertendo cada tupla de digito / frequência em um nó
    tree = []
    for x in freq:
        tree.append(Node(x[0], x[1]))

    # Montando a árvore
    while len(tree) > 1:
        node1 = tree[len(tree) - 1]
        node1.code = '1'
        tree.pop()

        node2 = tree[len(tree) - 1]   
        node2.code = '0'      
        tree.pop()
        
        node = Node('in', node1.val+node2.val, '', node1, node2)

        bisect.insort(tree, node, key=lambda x:-1*x.val)

    # Contruindo o código para cada valor de acordo com a árvore
        # direita -> 0, esquerda -> 1
    getCode(tree[0])
    
    return tree[0]

# Função que pega o código de cada nó
def getCode(node, code='', codeList=[]): 
    
    # Código do nó atual
    newCode = code + node.code
    
    # Se não é folha
    if (node.left): 
        getCode(node.left, newCode) 
    if (node.right): 
        getCode(node.right, newCode) 
    
    # É folha
    if (not node.left and not node.right): 
        print(node.char + ' ' + newCode)

# -- Main --

if __name__ == '__main__':
    main()