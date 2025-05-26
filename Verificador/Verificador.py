from DocumentosUtiles.Arbol import ArbolSintaxisAbstracta, Nodo, TipoNodo
from DocumentosUtiles.TiposDato import TiposDato

class TablaSimbolos:
    '''Almacena informacion paraa el arbol con info del tipo y alcance, ya que se va a trabajar con niveles de profundidad'''

    profundidad : int = 0

    def abrir_bloque(self):
        '''Aumenta la profundidad del bloque o bueno lo simula aumentando la variable'''
        self.profundidad += 1
    
    def cerrar_bloque(self):

        for registro in self.simbolos:
            if registro['profundidad'] == self.profundidad:
                self.simbolos.remove(registro)
        '''Termina un bloque y quita todo lo que este dentro de este, y reduce la profundidad'''
        self.profundidad -= 1
    
    def nuevo_registro(self, nodo, tipo, nombre_registro=''):
        '''Añade un registro nuevo'''

        '''Aca se va a usar nombre, profundiad y referencia'''

        '''Referencia es el nodo del arbol'''

        diccionario = {}

        diccionario['Nombre'] = nodo.contenido
        diccionario['Profundidad'] = self.profundidad
        diccionario['Referencia'] = nodo
        
        self.simbolos.append(diccionario)
        
        
    def verificar_existencia(self, nombre):
        '''Verifica si existe un registro con el nombre dado'''

        for registro in self.simbolos:
            if registro['Nombre'] == nombre and registro['Profundidad'] <= self.profundidad:
                return registro
        
        raise Exception("No existe el carnalito", nombre)

    def __str__(self):

        resultado = "Tabla de Simbolos:\n"
        resultado += "Profundidad: " + str(self.profundidad) + "\n"
        for registro in self.simbolos:
            resultado += str(registro) + "\n"

        return resultado

class Visitante:
    tabla_simbolos: TablaSimbolos

    def __init__(self, nueva_tabla_simbolos):

        self.tabla_simbolos = nueva_tabla_simbolos
    
    
    def visitar(self, nodo: TipoNodo):
        '''Se usa para visitar los nodos del arbol'''
        '''Hay que poner aca todos los tipos de nodos a visitar'''

    def visitar_asignacion(self, nodo: TipoNodo):
        '''Asignacion es una variable que se le asigna un valor'''

    def visitar_bifurcacion(self, nodo: TipoNodo):
        '''Bifurcacion es un if o un else'''

    def visitar_comparacion(self, nodo: TipoNodo):
        '''Comparacion es una comparacion entre dos valores'''

    def visitar_comparador(self, nodo: TipoNodo):
        '''No se que poner aca, pero es un comparador'''

    def visitar_condicion(self, nodo: TipoNodo):
        '''Mae ya deberia de saber es la fucken condicion'''

    def visitar_funcion(self, nodo: TipoNodo):
        '''Funcion, def_funcion, tengo que ver que puto desmadre hicieron esos maes con el arbol'''


    def visitar_identificador(self, nodo: TipoNodo):
        '''Identificador es una variable o una funcion??'''

  


    def visitar_programa(self, nodo: TipoNodo):
        '''Programa es el michelin si mal no me acuerdo'''

    

    

    def visitar_matematica(self, nodo: TipoNodo):
        '''Matematica es una operacion matematica'''

    