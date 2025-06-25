from DocumentosUtiles.Arbol import ArbolSintaxisAbstracta, Nodo, TipoNodo
from Generador.Visitador import VisitadorPython


class Generador:

    asa : ArbolSintaxisAbstracta
    visitador: VisitadorPython

    ambiente_estandar = """import sys

# Imprime un valor
def servir(valor):
    print(valor)

# Realiza una operación matemática entre dos valores
def ajustar(var, op, val):
    if op == "batir":
        return var + val
    if op == "colar":
        return var - val
    if op == "amasar":
        return var * val
    if op == "partir":
        return var / val
    if op == "sobras":
        return var % val
    return 0

# Muestra un mensaje de error y termina la ejecución
def dingding():
    print("Error: se ha quemado algo en la cocina.")
    sys.exit(1)

# Simula una transformación de valor
def marinar(nombre, nuevo_valor):
    return nuevo_valor

# Resta una cantidad a un valor dado
def pelar(nombre, cantidad):
    return nombre - cantidad

# Ejecuta un bloque mientras se cumpla una condición
def integrar(condicion, bloque):
    while condicion():
        bloque()

# Asigna un valor a una variable en el ambiente
def incorporar(ambiente, nombre, valor):
    ambiente[nombre] = valor
"""

    def __init__(self, nuevo_asa: ArbolSintaxisAbstracta):
        
        self.asa = nuevo_asa
        self.visitador = VisitadorPython()

    def imprimir_asa(self):

        if self.asa.raiz is None:

            print([])

        else:
            self.asa.imprimir_preorden()

    def generar_codigo(self):

        resultado = self.visitador.visitar(self.asa.raiz)
        print(self.ambiente_estandar)
        print(resultado)


