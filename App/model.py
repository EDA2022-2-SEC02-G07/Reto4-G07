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
from DISClib.ADT import orderedmap as om
from DISClib.Algorithms.Sorting import mergesort as mer
from DISClib.Algorithms.Graphs import bfs as bf
from DISClib.Algorithms.Graphs import dijsktra as dj
from DISClib.ADT import stack as st
from DISClib.Algorithms.Graphs import scc as ko
from DISClib.Algorithms.Graphs import cycles as cy
from DISClib.Algorithms.Graphs import bellmanford as bell
assert cf



"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newCatalog():
    catalog = {'Graph':gr.newGraph(directed=True),
                'GraphNW':gr.newGraph(directed=True),
                "NameMap":mp.newMap(),
                "Transbordo":mp.newMap(),
                "VertexMap":mp.newMap(),
                "ExclusiveMap":mp.newMap(),
                "Graph_List":lt.newList("ARRAY_LIST"),
                "Load_Map":mp.newMap(),
                "Vecindario_Map":mp.newMap(),
                "scc":None,
                "components":om.newMap(),
                "Edge_List":lt.newList("ARRAY_LIST"),
                "Edge_components":om.newMap()}
    mp.put(catalog["Load_Map"],"Exclusivas",0)
    mp.put(catalog["Load_Map"],"Transbordo",0)
    mp.put(catalog["Load_Map"],"Arcos",0)
    mp.put(catalog['Load_Map'],"Rutas",0)
    mp.put(catalog["Load_Map"],"Longitud_Minima",10e100)
    mp.put(catalog["Load_Map"],"Longitud_Maxima",0)
    mp.put(catalog["Load_Map"],"Latitud_Minima",10e100)
    mp.put(catalog["Load_Map"],"Latitud_Maxima",0)
    mp.put(catalog['Load_Map'],"EdgesInFile",0),
    mp.put(catalog['Load_Map'], 'RutasCompartidas',0),
    mp.put(catalog['Load_Map'], 'RutasExclusivas', 0)
    return catalog
# Funciones para agregar informacion al catalogo

def add_contentStops(catalog, content):

    if float(content["Longitude"]) < me.getValue(mp.get(catalog["Load_Map"],"Longitud_Minima")):
        me.setValue(mp.get(catalog["Load_Map"],"Longitud_Minima"),float(content["Longitude"]))
    elif float(content["Longitude"]) > me.getValue(mp.get(catalog["Load_Map"],"Longitud_Maxima")):
        me.setValue(mp.get(catalog["Load_Map"],"Longitud_Maxima"),float(content["Longitude"]))
    if float(content["Latitude"]) < me.getValue(mp.get(catalog["Load_Map"],"Latitud_Minima")):
        me.setValue(mp.get(catalog["Load_Map"],"Latitud_Minima"),float(content["Latitude"]))
    elif float(content["Latitude"]) > me.getValue(mp.get(catalog["Load_Map"],"Latitud_Maxima")):
        me.setValue(mp.get(catalog["Load_Map"],"Latitud_Maxima"),float(content["Latitude"]))
    name = content['Code']+"-"+content['Bus_Stop'].replace('BUS-', '')
    content["Code-Ruta"] = name
    lt.addLast(catalog["Graph_List"],content)
    if content['Transbordo']=="S":
        name_T = "T-"+content["Code"]
        if mp.contains(catalog["Transbordo"],name_T) == False:
            me.setValue(mp.get(catalog["Load_Map"],"Transbordo"),me.getValue(mp.get(catalog["Load_Map"],"Transbordo"))+1)
            mp.put(catalog["Transbordo"],name_T,mp.newMap())
        mp.put(me.getValue(mp.get(catalog['Transbordo'], name_T)), name, content)  
    else:
        if mp.contains(catalog['ExclusiveMap'], content['Code'])==False:
            me.setValue(mp.get(catalog["Load_Map"],"Exclusivas"),me.getValue(mp.get(catalog["Load_Map"],"Exclusivas"))+1)
            mp.put(catalog['ExclusiveMap'],content['Code'],lt.newList('ARRAY_LIST'))
        lt.addLast(me.getValue(mp.get(catalog['ExclusiveMap'], content['Code'])), name)
    mp.put(catalog["NameMap"],name,content)
    if mp.contains(catalog["VertexMap"],name) == False:
        mp.put(catalog["VertexMap"],name,True)
    gr.insertVertex(catalog['Graph'], name)
    gr.insertVertex(catalog['GraphNW'], name)
    if mp.contains(catalog["Vecindario_Map"],content["Neighborhood_Name"]) == False:
        mp.put(catalog["Vecindario_Map"],content["Neighborhood_Name"],lt.newList("ARRAY_LIST"))
    lt.addLast(me.getValue(mp.get(catalog["Vecindario_Map"],content["Neighborhood_Name"])),name)
