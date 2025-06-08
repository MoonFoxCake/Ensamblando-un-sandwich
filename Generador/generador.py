from DocumentosUtiles.Arbol import ArbolSintaxisAbstracta, Nodo, TipoNodo
from Generador.Visitador import VisitadorPython


class Generador:

    asa : ArbolSintaxisAbstracta
    visitador: VisitadorPython

    ambiente_estandar = """hay que poner nuestras funciones como pelar o quemar"""




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


