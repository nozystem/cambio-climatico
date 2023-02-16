# como hemos separado las funciones en otro archivo para usar las funciones tenemos que importar el archivo
#  de funciones para ello hacemos import + el nombre del archivo sin la estension(.py)
import canvi_climatic_gava_funciones
import sys

#hacemos una lista con todos los comandos que se podran utilizar para indicarle que si no coincide con 
# ninguno de estos envie un mensaje de error
estudios=["help", "estudi1", "estudi2", "estudi3","estudi4", "estudi5", "estudi6", "estudi7", "estudi8"]
# definimos que la variable comanda sera el parametro 1 que insertaras en la terminal
comanda = sys.argv[1]
# si la comanda insertada en la terminal coincide con alguno de los elementos de la lista hara lo que
#  le pida cada elemento
if comanda in estudios:
    # si la comanda es igual a help te mostrara todos los estudios disponibles para poder saber 
    # cual quieres ejecutar
    if comanda == "help":
        print("Estudis disponibles per veure: ")
        print("estudi1 : grafico de las temperaturas maximas de los ultimos años")
        print("estudi2 : grafico de las temperaturas minimas de los ultimos años")
        print("estudi3 : grafico de las temperaturas maximas y minimas de los ultimos años")
        print("estudi4 : grafico de las temperaturas medias de los ultimos años")
        print("estudi5 : grafico de las temperaturas medias maximas de los ultimos años")
        print("estudi6 : grafico de las temperaturas medias minimas de los ultimos años")
        print("estudi7 : grafico de las temperaturas medias maximas y minimas de los ultimos años")
        print("estudi8 : grafico de los dias de lluvia de los ultimos años")
    # si es alguno de los estudios te mostrara el grafico que le corresponda
    if comanda == "estudi1":
        #para llamar a una funcion que esta en otro archivo despues de 
        # hacer el import de ese archivo ponemos el nombre de el archivo seguido de un . con el nombre de la funcion
        print(canvi_climatic_gava_funciones.estudi1('2010',"2022"))
    if comanda == "estudi2":
        print(canvi_climatic_gava_funciones.estudi2('2010',"2022"))
    if comanda == "estudi3":
        print(canvi_climatic_gava_funciones.estudi3('2010',"2022"))
    if comanda == "estudi4":
        print(canvi_climatic_gava_funciones.estudi4('2010',"2022"))
    if comanda == "estudi5":
        print(canvi_climatic_gava_funciones.estudi5('2010',"2022"))
    if comanda == "estudi6":
        print(canvi_climatic_gava_funciones.estudi6('2010',"2022"))
    if comanda == "estudi7":
        print(canvi_climatic_gava_funciones.estudi7('2010',"2022"))
    if comanda == "estudi8":
        print(canvi_climatic_gava_funciones.estudi8('2010',"2022"))
# si no coincide con ninguno de los elementos de la lista nos enviara un mensaje de error sobre no es un parametro valido
else:
    print("ERROR: No es un parametro valido")
    