def add_contentEdges(catalog, content):
    me.setValue(mp.get(catalog['Load_Map'], 'EdgesInFile'), me.getValue(mp.get(catalog['Load_Map'], 'EdgesInFile'))+1)
    vertexa = content['Code']+"-"+content['Bus_Stop'].replace('BUS-','')
    vertexb = content['Code_Destiny']+"-"+content['Bus_Stop'].replace("BUS-",'')
    if mp.contains(catalog["VertexMap"],vertexa) == True and mp.contains(catalog["VertexMap"],vertexb) == True :
        latlog_first = (float(me.getValue(mp.get(catalog['NameMap'], vertexa))['Latitude']),float( me.getValue(mp.get(catalog['NameMap'], vertexa))['Longitude']))
        latlog_last = (float(me.getValue(mp.get(catalog['NameMap'], vertexb))['Latitude']),float( me.getValue(mp.get(catalog['NameMap'], vertexb))['Longitude']))
        weight = haversine(latlog_first, latlog_last)
        gr.addEdge(catalog['Graph'], vertexa, vertexb, weight)
        gr.addEdge(catalog['GraphNW'], vertexa, vertexb, 1)
        lt.addLast(catalog["Edge_List"],{"vertexA":vertexa,"vertexB":vertexb,"weight":weight})
        me.setValue(mp.get(catalog["Load_Map"],"Arcos"),me.getValue(mp.get(catalog["Load_Map"],"Arcos"))+1)
        me.setValue(mp.get(catalog["Load_Map"],"RutasExclusivas"),me.getValue(mp.get(catalog["Load_Map"],"RutasExclusivas"))+1)
def add_Transbordos(catalog):
    Transbordo_keys = mp.keySet(catalog["Transbordo"])
    for i in lt.iterator(Transbordo_keys):
        list_ = mp.keySet(me.getValue(mp.get(catalog['Transbordo'], i)))
        values_ = mp.valueSet(me.getValue(mp.get(catalog['Transbordo'], i)))
        lt.addLast(catalog["Graph_List"],{"Code-Ruta":i,"Longitude":lt.getElement(values_, 1)['Longitude'],"Latitude":lt.getElement(values_, 1)['Latitude'],"Adjacents":""})
        gr.insertVertex(catalog["Graph"],i)
        gr.insertVertex(catalog["GraphNW"],i)
        for e in lt.iterator(list_):
            gr.addEdge(catalog["Graph"],i,e,0)
            gr.addEdge(catalog["Graph"],e,i,0)
            lt.addLast(catalog["Edge_List"],{"vertexA":i,"vertexB":e,"weight":0})
            lt.addLast(catalog["Edge_List"],{"vertexA":e,"vertexB":i,"weight":0})
            gr.addEdge(catalog["GraphNW"],i,e,1)
            gr.addEdge(catalog["GraphNW"],e,i,1)
            me.setValue(mp.get(catalog["Load_Map"],"Arcos"),me.getValue(mp.get(catalog["Load_Map"],"Arcos"))+2)
            me.setValue(mp.get(catalog["Load_Map"],"RutasCompartidas"),me.getValue(mp.get(catalog["Load_Map"],"RutasCompartidas"))+2)
