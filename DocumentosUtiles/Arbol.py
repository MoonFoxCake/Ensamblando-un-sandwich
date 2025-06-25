from enum import Enum, auto
import copy

class TipoNodo(Enum):
    ASIGNACION = auto()
    BIFURCACION = auto()
    BLOQUE_INSTRUCCIONES = auto()
    COMPARACION = auto()
    COMPARADOR = auto()
    CONDICION = auto()
    DEF_FUNCION = auto()
    ELIF = auto()
    ELSE = auto()
    ENTERO = auto()
    ERROR = auto()
    EXPRESION_MATEMATICA = auto()
    VARIABLE_MATEMATICA = auto()
    FLOTANTE = auto()
    FUNCION = auto()
    IDENTIFICADOR = auto()
    IF = auto()
    INSTRUCCION = auto()
    INVOCACION = auto()
    OPERADOR = auto()
    OPERADOR_LOGICO = auto()
    PALABRA_CLAVE = auto()
    PARAMETROS = auto()
    PARA_FUNCION = auto()
    PARA_INVOCACION = auto()
    PRINCIPAL = auto()
    PRINT = auto()
    PROGRAMA = auto()
    REPETICION = auto()  
    RETORNO = auto()
    TEXTO = auto()
    AUXILIAR = auto()
    VALOR_VERDAD = auto()



class Nodo:

    contenido : str
    tipo : TipoNodo
    atributos : dict
    def __init__(self, tipo, valor=None, atributos={}, nodos=None):
        self.tipo = tipo  
        
        # mae nos mamamos y lo trabajamos de 2 formas distintas...aca en teoria maneja ambas bien
        if isinstance(valor, list) and nodos is None:
            self.valor = None
            self.hijos = valor  
        else:
            self.valor = valor  
            self.hijos = nodos if nodos is not None else []  
            
        self.atributos = copy.deepcopy(atributos)  

    def visitar(self, visitador):
        return visitador.visitar(self)


    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)

    def __str__(self):
        # Coloca la información del nodo
        resultado = '{:30}\t'.format(self.tipo)
        
        if self.valor is not None:
            resultado += '{:10}\t'.format(self.valor)
        else:
            resultado += '{:10}\t'.format('')

        if self.atributos != {}:
            resultado += '{:38}'.format(str(self.atributos))
        else:
            resultado += '{:38}\t'.format('')

        if self.hijos != []:
            resultado += '<'

            # Imprime los tipos de los nodos del nivel siguiente
            for hijo in self.hijos[:-1]:
                if hijo is not None:
                    resultado += '{},'.format(hijo.tipo)

            resultado += '{}'.format(self.hijos[-1].tipo)
            resultado += '>'

        return resultado


class ArbolSintaxisAbstracta:
    def __init__(self, raiz=None):
        self.raiz = raiz
    def imprimir(self):
        if self.raiz is not None:
            print("Árbol de Sintaxis Abstracta:")
            ArbolSintaxisAbstracta.imprimir_preorden(self.raiz)
        else:
            print("El árbol está vacío.")

    def imprimir_preorden(nodo):
        if nodo is not None:
            print("-------------------------")
            if type(nodo.valor) == str or nodo.valor is None:
                print(nodo.tipo)
                if nodo.valor is not None:
                    print(nodo.valor)
                if nodo.atributos != {}:
                    print(nodo.atributos)
            else:
                print(nodo.tipo)
                print(nodo.atributos)
                # If valor is a list, iterate through it
                if isinstance(nodo.valor, list):
                    for hijo in nodo.valor:
                        if hasattr(hijo, 'tipo'):  # Check if it's a node
                            ArbolSintaxisAbstracta.imprimir_preorden(hijo)
            
            # Also process hijos if they exist, but skip None nodes
            for hijo in nodo.hijos:
                if hijo is not None:  # Only process non-None children
                    ArbolSintaxisAbstracta.imprimir_preorden(hijo)
        # Remove the else clause that prints "El árbol está vacío." for None nodes
