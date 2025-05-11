from Explorador import Componente, info_lexico
from DocumentosUtiles.Arbol import ArbolSintaxisAbstracta, Nodo, TipoNodo

class Analizador:

    componentes_lexicos: list 
    cantidad_componentes: int
    posicion_componente_actual: int
    componente_actual: Componente

    def __init__(self, lista_componentes):

        self.componentes_lexicos = lista_componentes
        self.cantidad_componentes = len(lista_componentes)

        self.posicion_componente_actual = 0
        self.componente_actual = lista_componentes[0]

        self.asa = ArbolSintaxisAbstracta()

    def imprimirarbolAbstracto(self):

        if self.asa.raiz is None:
            print([])
        else:
            self.asa.imprimir_preorden()
    def analizarArbol(self):
        self.asa.raiz = self.__analizar_programa()
    
    def __analizar_programa(self):
        
        Nodos_Nuevos = []

        while (True):

            if self.componente_actual.tipo == Componente.IDENTIFICADOR:
                Nodos_Nuevos = [self.__analizar_asignacion()]

            elif (self.componente_actual.texto == 'michelin'):
                Nodos_Nuevos = [self.__analizar_funcion()]
            
            else:
                break

        
        
        return Nodo(TipoNodo.PROGRAMA, nodos = Nodos_Nuevos)
    
    def __analizar_incorporacion(self):
        pass