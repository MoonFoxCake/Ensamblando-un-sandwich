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
    def imprimir(self):
        if self.raiz is not None:
            print("Árbol de Sintaxis Abstracta:")
            ArbolSintaxisAbstracta.imprimir_preorden(self.raiz)
        else:
            print("El árbol está vacío.")

    def imprimir_preorden(nodo):
        if nodo is not None:
            print("-------------------------")
            if type(nodo.valor) == str:
                print(nodo.tipo)
                print(nodo.valor)
            else:
                print(nodo.tipo)
                for hijo in nodo.valor:
                    ArbolSintaxisAbstracta.imprimir_preorden(hijo)
        else:
            print("El árbol está vacío.")
