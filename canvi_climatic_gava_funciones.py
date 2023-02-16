import requests
import json
import matplotlib.pyplot as plt
import numpy as np

 # Funcion para generar url de la API
def generaURL (startYear, endYear):
    # Le pasamos por parametros el año de principio y final para
    # generar una URL depende el rango que queramos generar
    restUrl="https://archive-api.open-meteo.com/v1/archive?latitude=52.52&longitude=13.41&start_date="+startYear+"-01-01&end_date="+endYear+"-12-30&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=Europe%2FLondon"
    return restUrl

def peticionAPI(startYear, endYear):
    # A partir de la libreria Request le hacemos una peticion a la
    # api que la guardamos en una variable pero en formato texto
    respostaREST=requests.get(generaURL(startYear, endYear))

    return respostaREST.text

def listaDatos(startYear, endYear):
    # La respuesta de la api la convertimos a formato JSON de forma
    # que despues podamos interactuar con ella como si fuese un diccionario
    dades=json.loads(peticionAPI(startYear, endYear))

    # Separamos los datos en variables para poder tratar la informacion mas
    # adelante en otras funciones
    tempMax = (dades["daily"]["temperature_2m_max"])
    tempMin = (dades["daily"]["temperature_2m_min"])
    lluvia = (dades["daily"]["precipitation_sum"])
    time = dades["daily"]["time"]

    return tempMin , tempMax, lluvia, time

 # Funcion donde recorremos la lista de fechas y separamos por años
def anyRecorriendo(startYear, endYear):
    # de la funcion de datos me traigo los datos de la lista de años que son
    # los que me interesan y voy a utilizar
    __ , __, __, lista = listaDatos(startYear, endYear)


    contador = 0 # Contador para saber el dia en que cambia de año
    any = [] # Lista con los años que recorremos ['2020','2021','2022']
    indices = [] # Lista con los Indices donde empieza cada año ['0','365','730']

    # Bucle donde recorremos la lista de años (formato ['2020-01-01', '2020-01-02', '2020-01-03'])
    # nos quedamos solamente con el año haciendo un split, y sumamos 1 al contador porque ha pasado
    # un dia.
    for i in lista:
        anyIndividual = lista[contador].split('-')
        contador += 1

        # Creamos una condicion en la que vamos a comprobar si el numero que estamos recorriendo esta
        # dentro de la lista, de manera que, si 2020 no esta en la lista lo añade, recorre los 364 dias
        # restantes de ese año y cuando cambia a 2021 la condicion se cumple (No esta en la lista) y lo
        # añade a la lista años. A la vez, como esto solo se ejecuta una vez cuando cambia de año, añadimos
        # el contador que en esa iteracion es el dia en el que cambia de año
        if anyIndividual[0] not in any:
            any.append(anyIndividual[0])
            indices.append(contador)

    # Este append es super importante porque nos añade la ultima posicion de la lista que vamos a necesitar
    # para mas adelante recorrer y crear las listas separadas con las temperaturas o valores de cada año   
    indices.append(contador)
    return indices, any

    # En esta funcion separamos la lista con todas las temperaturas (por ejemplo 730 para 2 años) en listas mas
    # pequeñas para cada año

def temperaturaAny(startYear, endYear):
    # Nos traemos los datos que queremos separar
    tempMin, tempMax, lluvia, __ = list(listaDatos(startYear, endYear))
    contador, any = list(anyRecorriendo(startYear, endYear))

    # Aqui lo que vamos a hacer es que vamos a recorrer la lista desde una posicion hasta otra posicion, y por cada
    # vez vamos a añadir esos valores a una lista, que a su vez va a estar dentro de una lista mayor.
    # listaMaxAnual = [[365 temperaturas año1], [365 temperaturas año2], [365 temperaturas año3]] 
    # para hacer eso tempMax[contador[1]:contador[i + 1]] contador[1] va a valer 0 la primera vez y 
    # contador[i + 1] va a valer 365, y asi hasta que termine todos los indices de cambios de año
    listaMaxAnual = [tempMax[contador[i]:contador[i + 1]] for i in range(len(any))]
    listaMinAnual = [tempMin[contador[i]:contador[i + 1]] for i in range(len(any))]
    listalluviaAnual = [lluvia[contador[i]:contador[i + 1]] for i in range(len(any))]

    return listaMaxAnual, listaMinAnual, listalluviaAnual

 # Funcion para calcular las temperaturas maximas y minimas de un año
