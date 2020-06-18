### Guilherme Hiago Costa dos Santos ###

font = ''
result = ""

# Dicionario de valores dos codigos de opcode
opcode = {"lui":'0x0f',"lw":'0x23', 
        "sw":'0x2b', "beq":'0x04',
        "bne":'0x05',"j":'0x02', "ori":'0x0d',
        "addiu":'0x09',"andi":'0x0c'}

# Dicionario de valores dos codigos de função
func = {"addu":33, "slt":42, "jr":8, 
        "and":36, "xor":38, "sll":0, "srl":2}

# Dicionario de valores dos registradores
reg = {'$0': 0, '$1': 1, '$2': 2, '$3': 3, 
        '$4': 4, '$5': 5, '$6': 6, '$7': 7, 
        '$8': 8, '$9': 9, '$10': 10, '$11': 11, 
        '$12': 12, '$13': 13, '$14': 14, '$15': 15, 
        '$16': 16, '$17': 17, '$18': 18, '$19': 19, 
        '$20': 20, '$21': 21, '$22': 22, '$23': 23, 
        '$24': 24, '$25': 25, '$26': 26, '$27': 27, 
        '$28': 28, '$29': 29, '$30': 30, '$31': 31}


#Complemento de dois para decimal (usado no condicional)
def comp2(b):
    agregado = 1

    if int(b[0]) == 1 and len(b) > 1:
        agregado = -1

    sig = (2 ** (len(b)-1)) * int(b[0])

    b = b[1:]

    b = b[::-1]
    soma = 0

    for i in range(len(b)):
        soma += (2 ** i) * int(b[i])

    if agregado == 1:
        return sig + soma

    return soma - sig


#Converte valor hexa para decimal
def hex2bin(n, bits = None):
    retorno = bin(int(n, 16))[2:]

    if bits != None:
        dif = bits - len(retorno)

        if dif > 0: retorno = ("0"*dif)+retorno

    return retorno


#Converte valor decimal para binario
def dec2bin(n, bits = None):
    retorno = ""
    bitComplemento = '0'

    if n < 0:
        n *= -1
        retorno = bin(n)[2:]
        retorno = retorno

        for i in range(len(retorno)):
            if retorno[i] == '1':
                retorno = retorno[:i] + '0' + retorno[i+1:]
            else:
                retorno = retorno[:i] + '1' + retorno[i+1:]
        
        retorno = retorno[::-1]

        for i in range(len(retorno)):
            if retorno[i] == '0':
                retorno = retorno[:i] + '1' + retorno[i+1:]
                break
            else:
                retorno = retorno[:i] + '0' + retorno[i+1:]
        
        retorno = retorno[::-1]
        bitComplemento = '1'
    else:
        retorno = bin(n)[2:]

    if bits != None:
        dif = bits - len(retorno)

        if dif > 0: retorno = (bitComplemento*dif)+retorno

    return retorno


#Verifica o tipo de codificação (R, J ou I)
def codifica(cod):
    while(cod[0] == 0):
        cod = l[1:]
    
    comando = cod[0:cod.find(' ')]

    if comando == "beq" or comando == "bne":
        #label = l[l.find(' ')+1:]
        #label = label.split(',')
        #label = label[2].strip()

        des = cod.split(",")
        des = int(des[2].strip())
        return(codTypeI(cod, des)) #calcula_salto_condicional(linha_atual, label)))

    elif comando == "j":

        des = cod.replace("j", '') #calcula_salto_incondicional(label)))
        des = des.strip()
        return(codTypeJ(cod, des))

    elif comando in opcode.keys():
        return(codTypeI(cod))
        
    elif comando in func.keys():
        return(codTypeR(cod))


