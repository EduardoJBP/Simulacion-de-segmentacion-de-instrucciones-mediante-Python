class BancoRegistros:
    registros = {}

    def __init__(self): #Inicializamos las variables, todas a cero
        self.registros["zero"]=0
        for i in range(2):
            self.registros["v"+"%d"%i]=0
        for i in range(4):
            self.registros["a"+"%d"%i]=0
        for i in range(10):
            self.registros["t"+"%d"%i]=0
        for i in range(8):
            self.registros["s" + "%d" % i] = 0
        self.registros["ra"]=0

    """def getNumeroRegistro(self,registro):#Este método nos permite saber el valor del registro
        if registro=="zero":
            return 0
        if registro[0]=="v":
            return int(registro[1])+2
        if registro[0] == "a":
            return int(registro[1]) + 4
        if (registro[0]=="t")and (int(registro[1])<=7):
            return int(registro[1])+8
        if registro[0]=="s":
            return int(registro[1])+16
        if registro=="ra":
            return 31
        if (registro[0]=="t")and (int(registro[1])>7):
            return int(registro[1])+16"""

    def getRegistro(self,registro):
        return self.registros[registro]

    def setRegistro(self,registro,valor):
        self.registros[registro]=valor
    def getRegistros(self):
        return self.registros