def components(catalog):
    catalog["scc"] = ko.KosarajuSCC(catalog["Graph"])
    for i in lt.iterator(om.keySet(catalog["scc"]["idscc"])):
        if om.contains(catalog["components"],me.getValue(mp.get(catalog["scc"]["idscc"],i))) == False:
            om.put(catalog["components"],me.getValue(mp.get(catalog["scc"]["idscc"],i)),lt.newList("ARRAY_LIST"))
        lt.addLast(me.getValue(om.get(catalog["components"],me.getValue(mp.get(catalog["scc"]["idscc"],i)))),i)
    for i in lt.iterator(catalog["Edge_List"]):
        vertex = i["vertexA"]
        key = me.getValue(mp.get(catalog["scc"]["idscc"],vertex))
        if om.contains(catalog["Edge_components"],key) == False:
            om.put(catalog["Edge_components"],key,lt.newList("ARRAY_LIST"))
        lt.addLast(me.getValue(om.get(catalog["Edge_components"],key)),i)
def get_LoadValues(catalog):
    Total_Stops_File = mp.size(catalog['NameMap'])
    Total_Edges_File = me.getValue(mp.get(catalog['Load_Map'],'EdgesInFile'))
    Total_Exclusivas = me.getValue(mp.get(catalog["Load_Map"],"Exclusivas"))
    Total_Transbordo = me.getValue(mp.get(catalog["Load_Map"],"Transbordo"))
    Total_Estaciones = Total_Exclusivas + Total_Transbordo
    Total_Rutas_Compartidas = me.getValue(mp.get(catalog['Load_Map'],'RutasCompartidas'))
    Total_Rutas_Exclusivas = me.getValue(mp.get(catalog['Load_Map'],'RutasExclusivas'))
    Total_Rutas = Total_Rutas_Compartidas + Total_Rutas_Exclusivas
    Total_Arcos = me.getValue(mp.get(catalog["Load_Map"],"Arcos"))
    Total_Vertices = gr.numVertices(catalog['Graph'])
    Longitud_Minima = me.getValue(mp.get(catalog["Load_Map"],"Longitud_Minima"))
    Longitud_Maxima = me.getValue(mp.get(catalog["Load_Map"],"Longitud_Maxima"))
    Latitud_Maxima = me.getValue(mp.get(catalog["Load_Map"],"Latitud_Maxima"))
    Latitud_Minima = me.getValue(mp.get(catalog["Load_Map"],"Latitud_Minima"))
    First_5 = lt.subList(catalog["Graph_List"],1,5)
    Last_5 = lt.subList(catalog["Graph_List"],lt.size(catalog["Graph_List"])-4,5)
    for i in lt.iterator(First_5):
        i["Adjacents"] = lt.size(gr.adjacents(catalog["Graph"],i["Code-Ruta"]))
    for i in lt.iterator(Last_5):
        i["Adjacents"] = lt.size(gr.adjacents(catalog["Graph"],i["Code-Ruta"]))
    return Total_Stops_File, Total_Edges_File, Total_Estaciones, Total_Rutas_Compartidas, Total_Rutas_Exclusivas, Total_Rutas, Total_Exclusivas,Total_Transbordo,Total_Arcos,Total_Vertices,Longitud_Maxima,Longitud_Minima,Latitud_Maxima,Latitud_Minima,First_5,Last_5
# Funciones para creacion de datos