# Codifica o tipo R
def codTypeR(cod):
    # opcode | 1 fonte(rs) | 2 fonte(rt) | rd | shampt | func
    resp = "000000" # Ja contem opcode -4 bits

    comando = cod[0:cod.find(' ')].strip()

    cod = cod.replace(comando+' ', '')
    cod = cod.split(',')

    # Se n argumentos == 1 -> jr
    if len(cod) == 1: 
        comando = dec2bin(func[comando], 5)
        rs = dec2bin(reg[cod[0].strip()], 5)

        resp += rs + dec2bin(0, 16) + comando
    # Caso contrario possui 3 argumentos
    else:
        rd = cod[0].strip()
        rs = cod[1].strip()
        rt = cod[2].strip()

        comando = dec2bin(func[comando], 6)
        rd = dec2bin(reg[rd], 5)
        rs = dec2bin(reg[rs], 5)

        # Caso rt não seja um registrador
        if not rt in reg:
            rt = dec2bin(int(rt), 5)
            resp += '00000' + rs + rd + rt + comando
        else:
            rt = dec2bin(reg[rt], 5)
            resp += rs + rt + rd + '00000' + comando

    repsHex = "0x"
    
    # Converte binario em hexa
    for i in range(len(resp)//4):
        repsHex += hex(int(resp[:4], 2))[2:]
        resp = resp[4:]
        
    return repsHex


# Codifica o tipo I
def codTypeI(cod, deslocamento = None):
    # opcode | rs | rt (destino) | imediato (deslocamento)
    sem_rs = False
    op = cod[0:cod.find(' ')].strip()
    # alterar para lui
    cod = cod.replace(op+' ', '')
    cod = cod.split(',')

    if deslocamento == None:
        # Se o codigo tem 2 argumentos
        if len(cod) == 2:
            # Se ouver parenteses na linha o deslocamento vem logo antes dele
            if "(" in cod[1]:
                des = cod[1].strip()
                deslocamento = int(des[:des.find('(')])
                cod[1] = cod[1][cod[1].find("(")+1:]
                cod[1] = cod[1][:len(cod[1])-2]
            # Se não ouver, o deslocamento é o segundo argumento
            else:
                des = cod[1].strip()
                deslocamento = int(des)
                cod[1] = "0"
                sem_rs = True
        # Caso contrario o deslocamento é o terceiro argumento
        else:
            deslocamento = int(cod[2].strip())
    # Se deslocamento == None -> salto condicional
    

    rs = cod[1].strip()
    rt = cod[0].strip()

    op = hex2bin(opcode[op], 6)
    rt = dec2bin(reg[rt], 5)
    deslocamento = dec2bin(deslocamento, 16)

    if sem_rs:
        rs = "00000"
    else:
        rs = dec2bin(reg[rs], 5)

    resp = op + rs + rt + deslocamento
    repsHex = "0x"
    
    # Converte o binario em hexa
    for i in range(len(resp)//4):
        repsHex += hex(int(resp[:4], 2))[2:]
        resp = resp[4:]
    
    return repsHex


# Codifica o tipo J
def codTypeJ(cod, deslocamento):
    op = cod[0:cod.find(' ')].strip()

    resp = hex2bin(deslocamento,32)
    op = hex2bin(opcode[op],6)

    resp = resp[4:]
    resp = resp[:len(resp)-2]
    resp = op + resp
    repsHex = "0x"
    
    # Converte para hexadecimal
    for i in range(len(resp)//4):
        repsHex += hex(int(resp[:4], 2))[2:]
        resp = resp[4:]
    
    return repsHex


# Verifica qual tipo de decodificação
def decodifica(cod):
    # Converte os 2 digitos mais significativos para binario
    op = dec2bin(int(cod[:5], 16), 11)

    if op[:6] == "000000":
        return decodTypeR(cod)
    elif int(op[:5], 2) == 2:
        return decodTypeJ(cod)
    else:
        return decodTypeI(cod)


# Dodifica o tipo R
def decodTypeR(cod):
    # opcode | 1 fonte(rs) | 2 fonte(rt) | rd | shampt | func

    # Converte o codigo hex para binario
    cod = dec2bin(int(cod, 16), 32)
    op = dec2bin(0)
    
    rs = int(cod[6:11], 2)
    rt = int(cod[11:16], 2)
    rd = int(cod[16:21], 2)
    shamt = int(cod[21:26], 2)
    funct = int(cod[26:], 2)

    comando = ''

    for k in func.keys():
        if func[k] == funct:
            comando += k
            comando += "    "
            comando += " "*(4-len(k))
            break
    
    # Escolhe como concatenar o resultado para ceda modelo
    if  "jr" in comando:
        comando += "${}".format(rs)
    elif shamt == 0:
        comando += "${}, ${}, ${}".format(rd, rs, rt)
    else:
        comando += "${}, ${}, {}".format(rd, rt, shamt)
    
    return comando


# Codifica o tipo I
def decodTypeI(cod):
    # opcode | rs | rt (destino) | imediato (deslocamento)

    # Converte o codigo hex para binario
    cod = dec2bin(int(cod, 16), 32)
    op = hex(int(cod[:6], 2))
    
    rs = int(cod[6:11], 2)
    rt = int(cod[11:16], 2)
    desl = int(cod[16:32], 2)

    comando = ''

    #Procura a instrução no dicionario
    for k in opcode.keys():
        if int(opcode[k], 16) == int(op, 16):
            comando += k
            op = k
            comando += "    "
            comando += " "*(4-len(k))
            break
    
    # Escolhe como concatenar o resultado para ceda modelo
    if op in ["sw", "lw"]:
        comando += "${}, {}(${})".format(rt, desl, rs)
    elif op in ["addiu", "ori", "andi", "beq", "bne"]:
        comando += "${}, ${}, {}".format(rt, rs, desl)
    elif op == "lui":
        comando += "${}, {}".format(rt, desl)
    
    return comando


# Codifica o tipo J
def decodTypeJ(cod):
    # Converte o codigo hex para binario
    bin_l = dec2bin(int(cod, 16), 32)
    resp = "j       "

    bin_l = bin_l[6:] + "00"

    desl = "0x0"

    #Calcula o deslocamento
    for i in range(len(bin_l)//4):
        desl += hex(int(bin_l[:4], 2))[2:]
        bin_l = bin_l[4:]

    return  resp + desl


def main():
    in1 = input("Digite o nome do arquivo de entrada (com o tipo, ex: .asm): ").strip()
    in2 = int(input("Digite o tipo de operação \n(1) Codificar \n(2) Decodificar \n->:").strip())
    in3 = input("Digite o nome do arquivo de saida (com o tipo, ex: .asm): ").strip()
    font = open(in1, 'r')
    result = open(in3, 'w')
    label = 1

    # Codifica linha por linha
    if in2 == 1:
        resp = []

        for l in font:
            resp.append(codifica(l))
        
        for i in resp:
            result.write(i+"\n")

    else:
        resp = [".text", "    .globl main ", "main:	"]

        for l in font:
            resp.append(decodifica(l))

        linha_atual = 0

        #Verifica se algum salto esta sem o label
        for l in resp:
            # Codifica salto tipo I
            if "j" in l and not "$" in l:
                desl = 0

                try:
                    desl = int(l.replace('j', '').strip(), 16) - int("00400000", 16)
                except:
                    continue

                cont = (desl/4)+2
                linha_label = 1

                # Procura posição do label, cria um ou usa o nome de um existente
                for i in resp:
                    if ":" in i:
                        linha_label += 1
                        continue
                    else:
                        if cont == 0:
                            if ":" in  resp[linha_label-2]:
                                resp.pop(linha_label-1)
                                resp.insert(linha_label-1, str("j       "+ resp[linha_label-2].replace(":", '')))
                                break
                            else:
                                resp.insert(linha_label, str("label"+str(label)+":"))
                                resp.pop(linha_label-1)
                                resp.insert(linha_atual, str("j       "+"label"+str(label)))
                                label += 1
                            break
                        cont -= 1
                    linha_label += 1

            # Codifica Condiconal
            if "beq" in l or "bne" in l:
                desl = 0

                try:
                    desl = dec2bin(int(l.split(",")[2]))
                    desl = comp2(desl)
                except:
                    # caso caia em o condicional com label pronte pula a linha
                    continue

                text = l.split(",")
                
                # Procura posição do label, cria um ou usa o nome de um existente
                if ":" in resp[linha_atual+desl+1]:
                    text[2] = ", " + resp[linha_atual+desl+1].replace(":",'').strip()
                    resp.pop(linha_atual)
                    resp.insert(linha_atual, str(text[0]+", "+text[1]+text[2]))
                else:
                    resp.pop(linha_atual)   # Esclui o proprio comando para se inserir novamente
                    text[2] = ", label" + str(label)
                    resp.insert(linha_atual,  str(text[0]+", "+text[1]+text[2]))
                    resp.insert(linha_atual+1+desl, str("label"+str(label)+":"))
                    label += 1
                
            linha_atual += 1

        #Escreve Resposta
        for i in resp:
            result.write(i+"\n")
    
    #Fecha os arquivos de entrada e saida
    font.close()
    result.close()

#Executa o programa
main()
