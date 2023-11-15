# Pedro José de Araújo Siqueira Lima - 190036541
# Teoria da Informação - Projeto Final

import argparse, bisect, math, os, pickle
from pathlib import Path

import sys
sys.set_int_max_str_digits(0)

# -- Classe de nós para criação da árvore binária --

# Classe
class Node:
    # Definições básicas
    def __init__(self, char, prob, code='', left=None, right=None):
        self.char = char
        self.prob = prob
        self.code = code
        self.left = left    
        self.right = right

    # Método de testes que imprime a árvore
    def printTree(self):
        def printNode(node, val=0):
            if not node == None:
                printNode(node.right, val+1)
                print(' '*2*val+'- '+str(node.char)+' ('+str(node.code)+')')
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
                    leaves[node.char] = (node.code, node.prob)
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
    # Verificando se arquivo existe
    if not os.path.exists(file):
        return print('Arquivo escolhido não existe.')

    # Verificando se arquivo escolhido é um .huff
    if file.endswith('.huff'):
        return print('Erro. Arquivo escolhido já é um .huff')
    
    # Verificando se arquivo já existe
    compactedFile = Path(file).stem + ".huff"
    if os.path.exists(compactedFile):
        ask = input('\n' + compactedFile + ' já existe. Deseja sobrescreve-lo? (y / n) ')
        if (ask == 'N' or ask == 'n'):
            return print('\nCompactação cancelada.\n')

    # Lendo os bytes do arquivo
    data = b''
    with open(file, "rb") as dataFile:
        data = dataFile.read()
        dataFile.close()

    # Algoritmo de Huffman, retorna a árvore binária com seus custos
    huff = huffman(data)

    # Pegando apenas as folhas da árvore
    leaves = huff.getLeaves()

    # Substituindo cada byte por seu código
    codedData = ''
    for x in data:
        codedData += (leaves[x.to_bytes()])[0]

    # Fazendo o zero-padding
    codedData = zeroPadding(codedData)

    # Transformando os bits codificados em bytes
    codedBytes = toBytes(codedData)

    # Adicionando o cabeçalho que será utilizado na decodificação
    header = {v[0]: k for k, v in leaves.items()}
    codedHeader = pickle.dumps(header)

    # Escrevendo os bytes no arquivo .huff
    with open(compactedFile, "wb") as binaryFile:
        binaryFile.write(codedHeader + b'HEADER' + codedBytes)
        binaryFile.close()

    # Calculando entropia e tamanho médio
    h, lav = calcInfo(leaves) 

    # Calculando taxa de compressão
    sizeOriginal = os.path.getsize(file)
    sizeCompacted = os.path.getsize(compactedFile)
    tx = (1 - (sizeCompacted / sizeOriginal)) * 100

    # Imprimindo tudo na tela
    print('\nArquivo comprimido em "'+compactedFile+'" com sucesso!',
          '\n\nEntropia: '+str(round(h, 4)) + ' bits', 
          '\nComprimento médio: '+str(round(lav, 4)) + ' bits', 
          '\nTaxa de compressão: '+ str(round(tx, 2))+ '%\n')

# Função de descompacta um arquivo .huff
def decompact(file):
    # Verificando se arquivo escolhido é um .huff
    if not file.endswith('.huff'):
        return print('Erro. Arquivo escolhido não é um .huff')
    
    # Lendo os bytes do arquivo
    data = b''
    with open(file, "rb") as dataFile:
        data = dataFile.read()
        dataFile.close()

    # Separando o header do resto
    data = data.split(b'HEADER')
    header = pickle.loads(data[0])
    code = toBinary(data[1])

    # Substituindo cada byte por seu código (funciona, mas demora)
    codedData = b''
    test = ''
    for x in code:      # pensar como remover o padding
        test += x
        if header.get(test) != None:
            codedData += header[test]
            test = ''

    # Escrevendo os dados no arquivo descompactado
    print(codedData)

# Função que realiza o algoritmo de codificação de Huffman
def huffman(string):
    # Pegando a frequência de cada dígito
    freq = {}
    qty = 0
    for i in string:
        byte = i.to_bytes()
        qty += 1
        if byte in freq:
            freq[byte] += 1
        else:
            freq[byte] = 1

    # Transformando frequência em probabilidade
    prob = {}
    for key, value in freq.items():
        prob[key] = value / qty

    prob = sorted(prob.items(), key=lambda x:x[1], reverse=True)

    # Convertendo cada tupla de digito / probabilidade em um nó
    tree = []
    for x in prob:
        tree.append(Node(x[0], x[1]))
        
    # Montando a árvore
    while len(tree) > 1:
        nodeLeft = tree[len(tree) - 1]
        nodeLeft.code = '0'
        tree.pop()

        nodeRight = tree[len(tree) - 1]   
        nodeRight.code = '1'      
        tree.pop()
        
        node = Node('in', nodeLeft.prob+nodeRight.prob, '', nodeLeft, nodeRight)

        bisect.insort(tree, node, key=lambda x:-1*x.prob)

    # Contruindo o código para cada byte de acordo com a árvore
    tree[0].updateCodes()   # direita -> 1, esquerda -> 0
    
    return tree[0]

# -- Funções auxiliares --

# Função que transforma uma string binária (i.e. '10101000' e.g.) em bytes
def toBytes(string):
    b = bytearray()
    for i in range(0, len(string), 8):
        b.append(int(string[i:i+8], 2))
    return bytes(b)

# Função que transforma bytes em uma string binária
def toBinary(bytes):
    str = ''
    for i in bytes:
        s = format(i, '08b')
        s = zeroPadding(s)
        str += s
    return str

# Função que faz o zero-padding
def zeroPadding(str):
    qty0 = len(str) % 8
    if qty0 > 0:
        qty0 = 8 - qty0
    str += '0' * qty0
    return str

# Função que pega a entropia e o tamanho médio de um código
def calcInfo(nodes):
    h = 0
    lav = 0
    for x in nodes:
        code, prob = nodes[x]
        h += prob * math.log2(prob)
        lav += prob * len(code)
    return (-h), lav

# -- Main --

if __name__ == '__main__':
    main()