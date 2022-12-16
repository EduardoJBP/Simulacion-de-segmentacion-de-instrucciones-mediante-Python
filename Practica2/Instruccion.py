class Instruccion:
    tipo="" #tipo de instruccion
    operacion="" #cual operacion
    rD=""   #degistro destino
    rSrc1=""    #registro source1
    rSrc2=""    #registro source2
    etiqueta="" #etiqueta de la instruccion, si existe
    desplazamiento=0    #desplazamiento en instrucciones lw y sw
    inmediato=0 #para instrucciones con inmediatos
    señalesControl=""    #representa la etapa en la que se encuentra la instruccion decodificada

    def __init__(self):
        self.tipo = ""
        self.operacion = ""
        self.rD = "zero"
        self.rSrc1 = "zero"
        self.rSrc2 = "zero"
        self.etiqueta = ""
        self.desplazamiento = -1 #inicializado a un valor que podremos usar en el futuro
        self.inmediato = -1#inicializado a un valor que podremos usar en el futuro
        self.etapa = "ID"
    def decodificarInstruccion(self, instruccion):
        parametros = instruccion.split(sep=",") #conseguimos dos listas
        aux = parametros[0].split(sep=" ") #conseguimos dos listas, primera posicion operación y en segunda el primer registro
        if aux[0] == "add" or aux[0] == "sub":
            self.tipo = "R"
            self.operacion = aux[0]
            self.rD = aux[1][1:]
            self.rSrc1 = parametros[1][1:]#Se coge desde la posicion 1 para quitar el "$"
            self.rSrc2 = parametros[2][1:]
            #  print(self.operacion + " " + self.rD + " " + self.rSrc1 + " " + self.rSrc2)
        elif aux[0] == "lw":
            self.tipo = "I"
            self.operacion = "lw"
            self.rD = aux[1][1:]
            self.desplazamiento = int(parametros[1][:-5]) / 4 #calcular cuantas palabras esta desplazado
            self.rSrc1 = parametros[1][-3:-1]
            #   print(self.operacion + " " + self.rD + " %d" % self.desplazamiento + " " + self.rSrc1)
        elif aux[0] == "li":
            self.tipo = "I"
            self.operacion = "li"
            self.rD = aux[1][1:]
            self.inmediato = int(parametros[1])
            #  print(self.operacion + " " + self.rD + " %d" % self.inmediato)
        elif aux[0] == "sw":
            self.tipo = "I"
            self.operacion = "sw"
            self.rD = aux[1][1:]
            self.desplazamiento = int(parametros[1][:-5]) / 4
            self.rSrc1 = parametros[1][-3:-1]
            #   print(self.operacion + " " + self.rSrc1 + " %d" % self.desplazamiento + " " + self.rSrc2)
        elif aux[0] == "addi":
            self.tipo = "I"
            self.operacion = "addi"
            self.rD = aux[1][1:]
            self.rSrc1 = parametros[1][1:]
            self.inmediato = int(parametros[2])
            #   print(self.operacion + " " + self.rD + " " + self.rSrc1 + " %d" % self.inmediato)
        elif aux[0] == "j":
            self.tipo = "J"
            self.operacion = "j"
            self.etiqueta = aux[1]
            #  print(self.operacion + " " + self.etiqueta)
        elif aux[0] == "bgt" or aux[0] == "bge" or aux[0] == "beq" or aux[0] == "blt":
            self.tipo = "J"
            self.operacion = aux[0]
            self.rSrc1 = aux[1][1:]
            self.rSrc2 = parametros[1][1:]
            self.etiqueta = parametros[2]
           # print(self.operacion + " " + self.rSrc1 + " " + self.rSrc2 + " " + self.etiqueta)

    def setEtiqueta(self,etiqueta1):
        self.etiqueta=etiqueta1

    def getTipo(self):
        return self.tipo
    def getOperacion(self):
        return self.operacion
    def getRd(self):
        return self.rD
    def getSrc1(self):

        return self.rSrc1
    def getSrc2(self):
        return self.rSrc2
    def getEtiqueta(self):
        return self.etiqueta
    def getDesplazamiento(self):
        return self.desplazamiento
    def getInmediato(self):
        return self.inmediato
    def getEtapa(self):
        return self.etapa
    def setEtapa(self,etapa):
        self.etapa=etapa
    def setSrc1(self,registro):
        self.rSrc1=registro
    def setSrc2(self,registro):
        self.rSrc2=registro
    def setOperacion(self,operacion):
        self.operacion=operacion
    def setRd(self,rd):
        self.rD=rd

    def equals(self,instruccion):
        if instruccion.getTipo() !=self.tipo:
            return False
        if instruccion.getrD() != self.rD:
            return False
        if instruccion.getrSrc1() != self.rSrc1:
            return False
        if instruccion.rSrc2() != self.rSrc2:
            return False
        return True