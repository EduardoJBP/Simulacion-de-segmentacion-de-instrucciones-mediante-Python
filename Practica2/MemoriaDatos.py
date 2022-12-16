#va a ser un mapa, cada posición representará una palabra en la memoria de datos, tendremos una memoria de 32 posiciones, los desplazamientos de las instrucciones deberán ser
#multiplo de 4, siendo un desplazamiendo 4 una palabra, 8 dos palabras etc...
#inicializar todas las posiciones a cero



class MemoriaDatos:
    posiciones = {}

    def __init__(self):
        for i in range(32):
            self.posiciones[i]=0

    def getDato(self,registro):
        return self.posiciones[registro]

    def setDato(self,posicion,dato):
        self.posiciones[posicion]= dato
    def getDatos(self):
        return self.posiciones