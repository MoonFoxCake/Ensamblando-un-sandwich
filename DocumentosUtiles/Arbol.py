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

class Nodo:
    def __init__(self, tipo, valor=None):
        self.tipo = tipo  # Tipo del componente (por ejemplo, 'PALABRA_CLAVE', 'CONDICIONAL', etc.)
        self.valor = valor  # El valor asociado (por ejemplo, "michelin", "if", etc.)
        self.hijos = []  # Lista de hijos en el árbol (si es que tiene)
    
    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)

    def __str__(self, nivel=0):
        # Esto se usará para imprimir el árbol de manera legible
        resultado = "  " * nivel + f"{self.tipo}: {self.valor}\n"
        for hijo in self.hijos:
            resultado += hijo.__str__(nivel + 1)
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
