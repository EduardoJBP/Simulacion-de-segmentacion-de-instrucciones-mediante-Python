class Control:
    señales=""
    def __init__(self): #inicializamos la variable
        self.señales = ""

    def getSeñales(self,instruccion): #Dependiento que la instrucción las señales de control tendrán un valor u otro
        if instruccion.getTipo()=="R":  # r-format
            self.señales="100100011"
        elif instruccion.getOperacion() == "lw":
            self.señales="011110000"
        elif instruccion.getOperacion() == "sw":  # sw
            self.señales = "-1-001000"
        elif instruccion.getOperacion() == "beq":  # beq
            self.señales = "-0----101"
        elif instruccion.getOperacion()=="j":
            self.señales="---000---"
        elif instruccion.getOperacion()=="addi":
            self.señales="010100000"
        elif instruccion.getOperacion() == "li":
            self.señales = "0-01--0--"
        return self.señales
        #orden de bits
    #RegDest -->señales[0]
    #AluSrc -->señales[1]
    #MemToReg -->señales[2]
    #RegWrite -->señales[3]
    #MemRead -->señales[4]
    #MemWrite -->señales[5]
    #Branch -->señales[6]
    #AluOp //2 bits del final señales[7-8]

