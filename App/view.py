"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """
from tabulate import tabulate
import config as cf
import sys
import threading
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import map as mp
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Buscar un camino posible entre dos estaciones")
    print("3- Buscar el camino con menos estaciones entre dos estaciones")
    print("4- Reconocer los componentes conectados de la Red de rutas de bus")
    print("5- Planear el camino con distancia mínima entre dos puntos geográficos")
    print("6- Localizar las estaciones “alcanzables” desde un origen a un número máximo de conexiones dado")
    print("7- Buscar el camino con distancia mínima entre una estación de origen y un vecindario de destino")
    print("8- Encontrar un posible camino circular desde una estación de origen")
    print("9- Graficar resultados para cada uno de los requerimientos")
    print("0- Salir")


def printreq1(catalog, idOrigen, idDestino,search_method):
    stack,weight,list_ = controller.caminoPosibleEntreDosEstaciones(catalog, idOrigen, idDestino,search_method)
    print("Numero de estaciónes de camino:",str(st.size(stack))+".") 
    print("Distancia total",str(round(weight,2))+"km.")
    printlist = [["Stop","Distance Next Stop (km)"]]
    transbordos = 0
    i = 1
    while i < lt.size(list_)+2:
        if i != lt.size(list_)+1:
            if 'T' in lt.getElement(stack,i):
                transbordos += 1
            printlist.append([lt.getElement(stack,i),lt.getElement(list_,i)])
        else:
            if 'T' in lt.getElement(stack,i):
                transbordos += 1
            printlist.append([lt.getElement(stack,i),'-'])
        i+=1
    print('El número de transbordos en esta ruta es:', transbordos)
    print(tabulate(printlist,tablefmt="grid"))
            

def printreq2(catalog, idOrigen, idDestino):
    path, weight, list_ = controller.menorCaminoEntreDosEstaciones(catalog, idOrigen, idDestino)
    print("Numero de estaciónes de camino:",str(st.size(path))+".") 
    print("Distancia total",str(round(weight,2))+"km.")
    printlist = [["Stop","Distance Next Stop (km)"]]
    transbordos = 0
    i = 1
    while i < lt.size(list_)+2:
        if i != lt.size(list_)+1:
            if 'T' in lt.getElement(path,i):
                transbordos += 1
            printlist.append([lt.getElement(path,i),lt.getElement(list_,i)])
        else:
            if 'T' in lt.getElement(path,i):
                transbordos += 1
            printlist.append([lt.getElement(path,i),'-'])
        i+=1
    print('El número de transbordos en esta ruta es:', transbordos)
    print(tabulate(printlist,tablefmt="grid"))

def printreq3(catalog):
    sublist,componentes = controller.reconocerComponentesConectadosenlaRed(catalog)
    print("Hay",str(componentes),"componentes conectados.")
    printlist = [["rank","3 ultimos y primeros","cantidad"]]
    rank = 1
    for i in lt.iterator(sublist):
        a = [["Id"]]
        if lt.size(i) >= 6:
            first = lt.subList(i,1,3)
            last = lt.subList(i,lt.size(i)-2,3)
            for c in lt.iterator(first):
                a.append([c])
            for c in lt.iterator(last):
                a.append([c])
        else:
            for c in lt.iterator(i):
                a.append([c])
        printlist.append([rank,tabulate(a,tablefmt="grid"),lt.size(i)])
        rank +=1
    print(tabulate(printlist,tablefmt="grid"))
def printreq4(catalog, lonOrigen, latOrigen, lonDestino, latDestino):
    def_o,def_d,distancia,transbordo,path,lista_distancias = controller.planearCaminoDistanciaMinimaEntrePuntosGeograficos(catalog, lonOrigen, latOrigen, lonDestino, latDestino)
    print("Distancia entre el origen y la estacion mas cercana: "+ str(def_o), "km")
    print("Distancia las estaciones de origen y destino: "+ str(distancia), "km")
    print("Distancia entre el destino y la estacion mas cercana: "+ str(def_d), "km")
    print("Total de estaciones:", str(lt.size(path)))
    print("Total de transbordos:", str(transbordo))
    print("Estaciones que definen el camino:")
    printlist = [["Stop","Distance Next Stop (km)"]]
    transbordos = 0
    i = 1
    while i < lt.size(lista_distancias)+2:
        if i != lt.size(lista_distancias)+1:
            if 'T' in lt.getElement(path,i):
                transbordos += 1
            printlist.append([lt.getElement(path,i),lt.getElement(lista_distancias,i)])
        else:
            if 'T' in lt.getElement(path,i):
                transbordos += 1
            printlist.append([lt.getElement(path,i),'-'])
        i+=1
    print('El número de transbordos en esta ruta es:', transbordos)
    print(tabulate(printlist,tablefmt="grid"))


