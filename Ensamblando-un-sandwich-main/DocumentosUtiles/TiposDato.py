#Mae, aca pondremos los tipos de datos

from enum import Enum, auto

class TiposDato(Enum):

    BOOLEANO = auto()
    ENTERO = auto()
    EXPRESION_MATEMATICA = auto()
    VARIABLE_MATEMATICA = auto()
    FLOTANTE = auto()
    NUMERO = auto()
    OPERADOR = auto()
    OPERADOR_LOGICO = auto()
    TEXTO = auto()  