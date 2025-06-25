from DocumentosUtiles.Arbol import ArbolSintaxisAbstracta, Nodo, TipoNodo
from DocumentosUtiles.TiposDato import TiposDato

class TablaSimbolos:
    '''Almacena informacion paraa el arbol con info del tipo y alcance, ya que se va a trabajar con niveles de profundidad'''
    def __init__(self):
        self.simbolos = []       #Lista única por instancia
        self.profundidad = 0

    def abrir_bloque(self):
        '''Aumenta la profundidad del bloque o bueno lo simula aumentando la variable'''
        self.profundidad += 1
    
    def cerrar_bloque(self):
        # Create a list copy to avoid modification during iteration
        simbolos_a_remover = []
        for registro in self.simbolos:
            if registro['Profundidad'] == self.profundidad:
                simbolos_a_remover.append(registro)
        
        # Remove the symbols
        for registro in simbolos_a_remover:
            self.simbolos.remove(registro)
            
        '''Termina un bloque y quita todo lo que este dentro de este, y reduce la profundidad'''
        self.profundidad -= 1
    
    def nuevo_registro(self, nodo, tipo, nombre_registro=''):
        '''Añade un registro nuevo'''

        '''Aca se va a usar nombre, profundiad y referencia'''

        '''Referencia es el nodo del arbol'''

        diccionario = {}

        diccionario['Nombre'] = nodo.valor #Por que valor sale así?
        diccionario['Profundidad'] = self.profundidad
        diccionario['Referencia'] = nodo
        diccionario['Tipo'] = tipo #No se usaban aunque es un argumento entonces lo agregué
        diccionario['NombreRegistro'] = nombre_registro #No se usaban aunque es un argumento entonces lo agregué
        
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
    
    def visitar(self, nodo):
        '''Public method that calls the private __visitar method'''
        return self.__visitar(nodo)
    
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
        # registramos al chiquito en la tabla
        if nodo_actual.hijos and nodo_actual.hijos[0] is not None:
            self.tabla_simbolos.nuevo_registro(nodo_actual.hijos[0], TiposDato.CUALQUIERA)
        
        # A visitar a los mocosos
        for nodo in nodo_actual.hijos:
            if nodo is not None:
                nodo.visitar(self)
        
        # Assign the type of the right-hand side to both the assignment and identifier
        if len(nodo_actual.hijos) >= 2 and nodo_actual.hijos[1] is not None:
            valor_asignado = nodo_actual.hijos[1]
            tipo_valor = valor_asignado.atributos.get('tipo', TiposDato.CUALQUIERA)
            
            # tipo para asignar
            nodo_actual.atributos['tipo'] = tipo_valor
            
            # algo algo identificador
            if nodo_actual.hijos[0] is not None:
                nodo_actual.hijos[0].atributos['tipo'] = tipo_valor
        else:
            nodo_actual.atributos['tipo'] = TiposDato.CUALQUIERA

        
    def __visitar_auxiliar(self,  nodo_actual):
        '''Nodo auxiliar que puede tener cualquier propósito'''
        for nodo in nodo_actual.hijos:
            nodo.visitar(self)
        

        if nodo_actual.hijos and 'tipo' in nodo_actual.hijos[0].atributos:
            nodo_actual.atributos['tipo'] = nodo_actual.hijos[0].atributos['tipo']
        else:
            nodo_actual.atributos['tipo'] = TiposDato.CUALQUIERA

    def __visitar_bifurcacion(self,  nodo_actual): #Cambié en if y elif a nodo_actual.tipo ya que es el párametro en este contexto
        '''Bifurcacion es un if o un else'''
        """
        Bifurcacion ::= if (elif)* (else)?
        """
        
        if nodo_actual.tipo == TipoNodo.BIFURCACION:
            for nodo in nodo_actual.hijos:
                nodo.visitar(self)
            nodo_actual.atributos['tipo'] = TiposDato.CUALQUIERA
        elif nodo_actual.tipo ==  TipoNodo.IF:
            self.tabla_simbolos.abrir_bloque()

            for nodo in nodo_actual.hijos:
                nodo.visitar(self)
            
            # Set type based on the block of instructions if present
            if len(nodo_actual.hijos) > 1 and 'tipo' in nodo_actual.hijos[1].atributos:
                nodo_actual.atributos['tipo'] = nodo_actual.hijos[1].atributos['tipo']
            else:
                nodo_actual.atributos['tipo'] = TiposDato.CUALQUIERA
                
            self.tabla_simbolos.cerrar_bloque()  # Cerramos el bloque del if
        elif nodo_actual.tipo == TipoNodo.ELIF:
            self.tabla_simbolos.abrir_bloque()

            for nodo in nodo_actual.hijos:
                nodo.visitar(self)
                
            # Set type based on the block of instructions if present
            if len(nodo_actual.hijos) > 1 and 'tipo' in nodo_actual.hijos[1].atributos:
                nodo_actual.atributos['tipo'] = nodo_actual.hijos[1].atributos['tipo']
            else:
                nodo_actual.atributos['tipo'] = TiposDato.CUALQUIERA
                
            self.tabla_simbolos.cerrar_bloque()  # Cerramos el bloque del elif
        elif nodo_actual.tipo == TipoNodo.ELSE:
            self.tabla_simbolos.abrir_bloque()

            for nodo in nodo_actual.hijos:
                nodo.visitar(self)
                
            # Set type based on the block of instructions if present  
            if nodo_actual.hijos and 'tipo' in nodo_actual.hijos[0].atributos:
                nodo_actual.atributos['tipo'] = nodo_actual.hijos[0].atributos['tipo']
            else:
                nodo_actual.atributos['tipo'] = TiposDato.CUALQUIERA
                
            self.tabla_simbolos.cerrar_bloque()  # Cerramos el bloque del else
        


    def __visitar_bloque_instrucciones(self,  nodo_actual):
        """
        Visita un bloque de instrucciones.
        Estructura:

            BloqueInstrucciones ::= { Instruccion+ }

        """
        for nodo in nodo_actual.hijos:
            if nodo is not None:
                nodo.visitar(self)

        # mae, aca se pone el tipo del bloque, deberia de ser  ninguno si no hay instrucciones
        nodo_actual.atributos['tipo'] = TiposDato.NINGUNO
        
        for nodo in nodo_actual.hijos:
            if nodo is not None and 'tipo' in nodo.atributos:
                if nodo.atributos['tipo'] != TiposDato.NINGUNO:
                    nodo_actual.atributos['tipo'] = nodo.atributos['tipo']
                    break

    def __visitar_comparacion(self,  nodo_actual):
        '''Comparacion es una comparacion entre dos valores'''
        for nodo in nodo_actual.hijos:
            if nodo.tipo == TipoNodo.IDENTIFICADOR:
                try:
                    registro = self.tabla_simbolos.verificar_existencia(nodo.valor)
                except:
                    # If identifier doesn't exist, continue processing
                    pass
            nodo.visitar(self)
        
        # es un desmadre de comparacion, pero es una comparacion entre 3 valores
        if len(nodo_actual.hijos) >= 3:
            valor_izquierdo = nodo_actual.hijos[0]
            comparador = nodo_actual.hijos[1]
            valor_derecho = nodo_actual.hijos[2]

            # mae....nos aseguramos que todo bien
            if 'tipo' in valor_izquierdo.atributos and 'tipo' in valor_derecho.atributos:
                if valor_izquierdo.atributos['tipo'] == valor_derecho.atributos['tipo']:
                    comparador.atributos['tipo'] = valor_izquierdo.atributos['tipo']
                    nodo_actual.atributos['tipo'] = TiposDato.VALOR_VERDAD
                elif valor_izquierdo.atributos['tipo'] == TiposDato.CUALQUIERA or \
                     valor_derecho.atributos['tipo'] == TiposDato.CUALQUIERA:
                    # esto basicamente es que aunque no sean el mismo tipo, se puede comparar
                    comparador.atributos['tipo'] = TiposDato.CUALQUIERA
                    nodo_actual.atributos['tipo'] = TiposDato.CUALQUIERA
                else:

                    comparador.atributos['tipo'] = TiposDato.CUALQUIERA
                    nodo_actual.atributos['tipo'] = TiposDato.VALOR_VERDAD
            else:
                comparador.atributos['tipo'] = TiposDato.CUALQUIERA
                nodo_actual.atributos['tipo'] = TiposDato.VALOR_VERDAD
        else:
            # debe de ser booleano, manda huevo
            nodo_actual.atributos['tipo'] = TiposDato.VALOR_VERDAD

    def __visitar_comparador(self,  nodo_actual):
        """
        Comparador ::= mismo_sabor_que|mas_sazonado_que|menos_cocido_que|tan_horneado_como|tan_dulce_como
        """
        '''No se que poner aca, pero es un comparador'''

        # un poco basado en lo del profe un POQUITO
        if nodo_actual.valor in ['mas_sazonado_que', 'menos_cocido_que', 'tan_horneado_como']:
            nodo_actual.atributos['tipo'] = TiposDato.NUMERO 
        elif nodo_actual.valor in ['mismo_sabor_que', 'tan_dulce_como']:
            nodo_actual.atributos['tipo'] = TiposDato.CUALQUIERA  # compara papas y tomates
        else:
            nodo_actual.atributos['tipo'] = TiposDato.CUALQUIERA

    def __visitar_condicion(self,  nodo_actual):
        '''Mae ya deberia de saber es la fucken condicion'''
        for nodo in nodo_actual.hijos:
            nodo.visitar(self)

        # Conditions should result in boolean/truth values
        nodo_actual.atributos['tipo'] = TiposDato.VALOR_VERDAD

    def __visitar_entero(self,  nodo_actual):
        """
        Verifica si el tipo del componente lexico actuales de tipo ENTERO

        Entero ::= -?[0-9]+
        """
        nodo_actual.atributos['tipo'] = TiposDato.NUMERO  # mae, integers, enteros, ahora todo es numero, ok?
    
    def __visitar_error(self,  nodo_actual):
        '''Error, no deberia de llegar aca, pero para poder poner el error por si no se agarra con el analizador, o bueno si se pone quemar'''
        for nodo in nodo_actual.hijos:
            if nodo.tipo == TipoNodo.IDENTIFICADOR:
                registro = self.tabla_simbolos.verificar_existencia(nodo.valor)
            nodo.visitar(self)

    def __visitar_expresion_matematica(self,  nodo_actual):
        """
        ExpresionMatematica ::= (Expresion) | Numero | Identificador

        Esta mica soportaria textos

        """
        for nodo in nodo_actual.hijos:
            #Esta mica verifica que exista y si es global o local
            if nodo.tipo == TipoNodo.IDENTIFICADOR:
                try:
                    registro = self.tabla_simbolos.verificar_existencia(nodo.valor)
                except:
                    # If identifier doesn't exist, continue processing
                    pass

            nodo.visitar(self)
        
        # Mae...nos fijamos en los hijos para ver que tipo de dato es
        if nodo_actual.hijos:

            primer_hijo = nodo_actual.hijos[0]
            if 'tipo' in primer_hijo.atributos:
                if primer_hijo.atributos['tipo'] in [TiposDato.ENTERO, TiposDato.FLOTANTE, TiposDato.NUMERO]:
                    nodo_actual.atributos['tipo'] = primer_hijo.atributos['tipo']
                elif primer_hijo.atributos['tipo'] == TiposDato.TEXTO:
                    nodo_actual.atributos['tipo'] = TiposDato.NUMERO
                else:
                    nodo_actual.atributos['tipo'] = TiposDato.NUMERO
            else:
                nodo_actual.atributos['tipo'] = TiposDato.NUMERO
        else:
            nodo_actual.atributos['tipo'] = TiposDato.NUMERO
         


    def ___visitar_expresion(self,  nodo_actual):
        '''2 expresiones matematicas con su operador'''

        """
        Expresion ::= ajustar ExpresionMatematica Operador ExpresionMatematica
        """

        for nodo in nodo_actual.hijos:
            if nodo.tipo == TipoNodo.IDENTIFICADOR:
                try:
                    registro = self.tabla_simbolos.verificar_existencia(nodo.valor)
                except:
                    pass  # Continue if not found
            nodo.visitar(self)

        # lo matematico debe de terminar siendo numero, manda huevo
        nodo_actual.atributos['tipo'] = TiposDato.NUMERO

    
    def __visitar_funcion(self,  nodo_actual):
        '''Funcion, def_funcion, tengo que ver que puto desmadre hicieron esos maes con el arbol'''
        # primero la funcion, luego el resto, por eso se abre el bloque
        self.tabla_simbolos.nuevo_registro(nodo_actual, TiposDato.FUNCION, nodo_actual.valor)
        self.tabla_simbolos.abrir_bloque()  # Abrimos un bloque para la funcion
        
        for nodo in nodo_actual.hijos:
            if nodo is not None:
                nodo.visitar(self)
        
        self.tabla_simbolos.cerrar_bloque()  # Cerramos el bloque de la funcion

        # nos fijamos en los hijos para saber que van a ser
        if len(nodo_actual.hijos) > 2 and nodo_actual.hijos[2] is not None and 'tipo' in nodo_actual.hijos[2].atributos:

            nodo_actual.atributos['tipo'] = nodo_actual.hijos[2].atributos['tipo']
        else:
            # si no hay nada, es ninguno
            nodo_actual.atributos['tipo'] = TiposDato.NINGUNO

    def __visitar_flotante(self,  nodo_actual):
        """
        Verifica si el tipo del componente lexico actuales de tipo FLOTANTE

        Flotante ::= -?[0-9]+.[0-9]+
        """
        nodo_actual.atributos['tipo'] = TiposDato.NUMERO  # igual que con integer, todo es numero

    def __visitar_identificador(self,  nodo_actual):
        '''Identificador es una variable o una funcion??'''

        """
        Di mae identificador puede ser cualquier vara que no caiga dentro de lo otro
        Identificador ::= [a-zA-Z_]([a-zA-z0-9])*
        """
        # mae, nos fijamos en la tabla de simbolos
        try:
            registro = self.tabla_simbolos.verificar_existencia(nodo_actual.valor)
            # Use the type from the symbol table entry
            if 'Tipo' in registro:
                nodo_actual.atributos['tipo'] = registro['Tipo']
            elif 'tipo' in registro['Referencia'].atributos:
                nodo_actual.atributos['tipo'] = registro['Referencia'].atributos['tipo']
            else:
                nodo_actual.atributos['tipo'] = TiposDato.CUALQUIERA
        except:
            # Mae, di es cualquiera
            nodo_actual.atributos['tipo'] = TiposDato.CUALQUIERA

    def __visitar_invocacion(self,  nodo_actual):
        """
        Invocacion ::= Identificador ( ParametrosInvocacion )
        """
        '''Invocacion es una funcion que se invoca, o sea se llama'''

        # nos fijamos si los mocosos estan o si son validos
        if not nodo_actual.hijos or not nodo_actual.hijos[0]:

            nodo_actual.atributos['tipo'] = TiposDato.ERROR
            return

        try:
            busqueda = self.tabla_simbolos.verificar_existencia(nodo_actual.hijos[0].valor) #Mae la busqueda lo busca a ver si es algo real o no

            if busqueda['Referencia'].tipo != TipoNodo.FUNCION:
                raise Exception("No es una funcion, no se puede invocar", busqueda)
            

            for nodo in nodo_actual.hijos:
                if nodo is not None:
                    nodo.visitar(self)

            # 
            if 'tipo' in busqueda['Referencia'].atributos:
                nodo_actual.atributos['tipo'] = busqueda['Referencia'].atributos['tipo']
            elif 'Tipo' in busqueda:
                nodo_actual.atributos['tipo'] = busqueda['Tipo']
            else:
                nodo_actual.atributos['tipo'] = TiposDato.NINGUNO
        except:
            # si no existe o algo, ERROR
            for nodo in nodo_actual.hijos:
                if nodo is not None:
                    nodo.visitar(self)
            nodo_actual.atributos['tipo'] = TiposDato.ERROR

    def __visitar_instruccion(self,  nodo_actual):
        '''Instruccion ::= (Repeticion | Bifurcacion | Asignacion | Invocacion | Retorno | Error | Comentario )'''
        # Visit children to get their types
        for nodo in nodo_actual.hijos:
            if nodo is not None:
                nodo.visitar(self)
        
        # Instructions inherit type from their first child
        if nodo_actual.hijos and nodo_actual.hijos[0] is not None and 'tipo' in nodo_actual.hijos[0].atributos:
            nodo_actual.atributos['tipo'] = nodo_actual.hijos[0].atributos['tipo']
        else:
            nodo_actual.atributos['tipo'] = TiposDato.CUALQUIERA

    ##def __visitar_literal(self,  nodo_actual):
    ##    '''Literal es un valor literal, o sea un numero, una cadena, un booleano, etc'''

    def __visitar_matematica(self,  nodo_actual):
        '''Matematica es una operacion matematica'''
        for nodo in nodo_actual.hijos:
            if nodo.tipo == TipoNodo.IDENTIFICADOR:
                try:
                    registro = self.tabla_simbolos.verificar_existencia(nodo.valor)
                except:
                    pass  # Continue if not found
            nodo.visitar(self)
        
        # Mathematical operations result in NUMERO type
        nodo_actual.atributos['tipo'] = TiposDato.NUMERO

    def __visitar_michelin(self,  nodo_actual):
        '''Michelin es el programa principal, o sea el def por asi decirlo playo'''
    
        for nodo in nodo_actual.hijos:
            nodo.visitar(self)

        nodo_actual.atributos['tipo'] = nodo_actual.hijos[0].atributos['tipo']  
    
    
    def __visitar_operador(self,  nodo_actual):
        '''Operador es un operador matematico, como +, -, *, /'''

        nodo_actual.atributos['tipo'] = TiposDato.NUMERO  #operadores de algo son numeros, no voy a dividir M entre N

    def _visitar_parametros(self,  nodo_actual): 
        '''Visita los párametros de una función o invocación'''
        for nodo in nodo_actual.hijos:
            nodo.visitar(self)
        nodo_actual.atributos['tipo'] = TiposDato.NINGUNO  # Parameters don't have a specific type

    def _visitar_parametros_funcion(self,  nodo_actual):
        '''Parametros de una funcion, registramos cada parametro con tipo NUMERO por defecto'''
        for nodo in nodo_actual.hijos:
            # Los parametros usualmente son numeros
            self.tabla_simbolos.nuevo_registro(nodo, TiposDato.NUMERO, nodo.valor)
            nodo.atributos['tipo'] = TiposDato.NUMERO
            nodo.visitar(self)
        
        nodo_actual.atributos['tipo'] = TiposDato.NINGUNO  # Parameters don't have a specific type


    def _visitar_parametros_invocacion(self,  nodo_actual):
        '''Parametros de una invocacion, o sea los parametros que se le pasan a una funcion al invocarla'''
        for nodo in nodo_actual.hijos:
            if nodo.tipo == TipoNodo.IDENTIFICADOR:
                try:
                    registro = self.tabla_simbolos.verificar_existencia(nodo.valor)
                except:
                    # If identifier doesn't exist, continue processing
                    pass
            
            elif nodo.tipo == TipoNodo.FUNCION:
                raise Exception("Es una funcion, nada que ver con invocacion", nodo.valor)
        
            nodo.visitar(self)

    def __visitar_print(self,  nodo_actual):  
        '''Para printear'''
        for nodo in nodo_actual.hijos:
            nodo.visitar(self)
        nodo_actual.atributos['tipo'] = TiposDato.NINGUNO  # print es ninguno
        
    def __visitar_palabra_clave(self,  nodo_actual):  
        '''Mae, las palabras clave que tengamos'''
        nodo_actual.atributos['tipo'] = TiposDato.NINGUNO  # Palabras clave son nada

    def __visitar_programa(self,  nodo_actual):
        '''Programa es el michelin si mal no me acuerdo'''
        for nodo in nodo_actual.hijos:
            if nodo is not None:
                nodo.visitar(self)
        nodo_actual.atributos['tipo'] = nodo_actual.hijos[0].atributos['tipo'] if nodo_actual.hijos and nodo_actual.hijos[0] is not None and 'tipo' in nodo_actual.hijos[0].atributos else TiposDato.CUALQUIERA

    def __visitar_repeticion(self,  nodo_actual):
        '''Repeticion es un bucle, o sea un for o un while'''
        """
        Repeticion ::= Integrar ( Condicion ) BloqueInstrucciones
        """
        self.tabla_simbolos.abrir_bloque()  # Abrimos un bloque para la repeticion

        for nodo in nodo_actual.hijos:
            nodo.visitar(self)

        self.tabla_simbolos.cerrar_bloque()  # Cerramos el bloque de la repeticion

        nodo_actual.atributos['tipo'] = nodo_actual.hijos[1].atributos['tipo']  # Retorna el tipo

    def __visitar_retorno(self, nodo_actual):
        '''Retorno es el return de una función'''
        
        if not nodo_actual.hijos:
            # Si no hay hijos...nada pues
            nodo_actual.atributos['tipo'] = TiposDato.NINGUNO
            return
        
        for nodo in nodo_actual.hijos:
            if nodo.tipo == TipoNodo.IDENTIFICADOR:
                try:
                    # Primero revisemos que haya algo y despues el tipo
                    registro = self.tabla_simbolos.verificar_existencia(nodo.valor)
                    nodo_actual.atributos['tipo'] = registro['Referencia'].atributos.get('tipo', TiposDato.CUALQUIERA)
                except:
                    nodo_actual.atributos['tipo'] = TiposDato.CUALQUIERA
            else:
                nodo.visitar(self)
                
                nodo_actual.atributos['tipo'] = nodo.atributos.get('tipo', TiposDato.CUALQUIERA)

    def __visitar_texto(self,  nodo_actual):
        """
        Verifica si el tipo del componente lexico actuales de tipo TEXTO

        Texto ::= ~/\w(\s\w)*)?~
        """

        nodo_actual.atributos['tipo'] = TiposDato.TEXTO
        #Di mae....el tipo es texto asi que lo ponemos como texto

    def __visitar_valor_verdadero(self,  nodo_actual):
    
        """
        CRUDO_VALOR_VERDAD ::= (True | False)
        """

        nodo_actual.atributos['tipo'] = TiposDato.VALOR_VERDAD

        #Se le pone el tipo de valor que es verdadero, creo que booleano podria ir aca? pero puse ese por si las varas I guess

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
            print("\n\n\n\n\n\n\n\n")
            self.Arbol.imprimir()
    def __AmbienteEstandar(self):
        '''Mae aca estan las funciones estandar CREO que son todas, segun el pdf de documentacion, van en minuscula'''

        # Igual que antes pero aca esta mas bonito CREO YO que asi deberian de ser los tipos?
        funciones_estandar = [ 
            ('pelar', TiposDato.NINGUNO),     # y este era el numero que se resta, talvez NUMERO sirva?
            ('marinar', TiposDato.NINGUNO),   # Mae, acuerdese que era la variable que cambiaba el tiempo
            ('quemo', TiposDato.ERROR)
        ]

        for Nombre, tipo in funciones_estandar:
            nodo = Nodo(tipo=TipoNodo.FUNCION, valor=Nombre, atributos={'tipo': tipo})
            self.tabla_simbolos.nuevo_registro(nodo, tipo)

    def verificar(self):
        self.visitador._Visitante__visitar(self.Arbol.raiz)