def temperatura_min_max(startYear, endYear):
    # Nos traemos la lista con las sublistas de datos separados por año
    tempMax, tempMin, listalluviaAnual= temperaturaAny(startYear, endYear)
    resultat_min = [] # Array donde guardamos temperaturas minimas.
    resultat_max = [] # Array donde guardamos temperaturas maximas.
    min = 100 # Variable con un numero elevado para que cuando compare siempre sea mas bajo.
    max = 0   # Variable con un numero bajo para que cuando compare siempre sea mas elevado.
    contador = 0 # Contador para recorrer las sublistas de la lista.

    # Bucle donde vamos a recorrer las temperaturas minimas y maximas de cada año, tantas veces
    # como temperaturas minimas tengamos ya que la longitud de las dos listas son iguales.
    for contador in range(len(tempMin)):

        # Recorremos las temperaturas minimas y dentro del bucle se compara cada iteracion si la
        # temperatura es mas baja, si la condicion se cumple se le asigna a una variable; Lo mismo
        # a la inversa para las temperaturas maximas.
        for iMin in tempMin[contador]: 
            if iMin < min:
                min = iMin
        for iMax in tempMax[contador]:
            if iMax > max:
                max = iMax

        contador += 1 # Cada vez que se ejecute el bucle for contador in range el contador se va a sumar 1
                      # de manera que pasara a recorrer la siguiente sublista.

        resultat_min.append(min) # por cada vez que el bucle for contador in range se ejecute se va a añadir
        resultat_max.append(max) # a las listas el valor de la variable de manera que por cada año vamos a
                                 # asignar una vez la variable/temperatura.
        min = 100 # Asignamos las viarbles a 0 para reiniciar sus valores y que despues de vuelvan a reasignar
        max = 0   # con los valores mas altos/bajos
    return resultat_max, resultat_min

 # Esta funcion se encarga de verificar si un dia de verdad ha llovio o no siendo el minimo requisito para 
 # considerarlo dia de lluvia 4mm
def filtroLluvia(startYear, endYear):
    __, __, lluvia = (temperaturaAny(startYear, endYear)) # Nos traemos los datos de lluvia
    iany = 0 # Contador de los años que hemos recorrido de las sublistas
    diasLluvia = 0 # contador donde sumamos cuando un dia pasa el filtro de los 4mm 
    diasLluviaany = []

    # recorremos la lista de sublistas y por cada año
    for iany in range(len(lluvia)):
        for i in lluvia[iany]:
            if i >= 4: # Filtro que comprueba si se cumple la condicion de los 4mm
                diasLluvia +=1 # si se cumple la condicion sumamos un dia de lluvia
        iany +=1
        diasLluviaany.append(diasLluvia) # por cada año que pasa añadimos el valor a una lista
        diasLluvia=0 # reiniciamos los dias de lluvia para el nuevo año a calcular
    return diasLluviaany

def calcularMedia(startYear, endYear, temperaturas):
    temperatura = temperaturas
    media = []
    suma = 0
    contador = 0
    division = 0
    for contador in range(len(temperatura)):
        for i in temperatura[contador]:
            suma += i
            division += 1
        resultado = suma / division
        resultado = int(resultado *100)/100
        media.append(resultado)
        suma = 0
        division = 0
        contador += 1

    return media

def mediaTemperaturaMax(startYear, endYear):
    maxLista, minLista, lluvia=temperaturaAny(startYear, endYear)
    max = calcularMedia(startYear, endYear, maxLista)
    min = calcularMedia(startYear, endYear, minLista)
    contador = 0
    media = 0
    resultadoMedia =[]
    for i in max:
        media = (min[contador] + max[contador]) / 2
        media = int(media *100)/100
        resultadoMedia.append(media)
        contador += 1
        media= 0
    return resultadoMedia

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------- GRAFICOS -------------------------------------------------------


def estudi1 (startYear, endYear):
    #cogemos los datos de temperatura maxima de cada any y la guardamos en tempMax
    tempMin, tempMax= temperatura_min_max(startYear, endYear)
    # y como tambien necesitamos los anys de los que cogemos la temperatura hacemos lo mismo
    indices, any = (anyRecorriendo(startYear, endYear))
    fig, ax = plt.subplots()
    #definimos que datos queremos que salga en el grafico, los anys como la x y el tempMax seran los datos que se 
    # muestren la linea y ademas cambiamos el color de la linea por el rojo
    ax.plot(any, tempMax, label="TempMax", color = "red")
    ax.legend()
    ax.set_title("Grafico de las temperaturas maximas de los ultimos años")
    #guardamos en una variable cuando se ejecuta el grafico y se lo ponemos al return
    graficoTempMax = plt.show()
    return graficoTempMax

def estudi2(startYear, endYear):
    #cogemos los datps de temperatura minima de su funcion y tambien los anys para definirlos en el grafico 
    # de otra funcion
    tempMax, tempMin = temperatura_min_max(startYear, endYear)
    indices, any = (anyRecorriendo(startYear, endYear))
    fig, ax = plt.subplots()
    #definimos que datos queremos que salga en el grafico, los anys como la x y el tempMin seran los datos que se 
    # muestren la linea y ademas cambiamos el color de la linea por el azul flojo
    ax.plot(any, tempMin, label="TempMin", color = "blue")
    ax.legend()
    ax.set_title("Grafico de las temperaturas minimas de los ultimos años")
    # para  mostrar el grafico lo asignamos a una variable y lo definimos como return
    graficoTempMin= plt.show()

    return graficoTempMin
