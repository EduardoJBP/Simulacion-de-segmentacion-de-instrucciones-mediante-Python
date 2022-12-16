class ALU:

    def __init__(self): #Inicializamos las variables, zero se activará cuando "resultado"==0
        self.resultado = 0
        self.zero = 0
        self.a = ""
        self.b = ""
        self.operacion = ""

    def operar(self,a,b,operacion): #Ejecutamos la operación
        self.a=a
        self.b=b
        self.operacion=operacion
        if self.operacion=="=":
            self.resultado = (a == b)
        if self.operacion=="+":
            self.resultado =(a + b)
        if self.operacion=="-":
            self.resultado =(a - b)
            if self.resultado==0:
                self.zero=1
        return self.resultado,self.zero
