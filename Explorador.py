from enum import Enum, auto
#Para poder usar enums

import re
#Re = Regular expressions, deberia de ayudar

# Importar librerias basandose en el explorador de ciruelas

class Componente(Enum):
    #Se usa auto para simplicidad y no tener que asignar valores manualmente, se pueden añadir mas, solo no sabia que poner
    RESEÑA = auto()
    PALABRA_CLAVE = auto()
    CONDICIONAL = auto()
    REPETICION = auto()
    ASIGNACION = auto()
    OPERADOR = auto()
    COMPARADOR = auto()
    TEXTO = auto()
    IDENTIFICADOR = auto()
    ENTERO = auto()
    FLOTANTE = auto()
    CRUDO_VALOR_VERDAD = auto()
    PUNTUACION = auto()
    BLANCOS = auto()
    NINGUNO = auto()
    SEPARADORES = auto()
    SIMBOLO = auto()


class info_lexico:
    #Se va a almacenar la informacion de un componente lexico

    tipo: Componente
    texto: str
    linea_lectura: int #Numero de la linea en la que se encuentra el componente

    def __init__(self, nuevo_tipo: Componente, nuevo_texto: str, nueva_linea: int):
        self.tipo = nuevo_tipo
        self.texto = nuevo_texto
        self.lectura_linea = nueva_linea
        #se crea un nuevo objeto que va a contener la informacion lexica
    def __str__(self):
        #formateamos los componentes lexicos para que se vea bonito el error "b o n i t o", porque nunca es bonito ver un error

        resultado = f"{self.tipo:10} | {self.texto:10} | {self.lectura_linea:10}"
        return resultado
    
class Explorador:
    #Se encarga de encontrar los componentes lexicos, usualmente es el tipo de componente y un string que describe los textos


    componentes_posibles = [(Componente.RESEÑA, r'-E .*? -o'), 
                            (Componente.PALABRA_CLAVE, r'^(michelin|servir|quemo)'),
                            (Componente.CONDICIONAL, r'^(if|else|elif)'),
                            (Componente.REPETICION, r'^(integrar)'),
                            (Componente.ASIGNACION, r'^(incorporar|marinar|pelar)'),
                            (Componente.OPERADOR, r'^(batir|colar|amasar|partir|sobras)'),
                            (Componente.COMPARADOR, r'^(mismo sabor que|mas sazonado que|menos cocido que|tan horneado como|tan dulce como)'),
                            (Componente.TEXTO, r'^(".?[^"]*)"'),
                            (Componente.IDENTIFICADOR, r'^([a-zA-Z_]([a-zA-z0-9])*)'),
                            (Componente.ENTERO, r'^(-?[0-9]+)'),
                            (Componente.FLOTANTE, r'^(-?[0-9]+\.[0-9]+)'),
                            (Componente.CRUDO_VALOR_VERDAD, r'^(True|False)'),
                            (Componente.PUNTUACION, r'^([/\{}()])'),
                            (Componente.BLANCOS, r'^(\s)+'),
                            (Componente.SEPARADORES, r'^(;|,|\.)'),
                            (Componente.SIMBOLO, r'^(=|<|>|=|!=)')
                            ]
    #Maes, puse separadores y simbolos para que este mae no se salte cosas, si no tiene como clasificar explota, podria quedar asi o intentar meterlo como error, ahi pueden ver
    def __init__(self, contenido_archivo):
        self.texto = contenido_archivo
        self.componentes = []
        #Inicializacion, nada mas

    def explorar(self):

        #La idea aca es explorar cada linea y sacar los componentes con su info para despues poder analizarlos, aca solo se sacan datos, no se hace ningun analisis
        num_linea = 1
        for linea in self.texto:
            resultado = self.lectura_documento(linea, num_linea)
            self.componentes = self.componentes + resultado
            num_linea += 1
            #Se van guardando los resultados de cada linea en un array y se le suma al contador, para despues poder analizarlos

    def imprimir_componentes(self):
        #Se imprime en un formato algo lindo para que el usuario pueda ver que se hizo con el archivo dado

        for componente in self.componentes:
            print(componente)

    def lectura_documento(self, linea, num_linea):
        #Se encarga de leer el documento y sacar los componentes lexicos, se le pasa una linea y se le saca el componente
        
        componentes = []
        
        while(linea !=  ""):    
            for tipo_componente, regex in self.componentes_posibles:
                    
                    busqueda = re.match(regex, linea)

                    #si se encuentra algo se genera el componente
                    if busqueda is not None :
                            
                            #se evita las lineas vacias y los comentarios
                            if tipo_componente is not Componente.BLANCOS and tipo_componente is not Componente.RESEÑA:
                                
                                Componente_nuevo = info_lexico(tipo_componente,  busqueda.group(), num_linea )
                                #Se crea un componente nuevo
                                
                                componentes.append(Componente_nuevo)

                            linea = linea[busqueda.end():]
                            break;
            else:
                #Si no se encuentra nada se rompe el ciclo
                break
            #variacion del codigo de gitlab, por alguna razon si no esta esto, sigue infinitamente

        return componentes
        #Se retorna el array de componentes lexicos que se encontraron en la linea, si no se encuentra nada se regresa un array vacio
        #Variacion de gitlab, si esta dentro del for, ignora todos los espacios por alguna razon

                            
# Algo basico para leer el archivo
with open("ejemplo.sdw", "r", encoding="utf-8") as archivo:
    lineas = archivo.readlines()

# Crear el explorador y ejecutar el análisis
explorador = Explorador(lineas)
explorador.explorar()
explorador.imprimir_componentes()
