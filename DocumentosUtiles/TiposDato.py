#Mae, aca pondremos los tipos de datos

from enum import Enum, auto

class TiposDato(Enum):

    BOOLEANO = auto()
    CUALQUIERA = auto()
    ENTERO = auto()
    EXPRESION_MATEMATICA = auto()
    EXTRA = auto()
    VARIABLE_MATEMATICA = auto()
    FUNCION = auto()
    ERROR = auto()
    FLOTANTE = auto()
    NINGUNO = auto()  # Added for better type inference (like example2.py)
    NUMERO = auto()
    OPERADOR = auto()
    OPERADOR_LOGICO = auto()
    TEXTO = auto()  
    VALOR_VERDAD = auto()