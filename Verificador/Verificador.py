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
    
    
    def __visitar(self, nodo_actual):
        '''Se usa para visitar los nodos del arbol'''
        '''Hay que poner aca todos los tipos de nodos a visitar'''

    def __visitar_asignacion(self,  nodo_actual):
        '''Asignacion es una variable que se le asigna un valor'''

    def __visitar_bifurcacion(self,  nodo_actual):
        '''Bifurcacion es un if o un else'''

    def __visitar_booleano(self,  nodo_actual):
        '''Booleano es un valor booleano, true o false'''

    def __visitar_bloque_instrucciones(self,  nodo_actual):
        '''usted que cree hp'''

    def __visitar_booleano(self,  nodo_actual):
        '''Para Booleanos'''

    

    def __visitar_comparacion(self,  nodo_actual):
        '''Comparacion es una comparacion entre dos valores'''

    def __visitar_comparador(self,  nodo_actual):
        '''No se que poner aca, pero es un comparador'''

    def __visitar_condicion(self,  nodo_actual):
        '''Mae ya deberia de saber es la fucken condicion'''

    def __visitar_entero(self,  nodo_actual):
        '''Entero es un numero entero'''
    
    def __visitar_error(self,  nodo_actual):
        '''Error, no deberia de llegar aca, pero para poder poner el error por si no se agarra con el analizador, o bueno si se pone quemar'''

    def __visitar_funcion(self,  nodo_actual):
        '''Funcion, def_funcion, tengo que ver que puto desmadre hicieron esos maes con el arbol'''


    def __visitar_identificador(self,  nodo_actual):
        '''Identificador es una variable o una funcion??'''

    def __visitar_matematica(self,  nodo_actual):
        '''Matematica es una operacion matematica'''

    def __visitar_operador(self,  nodo_actual):
        '''Operador es un operador matematico, como +, -, *, /'''

    def __visitar_print(self,  nodo_actual):
        '''Mae para printear'''


    def __visitar_programa(self,  nodo_actual):
        '''Programa es el michelin si mal no me acuerdo'''

    

    

class Verificador:

    Arbol: ArbolSintaxisAbstracta
    visitador: Visitante
    tabla_simbolos: TablaSimbolos


    def __init__(self, nuevoArbol: ArbolSintaxisAbstracta):
        self.Arbol = nuevoArbol
        self.tabla_simbolos = TablaSimbolos()
        self.visitador = Visitante(self.tabla_simbolos)


    def print_arbol(self):
        '''Nada mas recuerden que esta no ocupa ser privada, esta se usara en el main'''

        if self.Arbol.raiz is None:
            print("Acaso hay arbol mae")

        else:
            print("Arbol de Sintaxis Abstracta:")
            self.Arbol.imprimir_preorden(self.Arbol.raiz)

    def __AmbienteEstandar(self):
        '''Mae aca estan las funciones estandar CREO que son todas, segun el pdf de documentacion, van en minuscula'''

        funciones_estandar = [ ('pelar', TiposDato.FUNCION), ('marinar', TiposDato.FUNCION), ('quemo', TiposDato.ERROR)]

        for Nombre, tipo in funciones_estandar:
            nodo = Nodo(TiposDato.FUNCION, contendido=Nombre, atributos={'tipo': tipo})
            self.tabla_simbolos.nuevo_registro(nodo)

    def verificar(self):
        self.verificar.visitar(self.Arbol.raiz)