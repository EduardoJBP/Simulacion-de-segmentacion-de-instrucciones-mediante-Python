class MemoriaInstrucciones:
    banco_instrucciones=[]
    etiquetas={}
    def __init__(self,instrucciones):#Se lee del fichero txt cada línea, se añaden a la memoria de instrucciones y si se encuentra una etiqueta se almacena
        cont=0
        for i in instrucciones:
            parametros = i.split(sep=",")#tendrá varias posiciones, en la primera se encuentra la posible etiqueta, con la opracion y el primer registro
            aux = parametros[0].split(sep=" ")
            if len(aux)==3:
                etiqueta=aux[0][:-1]
                instruccion=i[len(etiqueta)+2:]
                instruccion= instruccion.replace("\n","")#Quitar todos los \n elimina posibles problemas en el futuro
                self.banco_instrucciones.append(instruccion)
                self.etiquetas[etiqueta]=cont
            else:
                instruccion = i.replace("\n", "")
                self.banco_instrucciones.append(instruccion)
            cont = cont + 1 #Se usa para saber la posicion en la que se encuentra la etiqueta


    def getBanco_Instrucciones(self):
        return self.banco_instrucciones
    def getEtiquetas(self):
        return self.etiquetas
