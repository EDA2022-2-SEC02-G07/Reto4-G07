"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """

from haversine import haversine
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import graph as gr
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newCatalog():
    catalog = {'Graph':gr.newGraph(directed=True),
                "NameMap":mp.newMap(),
                "Transbordo":mp.newMap(),
                'RoutesMap':mp.newMap()}
    return catalog
# Funciones para agregar informacion al catalogo

def add_contentStops(catalog, content):
    name = content['Code']+content['Bus_Stop'].replace('BUS - ', '')
    if content['Transbordo']=="S":
        name_T = "T-"+content["Code"]
        if mp.contains(catalog["Transbordo"],name_T) == False:
            mp.put(catalog["Transbordo"],name_T,lt.newList("ARRAY-LIST"))
        lt.addLast(me.getValue(mp.get(catalog["Transbordo"],name_T)),name)
    mp.put(content["NameMap"],name,content)
    gr.insertVertex(catalog['Graph'], name)

def add_contentEdges(catalog, content):
    vertexa = content['Code']+content['Bus_Stop'].replace('BUS-','')
    vertexb = content['Code_Destiny']+content['Bus_Stop'].replace('BUS-','')
    latlog_first = (me.getValue(mp.get(catalog['NameMap'], vertexa))['Latitude'], me.getValue(mp.get(catalog['NameMap'], vertexa))['Longitude'])
    latlog_last = (me.getValue(mp.get(catalog['NameMap'], vertexb))['Latitude'], me.getValue(mp.get(catalog['NameMap'], vertexb))['Longitude'])
    weight = haversine(latlog_first, latlog_last)
    gr.addEdge(catalog['Graph'], vertexa, vertexb, weight)

    Transbordo_keys = mp.keySet(catalog["Transbordo"])
    for i in lt.iterator(Transbordo_keys):
        list_ = me.getValue(mp.get(catalog["Transbordo"],i))
        if lt.size(list_) > 1:
            gr.insertVertex(catalog["Graph"],i)
            for e in lt.iterator(list_):
                gr.addEdge(catalog["Graph"],i,e,0)
                gr.addEdge(catalog["Graph"],e,i,0)
# Funciones para creacion de datos



# Funciones de consulta
def caminoPosibleEntreDosEstaciones(catalogo, idOrigen, idDestino): #Funcion principal Req 1
    pass

def menorCaminoEntreDosEstaciones(catalogo, idOrigen, idDestino): #Funcion principal Req 2
    pass

def reconocerComponentesConectadosenlaRed(catalogo): #Funcion principal Req 3
    pass

def planearCaminoDistanciaMinimaEntrePuntosGeograficos(catalogo, lonOrigen, latOrigen, lonDestino, latDestino): #Funcion principal Req 4
    pass

def localizarEstacionesAlcanzables(catalogo, idOrigen, nConexionesPermitidas): #Funcion principal Req 5
    pass

def menorCaminoEstacionVencindario(catalogo, idOrigen, idVecindario): #Funcion principal Req 6
    pass

def caminoCircular(catalogo, idOrigen): #Funcion principal Req 7
    pass

def graficarResultados(catalogo): #Funcion principal Req 8
    pass

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