def printreq5(catalog, idOrigen, nConexionesPermitidas):
    alcanzables, latitudes, longitudes, weights = controller.localizarEstacionesAlcanzables(catalog, idOrigen, nConexionesPermitidas)
    lats, longs, weis = [], [], []
    for i in lt.iterator(latitudes):
        lats.append(i)
    for i in lt.iterator(longitudes):
        longs.append(i)
    for i in lt.iterator(weights):
        weis.append(i)
    print('Estaciones alcanzables:')
    printlist = [['ID', 'Latitud', 'Longitud', 'Peso']]
    pos = 0
    for i in lt.iterator(alcanzables):
        if weis[pos-1] != None:
            if pos < len(lats) and weis[pos] != weis[pos-1]:
                printlist.append([i, lats[pos], longs[pos], weis[pos]])
        pos+=1
    print(tabulate(printlist,tablefmt="grid"))

def printreq6(catalog, idOrigen, idVecindario):
    path,distances_list,weight = controller.menorCaminoEstacionVencindario(catalog, idOrigen, idVecindario)
    print("Numero de estaciónes de camino:",str(lt.size(path))+".") 
    print("Distancia total",str(round(weight,2))+"km.")
    printlist = [["Stop","Distance Next Stop (km)"]]
    i = 1
    while i < lt.size(distances_list)+2:
        if i != lt.size(distances_list)+1:
            printlist.append([lt.getElement(path,i),lt.getElement(distances_list,i)])
        else:
            printlist.append([lt.getElement(path,i),'-'])
        i+=1
    print(tabulate(printlist,tablefmt="grid"))
def printreq7(catalog, idOrigen):
    cycle_path,weight,list_ = controller.caminoCircular(catalog, idOrigen)
    if cycle_path != None:
        t = 0
        for i in lt.iterator(cycle_path):
            if "T" in i:
                t+=1
        print("Numero de estaciónes de camino:",str(st.size(cycle_path))+".") 
        print("Distancia total",str(round(weight,2))+"km.")
        print("Total de transbordos:",t)
        printlist = [["Stop","Distance Next Stop (km)"]]
        i = 1
        while i < lt.size(list_)+2:
            if i != lt.size(list_)+1:
                printlist.append([lt.getElement(cycle_path,i),lt.getElement(list_,i)])
            else:
                printlist.append([lt.getElement(cycle_path,i),'-'])
            i+=1
        print(tabulate(printlist,tablefmt="grid"))
    else:
        print("No hay ciclo.")
def printreq8(catalog):
    pass

"""
Menu principal
"""

def load(catalog):
    pass