def estudi3 (startYear, endYear):
    tempMax, tempMin = temperatura_min_max(startYear, endYear)
    indices, any = (anyRecorriendo(startYear, endYear))
    fig, ax = plt.subplots()
    #definimos que datos queremos que salga en el grafico, los anys como la x y el tempMin seran los datos que se 
    # muestren la linea y ademas cambiamos el color de la linea por el azul flojo
    ax.plot(any,tempMax,label="TempMax", color= "red" )
    ax.plot(any, tempMin, label="TempMin", color = "blue")
    
    ax.legend()
    ax.set_title("Grafico de las temperaturas maximas y minimas de los ultimos años")
    graficoTempMinYMax= plt.show()
    return graficoTempMinYMax
def estudi4 (startYear, endYear):
    # cogemos los datos de temperatura de otra funcion creada anteriormente y lo guardamos en la variable
    temperatura = mediaTemperaturaMax(startYear, endYear)
    # y tambien cogemos los datos de los anys para definirlos en el grafico
    indices, any = anyRecorriendo(startYear, endYear)
    fig, ax = plt.subplots()
    plt.ylim([0, 20])
    #definimos que graficos se tienen que mostrar
    ax.stackplot(any, temperatura, alpha=0.8)
    #definimos titulos
    ax.set_title("Media de las temperaturas de los ultimos años")
    ax.set_xlabel("año")
    #definimos una variable para devolverlo en el return
   
    graficoMediaTemp= plt.show()
    return graficoMediaTemp
def estudi5 (startYear, endYear):
    maxLista, minLista, lluvia=temperaturaAny(startYear, endYear)
    TMax = calcularMedia(startYear, endYear, maxLista)
    indices, any = (anyRecorriendo(startYear, endYear))
    fig, ax = plt.subplots()
    #definimos que graficos se tienen que mostrar
    ax.stackplot(any, TMax, alpha=0.8, color = "#C95052")
    #definimos titulos
    ax.set_title("Media de las temperaturas maxima de los ultimos años")
    ax.set_xlabel("año")
    #definimos una variable para devolverlo en el return
    graficoMediaTempMax= plt.show()

    return graficoMediaTempMax
def estudi6(startYear, endYear):
    maxLista, minLista, lluvia=temperaturaAny(startYear, endYear)
    TMin = calcularMedia(startYear, endYear, minLista)
    indices, any = (anyRecorriendo(startYear, endYear))
    fig, ax = plt.subplots()
    #definimos que graficos se tienen que mostrar
    ax.stackplot(any, TMin, alpha=0.8, color = "#92ffe6")
    #definimos titulos
    ax.set_title("Media de las temperaturas minima de los ultimos años")
    ax.set_xlabel("año")
    #definimos una variable para devolverlo en el return
    graficoMediaTempMin= plt.show()
    return graficoMediaTempMin
def estudi7 (startYear, endYear):
    maxLista, minLista, lluvia=temperaturaAny(startYear, endYear)
    TMin = calcularMedia(startYear, endYear, minLista)
    TMax = calcularMedia(startYear, endYear, maxLista)
    indices, any = (anyRecorriendo(startYear, endYear))
    fig, ax = plt.subplots()
    #definimos que graficos se tienen que mostrar
    ax.stackplot(any, TMin, alpha=0.9, color = "blue", zorder= 10)
    ax.stackplot(any, TMax, alpha=0.8, color = "red", zorder= 5)
    #definimos titulos
    ax.set_title("Media de las temperaturas maxima y minima de los ultimos años")
    ax.set_xlabel("año")
    #definimos una variable para devolverlo en el return
    graficoMediaTempMinYMax= plt.show()
    return graficoMediaTempMinYMax
def estudi8 (startYear, endYear):
    #cogemos los datos de los dias que ha llovido cada any de la funcion anterior 
    lluvias = filtroLluvia(startYear, endYear)
    #Y los anys para ponerlos en la barra del grafico
    indices, any = (anyRecorriendo(startYear, endYear))
    # le indicamos que la x sera los anys de que le daremos datos
    x = np.arange(len(any))
    # le definimos el ancho de las barras
    width = 0.20 
    fig, ax = plt.subplots()
    # aqui le definimos que los datos a las barras
    rects1 = ax.bar(x - width/2, lluvias, width)
    # le añadimos un titulo al grafico
    ax.set_title("Dias de lluvia en los últimos años")
    ax.set_xticks(x, any)
    # se las añadimos al grafico
    ax.bar_label(rects1, padding=3)
    fig.tight_layout()
    # creamos una variable para mostrar el grafico
    graficoLluvia= plt.show()
    #y como return le añadimos la variable que muestra el grafico
    return graficoLluvia