# Funciones de consulta
def caminoPosibleEntreDosEstaciones(catalog, idOrigen, idDestino,search_method): #Funcion principal Req 1
    weight = 0
    list_ = lt.newList("ARRAY_LIST")
    if search_method == "bfs":
        search = bf.BreadhtFisrtSearch(catalog["Graph"],idOrigen)
        path = bf.pathTo(search,idDestino)
    path = reverselist(path)
    i = 1
    while i < lt.size(path):
        if i != lt.size(path):
            distance = gr.getEdge(catalog["Graph"],lt.getElement(path,i),lt.getElement(path,i+1))["weight"]
            weight += distance
            lt.addLast(list_,round(distance,2))
        i+=1
    return path,weight,list_

def menorCaminoEntreDosEstaciones(catalogo, idOrigen, idDestino): #Funcion principal Req 2
    search = dj.Dijkstra(catalogo['GraphNW'], idOrigen)
    path = reverselist(dj.pathTo(search, idDestino))
    path_list = lt.newList('ARRAY_LIST')
    for i in lt.iterator(path):
        lt.addLast(path_list, i['vertexA'])
    weight = 0
    list_ = lt.newList("ARRAY_LIST")
    i = 1
    while i < lt.size(path):
        if i != lt.size(path):
            distance = gr.getEdge(catalogo["Graph"],lt.getElement(path_list,i),lt.getElement(path_list,i+1))["weight"]
            weight += distance
            lt.addLast(list_,round(distance,2))
        i+=1
    return path_list, weight, list_

def reconocerComponentesConectadosenlaRed(catalogo): #Funcion principal Req 3
    componentes_conectados = ko.connectedComponents(catalogo["scc"])
    maxkey = om.maxKey(catalogo["components"])
    minkey = om.minKey(catalogo["components"])
    list_ = om.values(catalogo["components"],minkey,maxkey)
    mer.sort(list_,cmpReq3)
    sublist = lt.subList(list_,1,5)
    return sublist,componentes_conectados
def planearCaminoDistanciaMinimaEntrePuntosGeograficos(catalogo, lonOrigen, latOrigen, lonDestino, latDestino): #Funcion principal Req 4
    origen = None
    destino = None
    def_o = None
    def_d = None
    vertices = gr.vertices(catalogo['Graph'])
    for v in lt.iterator(vertices):
        dist_estacion_o = haversine((lonOrigen, latOrigen),(v['Longitude'],v['Latitude']))
        dist_estacion_d = haversine((lonDestino, latDestino),(v['Longitude'],v['Latitude']))
        if def_o == None or dist_estacion_o < def_o:
            def_o = dist_estacion_o
            origen = v
        if def_d == None or dist_estacion_d < def_d:
            def_d = dist_estacion_d
            destino = v
    graph = bell.BellmanFord(catalogo['GraphNW'],origen)
    distancia = bell.distTo(graph,destino)

    return origen,def_o,destino,def_d,distancia

def localizarEstacionesAlcanzables(catalogo, idOrigen, nConexionesPermitidas): #Funcion principal Req 5
    vertexes = gr.vertices(catalogo['Graph'])
    search = dj.Dijkstra(catalogo['Graph'], idOrigen)
    alcanzables = lt.newList('ARRAY_LIST')
    for i in lt.iterator(vertexes):
        while lt.size(alcanzables) < int(nConexionesPermitidas):
            if i != idOrigen:
                temp_path = reverselist(dj.pathTo(search, i))
                path_list = lt.newList('ARRAY_LIST')
                for i in lt.iterator(temp_path):
                    lt.addLast(path_list, i['vertexA'])
                for j in lt.iterator(path_list):
                        if lt.isPresent(alcanzables, j) == 0:
                            lt.addLast(alcanzables, j)
    return alcanzables

