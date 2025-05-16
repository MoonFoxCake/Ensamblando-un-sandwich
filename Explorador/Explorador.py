from enum import Enum, auto
import os
#Para poder usar enums

import re
#Re = Regular expressions, deberia de ayudar

# Importar librerias basandose en el explorador de ciruelas

class Componente(Enum):
    #Se usa auto para simplicidad y no tener que asignar valores manualmente, se pueden añadir mas, solo no sabia que poner
    ASIGNACION = auto()
    BLANCOS = auto()
    COMPARADOR = auto()
    CONDICIONAL = auto()
    CRUDO_VALOR_VERDAD = auto()
    ENTERO = auto()
    ERROR = auto()
    FLOTANTE = auto()
    IDENTIFICADOR = auto()
    NINGUNO = auto()
    OPERADOR = auto()
    PALABRA_CLAVE = auto()
    PUNTUACION = auto()
    REPETICION = auto()
    RESEÑA = auto()
    SEPARADORES = auto()
    SIMBOLO = auto()
    TEXTO = auto()



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

        resultado = [f"{self.tipo:10}" , f"{self.texto:10}" ,f"{self.lectura_linea:10}"]
        return resultado
    
    def to_lista(self):
        return [self.tipo, self.texto, self.lectura_linea]

    
class Explorador:
    #Se encarga de encontrar los componentes lexicos, usualmente es el tipo de componente y un string que describe los textos


    componentes_posibles = [(Componente.RESEÑA, r'-E .*? -o'), # Arreglar
                            (Componente.PALABRA_CLAVE, r'^(michelin|servir|ajustar)'),
                            (Componente.CONDICIONAL, r'^(if|else|elif)'),
                            (Componente.REPETICION, r'^(integrar)'),
                            (Componente.ASIGNACION, r'^(incorporar|marinar|pelar)'),
                            (Componente.OPERADOR, r'^(batir|colar|amasar|partir|sobras)'),
                            (Componente.COMPARADOR, r'^(mismo_sabor_que|mas_sazonado_que|menos_cocido_que|tan_horneado_como|tan_dulce_como)'),
                            (Componente.TEXTO, r'^(".?[^"]*)"'), 
                            (Componente.IDENTIFICADOR, r'^([a-zA-Z_]([a-zA-z0-9])*)'),
                            (Componente.FLOTANTE, r'^(-?[0-9]+\.[0-9]+)'),
                            (Componente.ENTERO, r'^(-?[0-9]+)'),
                            (Componente.CRUDO_VALOR_VERDAD, r'^(true|false)'),
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
    
    def verificar_balanceo(self):
        pila = []
        errores = []

        pares = {
            '(': ')',
            '{': '}'
        }

        for comp in self.componentes:
            if comp.tipo == Componente.PUNTUACION:
                simbolo = comp.texto
                linea = comp.lectura_linea

                if simbolo in pares:
                    pila.append((simbolo, linea))
                elif simbolo in pares.values():
                    if not pila:
                        errores.append(f"Error: cierre inesperado '{simbolo}' en la línea {linea}")
                    else:
                        simbolo_abierto, linea_abierta = pila[-1]
                        if pares[simbolo_abierto] == simbolo:
                            pila.pop()
                        else:
                            errores.append(
                                f"Error: se esperaba '{pares[simbolo_abierto]}' para cerrar '{simbolo_abierto}' "
                                f"abierto en la línea {linea_abierta}, pero se encontró '{simbolo}' en la línea {linea}"
                            )
                            pila.pop()  # Sacamos el que no cierra bien, para seguir el flujo correctamente

        # Al final, si hay símbolos abiertos sin cerrar
        for simbolo_abierto, linea_abierta in pila:
            errores.append(f"Error: no se cerró '{simbolo_abierto}' abierto en la línea {linea_abierta}")

        for err in errores:
            print(err)


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
                # Si no hay match, se registra un error como un componente más
                caracter_erroneo = linea[0]
                Componente_error = info_lexico(Componente.ERROR, caracter_erroneo, num_linea)
                componentes.append(Componente_error)
                break
            #variacion del codigo de gitlab, por alguna razon si no esta esto, sigue infinitamente

        return componentes
        #Se retorna el array de componentes lexicos que se encontraron en la linea, si no se encuentra nada se regresa un array vacio
        #Variacion de gitlab, si esta dentro del for, ignora todos los espacios por alguna razon

