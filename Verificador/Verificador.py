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
    
    
    def __visitar(self, nodo: TipoNodo):
        '''Se usa para visitar los nodos del arbol'''
        '''Hay que poner aca todos los tipos de nodos a visitar'''

        if nodo.tipo is TipoNodo.PROGRAMA:
            self.__visitar_programa(nodo)

        elif nodo.tipo is TipoNodo.ASIGNACION:
            self.__visitar_asignacion(nodo)
        
        elif nodo.tipo is TipoNodo.BIFURCACION:
            self.__visitar_bifurcacion(nodo)

        elif nodo.tipo is TipoNodo.BLOQUE_INSTRUCCIONES:
            self.__visitar_bloque_instrucciones(nodo)
        
        elif nodo.tipo is TipoNodo.COMPARACION:
            self.__visitar_comparacion(nodo)
        
        elif nodo.tipo is TipoNodo.COMPARADOR:
            self.__visitar_comparador(nodo)
        
        elif nodo.tipo is TipoNodo.CONDICION:
            self.__visitar_condicion(nodo)

        elif nodo.tipo is TipoNodo.DEF_FUNCION:
            self.__visitar_funcion(nodo)
        
        elif nodo.tipo is TipoNodo.ELIF:
            self.__visitar_bifurcacion(nodo) #En la función
        
        elif nodo.tipo is TipoNodo.ELSE: #No sabemos si hacer uno especifico para else
            self.__visitar_bifurcacion(nodo)
        
        elif nodo.tipo is TipoNodo.ENTERO:
            self.__visitar_entero(nodo)

        elif nodo.tipo is TipoNodo.ERROR:
            self.__visitar_error(nodo)
        
        elif nodo.tipo is TipoNodo.EXPRESION_MATEMATICA:
            self.__visitar_expresion_matematica(nodo)
        
        elif nodo.tipo is TipoNodo.VARIABLE_MATEMATICA:
            self.__visitar_matematica(nodo)
        
        elif nodo.tipo is TipoNodo.FLOTANTE:
            self.__visitar_flotante(nodo)
        
        elif nodo.tipo is TipoNodo.FUNCION:
            self.__visitar_funcion(nodo)
        
        elif nodo.tipo is TipoNodo.IDENTIFICADOR:
            self.__visitar_identificador(nodo)
        
        elif nodo.tipo is TipoNodo.IF:
            self.__visitar_bifurcacion(nodo) #No sabemos si hacer uno especifico para if

        elif nodo.tipo is TipoNodo.INSTRUCCION:
            self.__visitar_instruccion(nodo)
        
        elif nodo.tipo is TipoNodo.INVOCACION:
            self.__visitar_invocacion(nodo)
        
        elif nodo.tipo is TipoNodo.OPERADOR:
            self.__visitar_operador(nodo)
        
        elif nodo.tipo is TipoNodo.PALABRA_CLAVE:
            self.__visitar_palabra_clave(nodo)
        
        elif nodo.tipo is TipoNodo.PARAMETROS:
            self._visitar_parametros (nodo)
        
        elif nodo.tipo is TipoNodo.PARA_FUNCION:
            self._visitar_parametros_funcion(nodo)
        
        elif nodo.tipo is TipoNodo.PARA_INVOCACION:
            self._visitar_parametros_invocacion(nodo)
        
        elif nodo.tipo is TipoNodo.PRINCIPAL:
            self.__visitar_michelin(nodo)
        
        elif nodo.tipo is TipoNodo.PRINT:
            self.__visitar_print(nodo)
        
        elif nodo.tipo is TipoNodo.REPETICION:
            self.__visitar_repeticion(nodo)

        elif nodo.tipo is TipoNodo.RETORNO:
            self.__visitar_retorno(nodo)
        
        elif nodo.tipo is TipoNodo.TEXTO:
            self.__visitar_texto(nodo)
        
        elif nodo.tipo is TipoNodo.AUXILIAR:
            self.__visitar_auxiliar(nodo)

        elif nodo.tipo is TipoNodo.VALOR_VERDAD:
            self.__visitar_valor_verdadero(nodo)

        ## elif nodo.tipo is TipoNodo.LITERAL:      No sabemos si ponerlo, ya que no se usa en el arbol
        ##   self.__visitar_literal(nodo) 
            

        


    def __visitar_asignacion(self,  nodo_actual):
        '''Asignacion es una variable que se le asigna un valor'''
        self.tabla_simbolos.nuevo_registro(nodo_actual.nodos[0])

        for nodo in nodo_actual.nodos:
            nodo.visitar(self)
        
        nodo_actual.atributos['tipo'] =  nodo_actual.nodos[1].atributos['tipo']

        nodo_actual.nodos[0].atributos['tipo']= nodo_actual.nodos[1].atributos['tipo']

        
    def __visitar_auxiliar(self,  nodo_actual):


    def __visitar_bifurcacion(self,  nodo_actual):
        '''Bifurcacion es un if o un else'''

    def __visitar_bloque_instrucciones(self,  nodo_actual):
        '''usted que cree hp'''

    def __visitar_comparacion(self,  nodo_actual):
        '''Comparacion es una comparacion entre dos valores'''
        for nodo in nodo_actual.nodos:
            if nodo.tipo == TipoNodo.IDENTIFICADOR:
                registro = self.tabla_simbolos.verificar_existencia(nodo.contenido)
            nodo.visitar(self)
        
        valor_izquierdo = nodo_actual.nodos[0]
        comparador = nodo_actual.nodos[1]
        valor_derecho = nodo_actual.nodos[2]

        if valor_izquierdo.atributos['tipo'] == valor_derecho.atributos['tipo']:
            comparador.atributos['tipo'] = valor_izquierdo.atributos['tipo']  # Asignamos el tipo de dato del comparador

            nodo_actual.atributos['tipo'] = TiposDato.VALOR_VERDAD  # Asignamos el tipo de dato de la comparacion

        ##PETE CON LO DEL PROFE...
        ## Caso especial loco: Si alguno de los dos es un identificador de
        ## un parámetro de función no puedo saber que tipo tiene o va a
        ## tener por que este lenguaje no es tipado... tons vamos a poner
        ## que la comparación puede ser cualquiera
        ##elif valor_izq.atributos['tipo'] == TipoDatos.CUALQUIERA or \
        ##       valor_der.atributos['tipo'] == TipoDatos.CUALQUIERA:
        ##
        ##    comparador.atributos['tipo'] = TipoDatos.CUALQUIERA
        ##
        ##    # Todavía no estoy seguro.
        ##    nodo_actual.atributos['tipo'] = TipoDatos.CUALQUIERA

        else:
            raise Exception("Los tipos de los valores a comparar no son compatibles", valor_izquierdo.atributos['tipo'], valor_derecho.atributos['tipo'])

    def __visitar_comparador(self,  nodo_actual):
        '''No se que poner aca, pero es un comparador'''

    def __visitar_condicion(self,  nodo_actual):
        '''Mae ya deberia de saber es la fucken condicion'''
        for nodo in nodo_actual.nodos:
            nodo.visitar(self)

        nodo_actual.atributos['tipo'] = TiposDato.BOOLEANO  # Asignamos el tipo de dato de la condicion

    def __visitar_entero(self,  nodo_actual):
         """
        Verifica si el tipo del componente lexico actuales de tipo ENTERO

        Entero ::= -?[0-9]+
        """
    
    def __visitar_error(self,  nodo_actual):
        '''Error, no deberia de llegar aca, pero para poder poner el error por si no se agarra con el analizador, o bueno si se pone quemar'''
        for nodo in nodo_actual.nodos:
            if nodo.tipo == TipoNodo.IDENTIFICADOR:
                registro = self.tabla_simbolos.verificar_existencia(nodo.contenido)
            nodo.visitar(self)

    def __visitar_expresion_matematica(self,  nodo_actual):
        """
        ExpresionMatematica ::= (Expresion) | Numero | Identificador

        Esta mica soportaria textos

        """
        for nodo in nodo_actual.nodos:
            #Esta mica verifica que exista y si es global o local
            if nodo.tipo == TipoNodo.IDENTIFICADOR:
                registro = self.tabla_simbolos.verificar_existencia(nodo.contenido)

            nodo.visitar(self)
        #Anotamos que tipo de dato es 
        nodo_actual.atributos['tipo'] = TiposDato.NUMERO
         


    def ___visitar_expresion(self,  nodo_actual):
        '''2 expresiones matematicas con su operador'''

        #for nodo in nodo_actual.nodos:

    
    def __visitar_funcion(self,  nodo_actual):
        '''Funcion, def_funcion, tengo que ver que puto desmadre hicieron esos maes con el arbol'''
        self.tabla_simbolos.nuevo_registro(nodo_actual, TiposDato.FUNCION, nodo_actual.contenido)
        self.tabla_simbolos.abrir_bloque()  # Abrimos un bloque para la funcion
        for nodo in nodo_actual.nodos:
            nodo.visitar(self)
        
        self.tabla_simbolos.cerrar_bloque()  # Cerramos el bloque de la funcion

        nodo_actual.atrubutos['tipo'] = nodo_actual.nodos[2].atributos['tipo']  # Asignamos el tipo de dato de retorno de la funcion

    def __visitar_flotante(self,  nodo_actual):
        """
        Verifica si el tipo del componente lexico actuales de tipo FLOTANTE

        Flotante ::= -?[0-9]+.[0-9]+
        """

    def __visitar_identificador(self,  nodo_actual):
        '''Identificador es una variable o una funcion??'''

    def __visitar_invocacion(self,  nodo_actual):
        '''Invocacion es una funcion que se invoca, o sea se llama'''

    def __visitar_instruccion(self,  nodo_actual):
        '''nstruccion ::= (Repeticion | Bifurcacion | Asignacion | Invocacion | Retorno | Error | Comentario )'''

    ##def __visitar_literal(self,  nodo_actual):
    ##    '''Literal es un valor literal, o sea un numero, una cadena, un booleano, etc'''

    def __visitar_matematica(self,  nodo_actual):
        '''Matematica es una operacion matematica'''

    def __visitar_michelin(self,  nodo_actual):
        '''Michelin es el programa principal, o sea el def por asi decirlo playo'''
    
    def __visitar_operador(self,  nodo_actual):
        '''Operador es un operador matematico, como +, -, *, /'''


    def _visitar_parametros(self,  nodo_actual):

    def _visitar_parametros_funcion(self,  nodo_actual):
        '''Parametros de una invocacion, o sea los parametros que se le pasan a una funcion al invocarla'''
        for nodo in nodo_actual.nodos:
            self.tabla_simbolos.nuevo_registro(nodo, TiposDato.PARAMETROS, nodo.contenido)
            nodo.visitar(self)


    def _visitar_parametros_invocacion(self,  nodo_actual):
        '''Parametros de una invocacion, o sea los parametros que se le pasan a una funcion al invocarla'''
        for nodo in nodo_actual.nodos:
            if nodo.tipo == TipoNodo.IDENTIFICADOR:
                registro = self.tabla_simbolos.verificar_existencia(nodo.contenido)
            
            elif nodo.tipo == TipoNodo.FUNCION:
                raise Exception("Es una funcion, nada que ver con invocacion", nodo.contenido)
        
            nodo.visitar(self)

    def __visitar_print(self,  nodo_actual):
        '''Mae para printear'''

    def __visitar_palabra_clave(self,  nodo_actual):

    def __visitar_programa(self,  nodo_actual):
        '''Programa es el michelin si mal no me acuerdo'''

    def __visitar_repeticion(self,  nodo_actual):
        '''Repeticion es un bucle, o sea un for o un while'''

    def __visitar_texto(self,  nodo_actual):
        """
        Verifica si el tipo del componente lexico actuales de tipo TEXTO

        Texto ::= ".*"
        """

    def __visitar_valor_verdadero(self,  nodo_actual):
    
        """
        CRUDO_VALOR_VERDAD ::= (True | False)
        """
       

    

class Verificador:

    Arbol: ArbolSintaxisAbstracta
    visitador: Visitante
    tabla_simbolos: TablaSimbolos


    def __init__(self, nuevoArbol: ArbolSintaxisAbstracta):
        self.Arbol = nuevoArbol
        self.tabla_simbolos = TablaSimbolos()
        self.visitador = Visitante(self.tabla_simbolos)
        self.__AmbienteEstandar()


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