class LeerTxt:
    lista=[]
    def __init__(self,aux):
        f = open(aux+".txt", "r")
        self.lista = f.readlines()
        f.close()
    def getLista(self):
        return self.lista
