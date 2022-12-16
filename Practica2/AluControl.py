class AluControl:
    def __init__(self):
        self.operacion=""

    def getOperacion(self,aluOp,instruccion): #La operación que recibirá la ALU dependerá de AluControl
        if aluOp=="00" or (aluOp=="11" and instruccion.getOperacion()=="add"):
            self.operacion="+"
        elif aluOp=="01":
            self.operacion="-"
        elif aluOp=="11" and instruccion.getOperacion()=="sub":
            self.operacion="-"
        return self.operacion