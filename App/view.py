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

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
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

catalog = None
size = "-large"

def printreq1(catalog, idOrigen, idDestino):
    pass

def printreq2(catalog, idOrigen, idDestino):
    pass

def printreq3(catalog):
    pass

def printreq4(catalog, lonOrigen, latOrigen, lonDestino, latDestino):
    pass

def printreq5(catalog, idOrigen, nConexionesPermitidas):
    pass

def printreq6(catalog, idOrigen, idVecindario):
    pass

def printreq7(catalog, idOrigen):
    pass

def printreq8(catalog):
    pass

"""
Menu principal
"""

def load(catalog):
    pass

while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
         if catalog == None:
            catalog = controller.newController()
            controller.loadData(catalog,size)
            print("Cargando información de los archivos ....")
            load(catalog)

    elif int(inputs[0]) == 2:
        idOrigen = input(": ")
        idDestino = input(": ")
        printreq1(catalog, idOrigen, idDestino)

    elif int(inputs[0]) == 3:
        printreq2(catalog)

    elif int(inputs[0]) == 4:
        lonOrigen = input(": ")
        latOrigen = input(": ")
        lonDestino = input(": ")
        latDestino = input(": ")
        printreq3(catalog, lonOrigen, latOrigen, lonDestino, latDestino)

    elif int(inputs[0]) == 5:
        idOrigen = input(": ")
        N = input(": ")
        printreq4(catalog, idOrigen, idDestino)

    elif int(inputs[0]) == 6:
        idOrigen = input(": ")
        idDestino = input(": ")
        printreq5(catalog, idOrigen, idDestino)

    elif int(inputs[0]) == 7:
        idOrigen = input(": ")
        idVecindario = input(": ")
        printreq6(catalog, idOrigen, idDestino)

    elif int(inputs[0]) == 8:
        idOrigen = input(": ")
        printreq7(catalog, idOrigen, idDestino)

    elif int(inputs[0]) == 8:
        printreq8(catalog)

    else:
        sys.exit(0)
sys.exit(0)
