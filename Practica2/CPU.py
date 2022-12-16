from LeerTxt import LeerTxt
from MemoriaInstrucciones import MemoriaInstrucciones
from BancoRegistros import BancoRegistros
from Instruccion import Instruccion
from MemoriaDatos import MemoriaDatos
from ALU import ALU
from Control import Control
from AluControl import AluControl


class CPU:

    def __init__(self, nombretxt):
        self.txt = LeerTxt(nombretxt)
        self.memoriaInstrucciones = MemoriaInstrucciones(self.txt.getLista())
        self.bancoRegistro = BancoRegistros()
        self.memoriaDatos = MemoriaDatos()
        #----------------------------Si se desea inicializar datos en la memoria de datos hacerlo en este bloque
        self.memoriaDatos.setDato(0, 10)  # inicializamos en la posicion cero de la memoria de datos un 10
        #----------------------------
        self.alu = ALU()
        self.aluControl = AluControl()
        self.control = Control()
        # self.instruccionSinD = ""

        # Representa el registro de acoplamiento IF/ID
        self.registroD1 = ""

        # Representa el registro de acoplamiento ID/EX
        self.registroD2 = [0, 0, 0, 0, ""]  # src1,src2,desplazamiento,inmedaito,señal,instruccionD, PC, Rd
        self.registroD2.append(Instruccion())
        self.registroD2.append(0)
        self.registroD2.append(0)

        # Representa el registro de acoplamiento EX/MEM
        self.registroD3 = [0, 0, 0, ""]  # zero,resultado,src2,señal,instruccionD, PC, Rd
        self.registroD3.append(Instruccion())
        self.registroD3.append(0)
        self.registroD3.append(0)

        # Representa el registro de acoplamiento MEM/WB
        self.registroD4 = [0, 0, ""]  # resultadoMem,resultadoAlu,señal,instruccionD, PC, Rd
        self.registroD4.append(Instruccion())
        self.registroD4.append(0)
        self.registroD4.append(0)

        self.señalBurbuja = ""  # Señal que se activa cuando hay una burbuja
        self.señalAux = 1  # Señal que se activa cuando ha habido una burbuja, evita que se ejecuten instrucciones erróneas
        self.ciclosPrograma = 1  # Señal que avisa a la CPU cuando termine de hacer el último WB
        self.ciclo = -1  # Nos indicará el ciclo en el que se encuentra
        self.PC = 0  # Indicará el PC

    def IF(self, pc, memoriaInstrucciones):  # devuelve la instruccion en formato string

        print("Realizando instruction fetch(IF) de instrucción: %d" % pc)
        print("PC se incrementa en fase IF")
        print("La instruccion sin decodificar es: " + memoriaInstrucciones.getBanco_Instrucciones()[pc])
        return memoriaInstrucciones.getBanco_Instrucciones()[pc]

    def ID(self, instruccion, bancoRegistro, control,
           pc):  # devuelve un tipo instruccion ya decodificada junto a los valores de los registros y las señales de control
        print("Realizando decodificacion de instrucción(ID): %d" % pc)
        aux = Instruccion()
        aux.decodificarInstruccion(instruccion)

        return aux, bancoRegistro.getRegistro(aux.getRd()), bancoRegistro.getRegistro(
            aux.getSrc1()), bancoRegistro.getRegistro(
            aux.getSrc2()), aux.getDesplazamiento(), aux.getInmediato(), control.getSeñales(
            aux), aux.getEtiqueta()  # devuelve la instruccion, el valor de RD Rsrc1 y Rsrc2

    def EX(self, instruccionD, srC1, srC2, inmediato, desplazamiento, alu, señalesControl,
           pc):  # primero obtenemos la operación a realizar con aluControl y por último la reealizamos

        print("Realizando fase EX de instrucción %d" % pc)
        if señalesControl[
            1] == "0":  # si AluSrc vale 0 entonces hacemos operación de alu con el valor de los dos registros
            operacion = self.aluControl.getOperacion(señalesControl[7] + señalesControl[8], instruccionD)
            resultado, cero = alu.operar(srC1, srC2, operacion)
            print("Operacion a realizar es: " + str(srC1) + operacion + str(srC2))
            print("El resultado es: %d" % resultado)
            print(" AluSrc=" + señalesControl[1])

        elif señalesControl[
            1] == "1":  # si AluSrc vale 1 entonces hacemos operación de alu con el valor o bien del inmedaito o bien del desplazamiento desplazado
            print(" AluSrc=" + señalesControl[1])
            operacion = self.aluControl.getOperacion(señalesControl[7] + señalesControl[8], instruccionD)
            if desplazamiento == -1:  # si no tiene desplazamiento hacemos la operacion con el inmediato
                resultado, cero = alu.operar(srC1, inmediato, operacion)
                print("Operacion a realizar es: " + str(srC1) + operacion + str(inmediato))
                print("El resultado es: %d" % resultado)
            elif inmediato == -1:
                resultado, cero = alu.operar(srC1, desplazamiento, operacion)
                print("Operacion a realizar es: " + str(srC1) + operacion + str(desplazamiento))
                print("El resultado es: %d" % resultado)
        # si no tiene esa fase espera
        if señalesControl[1] == "-":
            print("La instruccion %d" % pc + " No tiene fase EX")
            resultado = ""
            cero = ""
        print("Fase EX de instrucción %d" % pc + " terminada")

        return resultado, cero

    def MEM(self, memoriaDatos, direccion, dato, señalesControl,
            PC):  # si mem write es 1 escribiremos el dato en la direccion calculada por la Alu, en caso copntrario devolveremos el dato que esta en esa posicion

        print("Realizando fase MEM de instruccion %d" % PC)

        if señalesControl[4] + señalesControl[5] == "00":
            print("La instruccion %d" % PC + " No tiene fase MEM")
            print("fase MEM terminada de instruccion %d" % PC)
            return ""
        elif señalesControl[4] == "1":
            print(" MemRead= 1 y MemWrite= 0")
            dato = memoriaDatos.getDato(direccion)
            print("el dato obtenido de la dirección " + str(direccion) + " de memoria es: %d" % dato)
            print("fase MEM terminada de instruccion %d" % PC)
        elif señalesControl[5] == "1":
            print(" MemRead= 0 y MemWrite= 1")
            memoriaDatos.setDato(direccion, dato)
            print("Se ha escrito en posicion %d" % direccion + " el valor %d" % dato)
            print("fase MEM terminada de instruccion %d" % PC)
            return ""
        else:
            print("La instruccion %d" % PC + " No tiene fase MEM")
            print("fase MEM terminada de instruccion %d" % PC)
            return ""
        return dato

    def WB(self, datoMem, resultado, bancoRegistro, señalesControl, instruccionD, PC):
        print("Realizando fase WB de instruccion %d" % PC)

        if señalesControl[2] == "1" and señalesControl[3] == "1":
            print(" MemToReg= 1 y RegWrite= 1")
            if señalesControl[0] == "1":
                print(" RegDest= 1")
                print("Escribiendo dato de la memoria: " + str(datoMem) + " en registro " + instruccionD.getRd())
                bancoRegistro.setRegistro(instruccionD.getRd(), datoMem)

            elif señalesControl[0] == "0":
                print(" RegDest= 0")
                print(
                    "Escribiendo dato de la memoria %d " % datoMem + " en registro " + instruccionD.getRd())  # en teoria es el Src pero en sw lo tengo así
                bancoRegistro.setRegistro(instruccionD.getRd(), datoMem)

        elif señalesControl[2] == "0" and señalesControl[3] == "1" and instruccionD.getOperacion() == "li":
            print(" MemToReg= 0 y RegWrite= 1")
            print(
                "Escribiendo dato inmediato %d" % instruccionD.getInmediato() + " en registro " + instruccionD.getRd())
            bancoRegistro.setRegistro(instruccionD.getRd(), instruccionD.getInmediato())

        elif señalesControl[2] == "0" and señalesControl[
            3] == "1":  # elif señalesControl[2]=="0" and señalesControl[3]=="1" and instruccionD.getOperacion()=="addi":
            print(" MemToReg= 0 y RegWrite= 1")
            print("Escribiendo dato de la ALU %d" % resultado + " en registro " + instruccionD.getRd())
            bancoRegistro.setRegistro(instruccionD.getRd(), resultado)
        else:
            print("La instruccion %d" % PC + " No tiene fase WB")

    def forwardingUnit(self, registro2, registro3, registro4):
        if registro2[5].getOperacion() != "sw" and registro2[5].getOperacion() != "lw" and registro2[
            5].getOperacion() != "li":
            if registro2[5].getSrc1() == registro4[3].getRd() and registro2[5].getSrc1() != "zero":
                if registro4[3].getOperacion() == "lw":
                    registro2[0] = registro4[0]
                    print("Se actualiza valor de src1 con valor de memoria de instruccion LW")
                elif registro4[3].getOperacion() == "li":
                    registro2[0] = registro4[3].getInmediato()
                    print("Se actualiza valor de src1 con valor inmediato de li")
                else:
                    registro2[0] = registro4[1]
                    print("Se actualiza valor de src1 con valor en registro de acoplamiento MEM/WB")
            elif registro2[5].getSrc1() == registro3[4].getRd() and registro2[5].getSrc1() != "zero":
                if registro3[4].getOperacion() == "lw":
                    print("Se realiza burbuja por RAW")
                    return "burbuja"

                elif registro3[4].getOperacion() == "li":
                    print("Se actualiza valor de src1 con valor inmediato de li de registro acoplamiento EX/MEM")
                    registro2[0] = registro3[4].getInmediato()

                else:
                    print("Se actualiza valor de src1 con valor de la ALU")
                    registro2[0] = registro3[1]

            if registro2[5].getSrc2() == registro4[3].getRd() and registro2[
                5].getSrc2() != "zero":
                if registro4[3].getOperacion() == "lw":
                    registro2[1] = registro4[0]
                    print("Se actualiza valor de src2 con valor de memoria de instruccion LW")
                elif registro4[3].getOperacion() == "li":
                    registro2[1] = registro4[3].getInmediato()
                    print("Se actualiza valor de src2 con valor inmediato de li")
                else:
                    registro2[1] = registro4[1]
                    print("Se actualiza valor de src2 con valor en registro de acoplamiento MEM/WB")

            elif registro2[5].getSrc2() == registro3[4].getRd() and registro2[5].getSrc2() != "zero":
                if registro3[4].getOperacion() == "lw":
                    print("Se realiza burbuja por RAW")
                    return "burbuja"
                elif registro3[4].getOperacion() == "li":
                    print("Se actualiza valor de src2 con valor inmediato de li de registro acoplamiento EX/MEM")
                    registro2[1] = registro3[4].getInmediato()
                else:
                    registro2[1] = registro3[1]
                    print("Se actualiza valor de src2 con valor de la ALU")

        elif registro2[5].getOperacion() == "sw":
            if registro2[5].getRd() == registro3[4].getRd() and registro2[5].getSrc1() != "zero":
                if registro3[4].getOperacion() == "li":
                    print("Se actualiza src1 con valor inmediato de li")
                    registro2[7] = registro3[4].getInmediato()
                elif registro3[4].getOperacion() == "lw":
                    print("HAY QUE USAR FORWARDING UNIT EN EX")
                else:
                    print("Se actualiza src1 con valor de ALU")
                    registro2[7] = registro3[1]

            elif registro2[5].getRd() == registro4[3].getRd() and registro2[5].getRd() != "zero":
                if registro4[3].getOperacion() == "lw":
                    registro2[7] = registro4[0]
                    print("Se actualiza valor de rD con valor de MEM/WB de lw")
                elif registro4[3].getOperacion() != "sw":
                    registro2[7] = registro4[1]

    def vaciarRegistros(self, registro1, registro2):
        registro2 = [0, 0, 0, 0, "", Instruccion(), 0, 0]
        registro1 = ""
        return registro1, registro2

    def ejecutarInstrucciones(self):
        while self.ciclosPrograma == 1:
            self.ciclo = self.ciclo + 1
            print("Está en el ciclo: %d" % self.ciclo)
            if self.registroD4[3].getEtapa() == "WB":#si la etapa en la que se encuentra es la de wb pasa a este concional
                self.WB(self.registroD4[0], self.registroD4[1], self.bancoRegistro, self.registroD4[2],
                        self.registroD4[3], self.registroD4[4])
                if self.registroD4[4] == len(self.memoriaInstrucciones.getBanco_Instrucciones()) - 1:
                    self.ciclosPrograma = 0#Si se realiza el WB de la última instrucción se termina la ejecución del programa
                self.registroD4[3].setEtapa("ID")

            if self.registroD3[4].getEtapa() == "MEM" and self.ciclosPrograma != 0:#si la etapa en la que se encuentra es la de MEM pasa a este concional
                # Se asignan los valores al siguiente registro MEM/WB
                self.registroD4[0] = self.MEM(self.memoriaDatos, self.registroD3[1], self.registroD3[6],
                                              self.registroD3[3], self.registroD3[5])
                self.registroD4[1] = self.registroD3[1]
                self.registroD4[2] = self.registroD3[3]
                self.registroD3[4].setEtapa("WB")
                self.registroD4[3] = self.registroD3[4]
                self.registroD4[4] = self.registroD3[5]
                if self.señalBurbuja == "burbuja":#si la señal devuelta es burbuja, se resetean los registros y se pone de etapa la etapa ID de la instrucción del registro ID/EX
                    self.registroD2[5].setEtapa("ID")
                    self.registroD3 = [0, 0, 0, "", Instruccion(), 0, 0]
                    self.PC = self.PC - 1
                    self.registroD1 = registroD1aux #se pone de valor en el registro IF/ID el valor de la anterior instruccion
                print("Cargando datos de la Memoria y de registro acople EX/MEM a registro de acople MEM/WB")

            if self.registroD2[5].getEtapa() == "EX" and self.ciclosPrograma != 0:#si la etapa en la que se encuentra es la de EX pasa a este concional
                # Se asignan los valores al siguiente registro, EX/MEM
                self.registroD3[1], self.registroD3[0] = self.EX(self.registroD2[5], self.registroD2[0],
                                                                 self.registroD2[1], self.registroD2[3],
                                                                 self.registroD2[2], self.alu, self.registroD2[4],
                                                                 self.registroD2[6])
                self.registroD2[5].setEtapa("MEM")
                self.registroD3[4] = self.registroD2[5]
                self.registroD3[3] = self.registroD2[4]
                self.registroD3[2] = self.registroD2[1]
                self.registroD3[5] = self.registroD2[6]
                self.registroD3[6] = self.registroD2[7]
                print("Cargando datos de la ALU y de registro de acople ID/EX en registro acople EX/MEM")

                if self.registroD3[5] == len(self.memoriaInstrucciones.getBanco_Instrucciones()) - 1:
                    self.señalAux = 0  # si es la ultima instruccion no entra a la decodificacion e instruction Fetch de otra, esta señal me permite controalr los casos en lso que hay burbuja y los de salto
                if self.registroD3[3][6] == "1" and self.registroD3[0] == 1:
                    self.PC = self.memoriaInstrucciones.getEtiquetas()[etiqueta]
                    print(
                        "El valor de Branch es 1 y el de cero(BEQ) es 1 == PcSource=1, se calcula nuevo PC sumando con dir de etiqueta desplazada")
                    print("El valor del PC es: %d" % self.PC)
                    self.registroD1, self.registroD2 = self.vaciarRegistros(self.registroD1, self.registroD2)
                    self.señalAux = 1
                elif self.registroD3[3][6] == "-":
                    print(
                        "El valor de FuentePC es 1, se actualiza PC a dir de etiqueta de salto incondicional: " + etiqueta)
                    self.PC = self.memoriaInstrucciones.getEtiquetas()[etiqueta]
                    self.registroD1, self.registroD2 = self.vaciarRegistros(self.registroD1, self.registroD2)
                    self.señalAux = 1
                    print("El valor del PC es: %d" % self.PC)

            if self.PC - 1 < len(self.memoriaInstrucciones.getBanco_Instrucciones()) and self.ciclosPrograma != 0 and self.señalAux != 0:#si la etapa en la que se encuentra es la de ID pasa a este concional
                if self.memoriaInstrucciones.getBanco_Instrucciones()[self.PC - 1] == self.registroD1:
                    self.registroD2[6] = self.PC - 1 #el PC se resta porque está apuntando a la siguiente instrucción, por ejemplo, en la decodificacion de la instruccion 0 el PC vale 1
                    self.registroD2[5], self.registroD2[7], self.registroD2[0], self.registroD2[1], self.registroD2[2], \
                    self.registroD2[3], self.registroD2[4], etiqueta = self.ID(self.registroD1, self.bancoRegistro,
                                                                               self.control, self.registroD2[6])
                    self.registroD2[5].setEtapa("EX")

                    self.señalBurbuja = self.forwardingUnit(self.registroD2, self.registroD3, self.registroD4)

            if self.PC < len(
                    # Se asignan los valores al registro IF/ID
                    self.memoriaInstrucciones.getBanco_Instrucciones()) and self.ciclosPrograma != 0 and self.señalAux != 0:#si la etapa en la que se encuentra es la de IF pasa a este concional
                registroD1aux = self.registroD1
                self.registroD1 = self.IF(self.PC, self.memoriaInstrucciones)
                print("Cargando datos en registro de acople IF/ID")
                self.PC = self.PC + 1

    def getBancoYmemoria(self):
        return self.bancoRegistro, self.memoriaDatos
