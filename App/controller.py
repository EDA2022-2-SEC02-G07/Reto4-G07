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
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def newController():
    """
    Crea una instancia del modelo
    """
    control = {
        'model': model.newCatalog()
    }
    return control
def loadData(control,size):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    catalog = control['model']
    load_stops(catalog,size)
    load_edges(catalog,size)
    model.add_Transbordos(catalog)
    model.components(catalog)
    return model.get_LoadValues(catalog)
# Funciones para la carga de datos
def load_edges(catalog,size):
    file = 'Barcelona/bus_edges_bcn-utf8'+size+'.csv'
    contentfile = cf.data_dir + file
    input_file = csv.DictReader(open(contentfile, encoding='utf-8'))
    for content in input_file:
        model.add_contentEdges(catalog, content)
    return catalog
def load_stops(catalog,size):
    file = 'Barcelona/bus_stops_bcn-utf8'+size+'.csv'
    contentfile = cf.data_dir + file
    input_file = csv.DictReader(open(contentfile, encoding='utf-8'))
    for content in input_file:
        model.add_contentStops(catalog, content)
    return catalog
# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def caminoPosibleEntreDosEstaciones(catalogo, idOrigen, idDestino,search_method): #Funcion principal Req 1
    return model.caminoPosibleEntreDosEstaciones(catalogo["model"], idOrigen, idDestino,search_method)

def menorCaminoEntreDosEstaciones(catalogo, idOrigen, idDestino): #Funcion principal Req 2
    return model.menorCaminoEntreDosEstaciones(catalogo["model"], idOrigen, idDestino)

def reconocerComponentesConectadosenlaRed(catalogo): #Funcion principal Req 3
    return model.reconocerComponentesConectadosenlaRed(catalogo["model"])

def planearCaminoDistanciaMinimaEntrePuntosGeograficos(catalogo, lonOrigen, latOrigen, lonDestino, latDestino): #Funcion principal Req 4
    return model.planearCaminoDistanciaMinimaEntrePuntosGeograficos(catalogo["model"], lonOrigen, latOrigen, lonDestino, latDestino)

def localizarEstacionesAlcanzables(catalogo, idOrigen, nConexionesPermitidas): #Funcion principal Req 5
    return model.localizarEstacionesAlcanzables(catalogo["model"], idOrigen, nConexionesPermitidas)

def menorCaminoEstacionVencindario(catalogo, idOrigen, idVecindario): #Funcion principal Req 6
    return model.menorCaminoEstacionVencindario(catalogo["model"], idOrigen, idVecindario)

def caminoCircular(catalogo, idOrigen): #Funcion principal Req 7
    return model.caminoCircular(catalogo["model"], idOrigen)

def graficarResultados(catalogo): #Funcion principal Req 8
    pass