def menorCaminoEstacionVencindario(catalogo, idOrigen, Vecindario): #Funcion principal Req 6
    vecindario_rutes = me.getValue(mp.get(catalogo["Vecindario_Map"],Vecindario))
    search = dj.Dijkstra(catalogo["Graph"],idOrigen)
    first = True
    max_name = None
    for i in lt.iterator(vecindario_rutes):
        ispath = dj.hasPathTo(search,i) 
        if ispath == True:
            if first == True:
                max_distance = dj.distTo(search,i)
                max_name = i
                first = False
            elif max_distance > dj.distTo(search,i):
                max_distance = dj.distTo(search,i)
                max_name = i
    if max_name == None:
        return lt.newList(),lt.newList(),0
    else:
        path = dj.pathTo(search,max_name)
        path = reverselist(path)
        path_ = lt.newList("ARRAY_LIST")
        distances_list = lt.newList()
        i = 1
        weight = 0
        for i in lt.iterator(path):
            lt.addLast(path_,i["vertexA"])
            distance = i["weight"]
            lt.addLast(distances_list,round(distance,2))
            weight += distance
        lt.addLast(path_,i["vertexB"])
        return path_,distances_list,weight
def caminoCircular(catalogo, idOrigen): #Funcion principal Req 7
    key = me.getValue(mp.get(catalogo["scc"]["idscc"],idOrigen))
    components = me.getValue(om.get(catalogo["components"],key))
    edges = me.getValue(om.get(catalogo["Edge_components"],key))
    adjacents = gr.adjacents(catalogo["Graph"],idOrigen)
    salida = lt.newList("ARRAY_LIST") #IdOrigen llega directamente a ellos
    entrada = lt.newList("ARRAY_LIST") #Llega directamente a IdOrigen
    for adjacent in lt.iterator(adjacents):
        if gr.getEdge(catalogo["Graph"],idOrigen,adjacent) != None:
            lt.addLast(salida,adjacent)
        if gr.getEdge(catalogo["Graph"],adjacent,idOrigen) != None:
            lt.addLast(entrada,adjacent)
    continuar = True
    new_component = newComponent(components,edges,idOrigen)
    cycle_path = None
    for salida_edge in lt.iterator(salida):
        if continuar:
            salida_search = bf.BreadhtFisrtSearch(new_component,salida_edge)
            for entrada_edge in lt.iterator(entrada):
                if salida_edge != entrada_edge and continuar == True:
                    if bf.hasPathTo(salida_search,entrada_edge) == True:
                        continuar = False
                        cycle_path = reverselist(bf.pathTo(salida_search,entrada_edge))
    if cycle_path != None:
        lt.addFirst(cycle_path,idOrigen)
        lt.addLast(cycle_path,idOrigen)
        weight = 0
        list_ = lt.newList("ARRAY_LIST")
        i = 1
        while i < lt.size(cycle_path):
            if i != lt.size(cycle_path):
                distance = gr.getEdge(catalogo["Graph"],lt.getElement(cycle_path,i),lt.getElement(cycle_path,i+1))["weight"]
                weight += distance
                lt.addLast(list_,round(distance,2))
            i+=1
        return cycle_path,weight,list_
    else:
        return None,None,None
def newComponent(components,edges,idOrigen): #Función Auxiliar Requerimiento 7
    graph = gr.newGraph()
    for component in lt.iterator(components):
        if component != idOrigen:
            gr.insertVertex(graph,component)
    for edge in lt.iterator(edges):
        if (edge["vertexA"] != idOrigen) and (edge["vertexB"] != idOrigen):
            gr.addEdge(graph,edge["vertexA"],edge["vertexB"],edge["weight"])
    return graph
def graficarResultados(catalogo): #Funcion principal Req 8
    pass

# Funciones utilizadas para comparar elementos dentro de una lista
def reverselist(list): #Función para invertir el orden de una lista
    li = 1
    lo = lt.size(list)
    while li <lo:
        lt.exchange(list,li,lo)
        li +=1
        lo -= 1
    return list
# Funciones de ordenamiento
def cmpReq3(lis1,list2):
    if lt.size(lis1) > lt.size(list2):
        return True
    else:
        return False