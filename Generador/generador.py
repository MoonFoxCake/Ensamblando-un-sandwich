from DocumentosUtiles.Arbol import ArbolSintaxisAbstracta
from Generador.Visitador import VisitadorPython

class Generador:
    def __init__(self, nuevo_asa: ArbolSintaxisAbstracta):
        """
        Inicializa el generador con el árbol de sintaxis abstracta (ASA).
        """
        self.asa = nuevo_asa
        self.visitador = VisitadorPython()

    def imprimir_asa(self):
        """
        Imprime el árbol de sintaxis abstracta en preorden.
        """
        if self.asa.raiz is None:
            print([])
        else:
            self.asa.imprimir_preorden()

    def generar_codigo(self):
        """
        Genera el código Python a partir del ASA usando solo el visitador.
        Retorna el código como string.
        """
        return self.visitador.visitar(self.asa.raiz)