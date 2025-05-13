from enum import Enum, auto
import copy

class TipoNodo(Enum):
    PROGRAMA = auto()
    ASIGNACION = auto()
    EXPRESION_MATEMATICA = auto()
    EXPRESION = auto()
    FUNCION = auto()
    INVOCACION = auto()
    PARA_FUNCION = auto()
    PARA_INVOCACION = auto()
    INSTRUCCION = auto()
    REPETICION = auto()
    BIFURCACION = auto()
    IF = auto()
    ELSE = auto()
    ELIF = auto()
    OPERADOR_LOGICO = auto()
    CONDICIONAL = auto()
    COMPARACION = auto()
    RETORNO = auto()
    ERROR = auto()
    PRINCIPAL = auto()
    BLOQUE_INSTRUCCIONES = auto()
    OPERADOR = auto()
    VALOR_VERDAD = auto()
    COMPARADOR = auto()
    TEXTO = auto()
    ENTERO = auto()
    FLOTANTE = auto()
    IDENTIFICADOR = auto()

class NodoArbol:
    def __init__(self, tipo, contenido=None, nodos=None, atributos=None):
        self.tipo = tipo
        self.contenido = contenido
        self.nodos = nodos if nodos is not None else []
        self.atributos = copy.deepcopy(atributos) if atributos is not None else {}

    def visitar(self, visitante):
        return visitante.visitar(self)

    def __str__(self):
        resultado = '{:30}\t'.format(self.tipo)

        if self.contenido is not None:
            resultado += '{:10}\t'.format(self.contenido)
        else:
            resultado += '{:10}\t'.format('')

        if self.atributos:
            resultado += '{:38}'.format(str(self.atributos))
        else:
            resultado += '{:38}\t'.format('')

        if self.nodos:
            resultado += '<'
            for nodo in self.nodos[:-1]:
                if nodo is not None:
                    resultado += '{},'.format(nodo.tipo)
            resultado += '{}'.format(self.nodos[-1].tipo)
            resultado += '>'
        return resultado

class ArbolSintaxisAbstracta:
    def __init__(self, raiz=None):
        self.raiz = raiz

    def imprimir_preorden(self):
        self.__preorden(self.raiz)

    def __preorden(self, nodo):
        if nodo is None:
            return
        print(nodo)
        for hijo in nodo.nodos:
            self.__preorden(hijo)
