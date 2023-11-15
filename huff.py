# Pedro José de Araújo Siqueira Lima - 190036541
# Teoria da Informação - Projeto Final

import argparse, bisect, math, os
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
    print(header)

    # Escrevendo os bytes no arquivo .huff
    with open(compactedFile, "wb") as binaryFile:
        binaryFile.write(codedBytes)
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

    header = {'00000': b'\r', '0000100': b'\xa3', '0000101000': b'G', '0000101001': b'y', '000010101': b':', '0000101100000': b'(', '0000101100001': b'\xad', '000010110001000': b'\x93', '000010110001001': b'5', '00001011000101': b'\xa0', '0000101100011': b'|', '00001011001': b'\xbb', '0000101101': b'\xb3', '000010111': b'O', '000011000': b'D', '0000110010': b'\xc2', '00001100110': b'\xab', '00001100111': b'\xb5', '00001101': b'C', '00001110': b'\xa1', '00001111': b"'", '00010': b'c', '000110': b'v', '000111': b'h', '001': b'a', '0100': b'r', '0101': b's', '0110000000': b'\xb4', '0110000001': b'V', '0110000010000000': b'+', '011000001000000100': b'&', '0110000010000001010': b'~', '0110000010000001011': b'\xb2', '01100000100000011000': b'\x8a', '01100000100000011001': b'\xb9', '01100000100000011010': b'@', '01100000100000011011': b'%', '011000001000000111': b'\x87', '011000001000001': b'3', '01100000100001': b'\x81', '011000001000100': b'*', '01100000100010100': b']', '01100000100010101': b'[', '0110000010001011': b'9', '011000001000110': b'Y', '011000001000111': b'4', '011000001001000': b'2', '011000001001001': b'}', '011000001001010': b'{', '01100000100101100': b'\xb1', '01100000100101101': b'Z', '0110000010010111': b'7', '0110000010011000': b'/', '01100000100110010': b'K', '011000001001100110': b'\xa2', '011000001001100111': b'$', '011000001001101': b'\xba', '011000001001110': b'8', '011000001001111': b'X', '01100000101': b'L', '0110000011': b'T', '01100001': b'\xa7', '011000100': b'M', '011000101': b'x', '01100011000': b'F', '01100011001': b'B', '0110001101': b';', '011000111': b'A', '0110010': b'q', '01100110': b'z', '01100111': b'E', '01101': b'l', '011100': b'.', '011101': b'\xc3', '01111': b't', '1000000': b'f', '10000010000': b'Q', '10000010001': b'I', '1000001001': b'N', '100000101': b'\xa9', '100000110000': b'k', '100000110001': b'H', '100000110010': b'^', '100000110011': b'\x89', '1000001101': b'?', '100000111': b'j', '100001': b'p', '10001': b'u', '10010': b'm', '1001100': b'b', '1001101': b'-', '1001110000': b'S', '10011100010': b'\xaa', '1001110001100000': b'6', '1001110001100001': b'W', '1001110001100010': b'"', '1001110001100011': b'#', '100111000110010': b'\xa8', '100111000110011': b'0', '10011100011010': b'1', '10011100011011': b')', '100111000111': b'w', '100111001': b'_', '1001110100': b'P', '10011101010': b'R', '100111010110': b'J', '100111010111': b'U', '100111011': b'!', '1001111': b'g', '101': b' ', '11000': b'n', '11001': b'd', '1101': b'o', '111000': b',', '111001': b'\n', '11101': b'i', '1111': b'e'}

    # Verificando se arquivo escolhido é um .huff
    if not file.endswith('.huff'):
        return print('Erro. Arquivo escolhido não é um .huff')
    
    data = b''
    with open(file, "rb") as dataFile:
        data = toBinary(dataFile.read())
        dataFile.close()

    # Substituindo cada byte por seu código (funciona, mas demora)
    codedData = b''
    test = ''
    for x in data[:-7]:
        test += x
        if header.get(test) != None:
            codedData += header[test]
            test = ''

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