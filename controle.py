class Controle:
    estados = [0,1,2,3,4,5,6,7,8,9]
    comando = ""

    def insere_comando(self, comando):
        self.comando = comando

    def saida(self):
        print(self.estado_atual)
        return self.dic_saida[self.estado_atual]()

    def saida0(self):
        saida = {
            "lerMemoria":1, "ULAFonteA":0, "louD":0, 
            "IREEsc":1, "ULAFonteB":"01", "ULAOp": "00", 
            "PCEsc":1, "FontePC":"00"
        }
        self.estado_atual = 1
        return saida

    def saida1(self):
        saida = {
            "ULAFonteA":0,
            "ULAFonteB":"11", 
            "ULAOp": "00", 
        }

        if "lw" in self.comando or "sw" in self.comando:
            self.estado_atual = 2 
        elif "beq" in self.comando:
            self.estado_atual = 8
        else:
            # Caso seja tipo r
            self.estado_atual = 6
        return saida

    def saida2(self):
        saida = {
            "ULAFonteA":1,
            "ULAFonteB":"10", 
            "ULAOp": "00", 
        }

        if "lw" in self.comando:
            self.estado_atual = 3
        elif "sw" in self.comando:
            self.estado_atual = 5

        return saida

    def saida3(self):
        # Acesso a memoria
        saida = {
            "lerMemoria":1, "louD":0,
        }
        self.estado_atual = 4
        return saida

    def saida4(self):
        saida = {
            "EscReg":1, "MemParaReg":1, 
            "RegDist":0
        }
        self.estado_atual = 0
        return saida

    def saida5(self):
        #acesso a memoria
        saida = {
            "EscMem":1, "louD":1
        }
        self.estado_atual = 0
        return saida

    def saida6(self):
        #execução
        saida = {
            "ULAFonteA":1, "ULAFonteB":"00", 
            "ULAOp":"10"
        }
        self.estado_atual = 7
        return saida

    def saida7(self):
        #Termino da instrução tipo R (escrita em Rd)
        saida = {
            "RegDst":1, "EscReg":1,
            "MemParaReg":0
        }
        self.estado_atual = 0
        return saida

    def saida8(self):
        #Termino do desvio condicional
        saida = {
            "ULAFonteA":1, "ULAFonteB":"00", 
            "ULAOp": "01", "PCEsc":0, 
            "FontePC":"01", "PCEscCond":1
        }
        self.estado_atual = 0
        return saida

    def saida9(self):
        self.estado_atual = 0
        saida = {
            "PCEsc":1, "FontePC":"01"
        }
        self.estado_atual = 0
        return saida

    def __init__(self):
        self.estado_atual = 0
        self.dic_saida = {
            0: self.saida0,
            1: self.saida1,
            2: self.saida2,
            3: self.saida3,
            4: self.saida4,
            5: self.saida5,
            6: self.saida6,
            7: self.saida7,
            8: self.saida8,
            9: self.saida9
        }

a = Controle()

def p1():
    return 2

dict = {
    1: p1
}

print(a.saida())
print(a.saida())