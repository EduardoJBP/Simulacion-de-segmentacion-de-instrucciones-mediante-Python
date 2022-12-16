from CPU import CPU

txt=input("Indique el nombre de su fichero txt sin incluir la extensión \".txt\" ")

cpu =CPU(txt)
cpu.ejecutarInstrucciones()
print("FIN EJECUCIÓN")

print("-------------------------------------------------------")
print("Valores del banco de Registros:")
bancoRegistro,memoriaDatos=cpu.getBancoYmemoria()

for i in bancoRegistro.getRegistros():
        print("Reg $"+i+" valor %d" %bancoRegistro.getRegistro(i))
print("-------------------------------------------------------")
print("Valores de Memoria de datos:")
for i in memoriaDatos.getDatos():
        print(memoriaDatos.getDato(i))