def menu():
    catalog = None
    size = "-large"
    search_method = "bfs"
    while True:
        printMenu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs[0]) == 1:
            if catalog == None:
                catalog = controller.newController()
                Total_Stops_File, Total_Edges_File, Total_Estaciones, Total_Rutas_Comparitdas, Total_Rutas_Exclusivas, Total_Rutas, Total_Exclusivas,Total_Transbordo,Total_Arcos,Total_Vertices,Longitud_Maxima,Longitud_Minima,Latitud_Maxima,Latitud_Minima,First_5,Last_5 = controller.loadData(catalog,size)
                printlist = [["Code-Ruta","Longitude","Latitude","Adjacents"]]
                print('Tamaño del archivo CSV Bus-Stops:', Total_Stops_File)
                print('Tamaño del archivo CSV Routes', Total_Edges_File)
                print("- - - Estaciones - - -")
                print("Total de estaciones exclusivas:",str(Total_Exclusivas)+".")
                print("Total de estaciones de transbordo:",str(Total_Transbordo)+".")
                print("Total de estaciones:",str(Total_Estaciones)+".\n")
                print("- - - Rutas - - -")
                print("Total de rutas exclusivas:",str(Total_Rutas_Exclusivas)+".")
                print("Total de rutas de transbordo:",str(Total_Rutas_Comparitdas)+".")
                print("Total de rutas:",str(Total_Rutas)+".")
                print(5*'-','Especificaciones del Grafo',5*'-')
                print("Total de vértices:",str(Total_Vertices)+".")
                print("Total de arcos:",str(Total_Arcos)+".")
                print('Rango del área rectangular de Barcelona:\nLongitud: [',str(Longitud_Minima),',',str(Longitud_Maxima),']\nLatitud: [',str(Latitud_Minima),',',str(Latitud_Maxima),']')
                for i in lt.iterator(First_5):
                    xd = []
                    for e in printlist[0]:
                        xd.append(i[e])
                    printlist.append(xd)
                for i in lt.iterator(Last_5):
                    xd = []
                    for e in printlist[0]:
                        xd.append(i[e])
                    printlist.append(xd)
                print(tabulate(printlist,tablefmt="grid"))
                print("Cargando información de los archivos ....")
                load(catalog)

        elif int(inputs[0]) == 2:
            idOrigen = input("Ingrese idOrigen: ")
            idDestino = input("Ingrese idDestino: ")
            memory1 = controller.getMemory()
            time1 = controller.getTime()
            printreq1(catalog, idOrigen, idDestino,search_method)
            time2 = controller.getTime()
            memory2 = controller.getMemory()
            deltatime = controller.deltaTime(time2, time1)
            deltamemory = controller.deltaMemory(memory2, memory1)
            print('Tiempo de ejecución:', str(deltatime), 'ms.')
            print('Memoria utilizada', deltamemory, 'KB.')

        elif int(inputs[0]) == 3:
            idOrigen = input("Ingrese idOrigen: ")
            idDestino = input("Ingrese idDestino: ")
            memory1 = controller.getMemory()
            time1 = controller.getTime()
            printreq2(catalog, idOrigen, idDestino)
            time2 = controller.getTime()
            memory2 = controller.getMemory()
            deltatime = controller.deltaTime(time2, time1)
            deltamemory = controller.deltaMemory(memory2, memory1)
            print('Tiempo de ejecución:', str(deltatime), 'ms.')
            print('Memoria utilizada', deltamemory, 'KB.')

        elif int(inputs[0]) == 4:
            memory1 = controller.getMemory()
            time1 = controller.getTime()
            printreq3(catalog)
            time2 = controller.getTime()
            memory2 = controller.getMemory()
            deltatime = controller.deltaTime(time2, time1)
            deltamemory = controller.deltaMemory(memory2, memory1)
            print('Tiempo de ejecución:', str(deltatime), 'ms.')
            print('Memoria utilizada', deltamemory, 'KB.')

        elif int(inputs[0]) == 5:
            lonOrigen = input("Ingrese la longitud del origen: ")
            latOrigen = input("Ingrese la latitud del origen: ")
            lonDestino = input("Ingrese la longitud del destino: ")
            latDestino = input("Ingrese la latitud del destino: ")
            memory1 = controller.getMemory()
            time1 = controller.getTime()
            printreq4(catalog, lonOrigen, latOrigen, lonDestino, latDestino)
            time2 = controller.getTime()
            memory2 = controller.getMemory()
            deltatime = controller.deltaTime(time2, time1)
            deltamemory = controller.deltaMemory(memory2, memory1)
            print('Tiempo de ejecución:', str(deltatime), 'ms.')
            print('Memoria utilizada', deltamemory, 'KB.')

        elif int(inputs[0]) == 6:
            idOrigen = input("Identificador de la estación origen: ")
            num_conex = input("Número de conexiones permitidas desde la estación origen: ")
            memory1 = controller.getMemory()
            time1 = controller.getTime()
            printreq5(catalog, idOrigen, num_conex)
            time2 = controller.getTime()
            memory2 = controller.getMemory()
            deltatime = controller.deltaTime(time2, time1)
            deltamemory = controller.deltaMemory(memory2, memory1)
            print('Tiempo de ejecución:', str(deltatime), 'ms.')
            print('Memoria utilizada', deltamemory, 'KB.')

        elif int(inputs[0]) == 7:
            idOrigen = input("Ingrese la Id de origen: ")
            idVecindario = input("Ingrese el nombre del vecindario: ")
            memory1 = controller.getMemory()
            time1 = controller.getTime()
            printreq6(catalog, idOrigen, idVecindario)
            time2 = controller.getTime()
            memory2 = controller.getMemory()
            deltatime = controller.deltaTime(time2, time1)
            deltamemory = controller.deltaMemory(memory2, memory1)
            print('Tiempo de ejecución:', str(deltatime), 'ms.')
            print('Memoria utilizada', deltamemory, 'KB.')

        elif int(inputs[0]) == 8:
            idOrigen = input("Ingrese la Id de origen: ")
            memory1 = controller.getMemory()
            time1 = controller.getTime()
            printreq7(catalog, idOrigen)
            time2 = controller.getTime()
            memory2 = controller.getMemory()
            deltatime = controller.deltaTime(time2, time1)
            deltamemory = controller.deltaMemory(memory2, memory1)
            print('Tiempo de ejecución:', str(deltatime), 'ms.')
            print('Memoria utilizada', deltamemory, 'KB.')

        elif int(inputs[0]) == 8:
            printreq8(catalog)

        else:
            sys.exit(0)
    sys.exit(0)

if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=menu)
    thread.start()