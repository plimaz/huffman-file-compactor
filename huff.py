# Pedro José de Araújo Siqueira Lima - 190036541
# Teoria da Informação - Projeto Final

import argparse, bisect
from pathlib import Path

import sys
sys.set_int_max_str_digits(0)

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

    # Método de testes que imprime a árvore
    def printTree(self):
        def printNode(node, val=0):
            if not node == None:
                printNode(node.right, val+1)
                print(' '*2*val+'- '+str(node.char)+' ('+node.code+')')
                printNode(node.left, val+1)
        return printNode(self)

    # Método que atualiza os códigos de cada nó
    def updateCodes(self):
        def updateCode(node, code=''):
            if not node == None:
                updateCode(node.left, code+node.code)
                updateCode(node.right, code+node.code)
                node.code = code + node.code
        return updateCode(self)
    
    # Método que pega as folhas da árvore
    def getLeaves(self):
        leaves = {}
        def getLeaf(node):
            if not node == None:
                if (node.left == None and node.right == None):
                    leaves[node.char] = node.code
                getLeaf(node.left)
                getLeaf(node.right)
        getLeaf(self)
        return leaves

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

    # Algoritmo de Huffman, retorna a árvore binária com seus custos
    data = open(file, "rb").read()
    huff = huffman(data)

    # Pegando apenas as folhas da árvore
    leaves = huff.getLeaves()

    
    print(leaves)

    # Substituindo cada byte por seu código
    """codedData = ''
    for x in data:
        codedData += leaves[x.to_bytes()]

    # Fazendo o zero-padding
    qty0 = len(codedData) % 8
    if qty0 > 0:
        qty0 = 8 - qty0

    codedData += '0' * qty0

    # Transformando os bits codificados em bytes
    print(int(codedData))
    codedBytes = int(codedData).to_bytes(len(codedData))
    print(codedBytes)

    # Escrevendo os bytes no arquivo .huff
    #with open("teste.huff", "ab") as binaryFile:
    #    binaryFile.write(codedBytes)"""

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
        byte = i.to_bytes()

        if byte in freq:
            freq[byte] += 1
        else:
            freq[byte] = 1

    freq = sorted(freq.items(), key=lambda x:x[1], reverse=True)

    # Convertendo cada tupla de digito / frequência em um nó
    tree = []
    for x in freq:
        tree.append(Node(x[0], x[1]))
        
    # Montando a árvore
    while len(tree) > 1:
        nodeLeft = tree[len(tree) - 1]
        nodeLeft.code = '0'
        tree.pop()

        nodeRight = tree[len(tree) - 1]   
        nodeRight.code = '1'      
        tree.pop()
        
        node = Node('in', nodeLeft.val+nodeRight.val, '', nodeLeft, nodeRight)

        bisect.insort(tree, node, key=lambda x:-1*x.val)

    # Contruindo o código para cada byte de acordo com a árvore
    tree[0].updateCodes()   # direita -> 1, esquerda -> 0
    
    return tree[0]

# -- Main --

if __name__ == '__main__':
    main()