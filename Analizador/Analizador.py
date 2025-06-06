from Explorador.Explorador import Componente, info_lexico
from DocumentosUtiles.Arbol import ArbolSintaxisAbstracta, Nodo, TipoNodo

class Analizador:

    componentes_lexicos = []
    cantidad_componentes = 0
    componente_actual = info_lexico

    def __init__(self, lista_componentes):
        self.componentes_lexicos = lista_componentes
        self.cantidad_componentes = len(lista_componentes)
        self.posicion_componente_actual = 0
        self.componente_actual = lista_componentes[0]
        self.asa = ArbolSintaxisAbstracta()

    def imprimir_asa(self):
        if self.asa.raiz is None:
            print([])
        else:
            self.asa.imprimir_preorden()
    
    def analizar(self):
        """
        Método principal que inicia el análisis siguiendo el esquema de
        análisis por descenso recursivo
        """
        self.asa.raiz = self.__analizar_programa()
    
    def __analizar_programa(self): #Listo
        nodos_nuevos = []
        # pueden venir múltiples asignaciones, funciones o prints (servir) 
        while (True):

            # Si es ciclo
            if self.componente_actual.texto == 'integrar':
                nodos_nuevos = [self.__analizar_repeticion()]

            # Si es "print"
            elif (self.componente_actual.texto == 'servir'): 
                nodos_nuevos += [self.__analizar_print()]
            
            # Si es asignación de variable
            elif (self.componente_actual.texto == 'incorporar'): 
                nodos_nuevos += [self.__analizar_asignacion()]

            # Si es definición de función
            elif (self.componente_actual.texto == 'michelin'): 
                nodos_nuevos += [self.__analizar_funcion()]

            else:
                break
        
        return Nodo(TipoNodo.PROGRAMA, nodos=nodos_nuevos)

    def __analizar_repeticion(self): 
        """
        Repetición ::= Integrar ( Condición ) BloqueInstrucciones
        """
        nodos_nuevos = []
        # Todos presentes en ese orden... sin opciones
        self.__verificar('integrar')
        nodos_nuevos += [self.__analizar_bloque_instrucciones()]
        return Nodo(TipoNodo.REPETICION, nodos=nodos_nuevos)
    
    def __analizar_bloque_instrucciones(self): #Listo
        """
        Analiza un bloque de instrucciones.
        Estructura:

            BloqueInstrucciones ::= { Instrucción+ }

        """
        nodos_nuevos = []

        # mínimo una
        nodos_nuevos += [self.__analizar_instruccion()]

        # Acá todo puede venir uno o más 
        while self.componente_actual.texto in ['integrar', 'if', 'return', 'servir' , 'else', 'elif', 'ajustar', 'incorporar', 'ajustar'] \
                or self.componente_actual.tipo == Componente.IDENTIFICADOR:  
        
            nodos_nuevos += [self.__analizar_instruccion()]

        return Nodo(TipoNodo.BLOQUE_INSTRUCCIONES, nodos=nodos_nuevos)
    
    def __analizar_instruccion(self): #Listo
        """
        Instrucción ::= (Repetición | Bifurcación | Asignación | Invocación | Retorno | Error | Comentario )

        Acá hay un error en la gramática por que no reconoce las
        Invocaciones por la falta de corregir un error en la gramática LL

        Invocación y Asignación ... ambas dos inician con un Identificador
        y acá no se sabe por cuál empezar.
        ...
        La solución en código que yo presentó acá esta sería como algo así

        Instrucción ::= (Repetición | Bifurcación | (Asignación | Invocación) | Retorno | Error | Comentario )

                                                    ^                       ^
        Ojo los paréntesis extra                    |                       |
        """

        nodos_nuevos = []        


        # Acá todo con if por que son opcionales
        if self.componente_actual.texto == 'integrar':
            nodos_nuevos += [self.__analizar_repeticion()]

        elif self.componente_actual.texto == 'if':
            nodos_nuevos += [self.__analizar_bifurcacion()]

        elif self.componente_actual.tipo == Componente.IDENTIFICADOR:
            if self.__componente_venidero().texto == "integrar": #Revisar con nuestra grámatica
                nodos_nuevos += [self.__analizar_asignacion()]
            else:
                nodos_nuevos += [self.__analizar_invocacion()]

        elif self.componente_actual.texto == 'servir': #Revisar con nuestra grámatica
            nodos_nuevos += [self.__analizar_print()]

        elif self.componente_actual.texto == 'return': #Revisar con nuestra grámatica
            nodos_nuevos += [self.__analizar_retorno()]

        elif self.componente_actual.texto == 'ajustar': #Revisar con nuestra grámatica
            nodos_nuevos += [self.__analizar_expresion()]

        else: # Muy apropiado el chiste de ir a revisar si tiene error al último.
            nodos_nuevos += [self.__analizar_error()]

        # Ignorado el comentario

        # Acá yo debería volarme el nivel Intrucción por que no aporta nada
        return Nodo(TipoNodo.INSTRUCCION, nodos=nodos_nuevos)

    def __analizar_error(self): #Listo
        self.__verificar_tipo_componente(Componente.ERROR)
        nodo = Nodo(TipoNodo.ERROR, contenido =self.componente_actual.texto)
        self.__pasar_siguiente_componente()
        return nodo

    def __analizar_bifurcacion(self):
        """
        Bifurcación ::= if (elif)* (else)?
        """
        return self.__analizar_if()  # Toda la lógica ahora está dentro del `if`
  
    def __analizar_if(self):
        """
        if ::= if BloqueInstrucciones (elif BloqueInstrucciones)* (else BloqueInstrucciones)?
        """
        nodos_nuevos = []

        self.__verificar('if')
        nodos_nuevos += [self.__analizar_bloque_instrucciones()]

        # Cero o más elif
        while self.componente_actual.texto == 'elif':
            nodos_nuevos += [self.__analizar_elif()]

        # Opcional un else
        if self.componente_actual.texto == 'else':
            nodos_nuevos += [self.__analizar_else()]

        return Nodo(TipoNodo.BIFURCACION, nodos=nodos_nuevos)

    def __analizar_else(self): #Listo
        """
        Else ::= else BloqueInstrucciones
        """

        nodos_nuevos = []

        # Todos presentes en ese orden... sin opciones
        self.__verificar('else')
        nodos_nuevos += [self.__analizar_bloque_instrucciones()]

        return Nodo(TipoNodo.ELSE, nodos=nodos_nuevos)

    def __analizar_elif(self): #Listo
        """
        Elif ::= elif BloqueInstrucciones
        """

        nodos_nuevos = []

        # Todos presentes en ese orden... sin opciones
        self.__verificar('elif')
        nodos_nuevos += [self.__analizar_bloque_instrucciones()]

        return Nodo(TipoNodo.ELIF, nodos=nodos_nuevos)

    def __analizar_expresion(self): #Listo
        """
        Expresión ::= ajustar ExpresiónMatemática Operador ExpresiónMatemática
        """

        nodos_nuevos = []

        self.__verificar('ajustar')

        nodos_nuevos += [self.__analizar_expresion()]

        nodos_nuevos += [self.__verificar_identificador()]

        self.__verificar('=')

        # Acá no hay nada que hacer todas son obligatorias en esas
        # posiciones
        nodos_nuevos += [self.__analizar_expresion_matematica()]

        nodos_nuevos += [self.__verificar_operador()]

        nodos_nuevos += [self.__analizar_expresion_matematica()]

        return Nodo(TipoNodo.EXPRESION , nodos=nodos_nuevos)
    
    def __analizar_expresion_matematica(self): #Listo
        """
        ExpresiónMatemática ::= (Expresión) | Número | Identificador
        """

        nodos_nuevos = []
        
        

        # Acá yo se que estan bien formados por que eso lo hizo el
        # explorador... es nada más revisar las posiciones.
        if self.componente_actual.tipo == Componente.ENTERO:
            nodos_nuevos += [self.__verificar_entero()]

        elif self.componente_actual.tipo == Componente.FLOTANTE:
            nodos_nuevos += [self.__verificar_flotante()]

        # Este código se simplifica si invierto la opción anterior y esta
        else:
            nodos_nuevos += [self.__verificar_identificador()]

        return Nodo(TipoNodo.EXPRESION_MATEMATICA, nodos=nodos_nuevos)

    def __verificar_operador(self): #Listo
        """
        Operador ::= (batir|colar|amasar|partir|sobras)
        """
        self.__verificar_tipo_componente(Componente.OPERADOR)

        nodo = Nodo(TipoNodo.OPERADOR, contenido =self.componente_actual.texto)
        self.__pasar_siguiente_componente()

        return nodo

    def __analizar_asignacion(self):  #Listo
        nodos_nuevos = []
        # El identificador en esta posición es obligatorio
        nodos_nuevos += [self.__verificar_identificador()]
        self.__verificar('=')
        # El siguiente bloque es de opcionales
        if self.componente_actual.tipo in [Componente.ENTERO, Componente.FLOTANTE, Componente.CRUDO_VALOR_VERDAD, Componente.TEXTO] :
            nodos_nuevos += [self.__analizar_literal()]

        # Acá tengo que decidir si es Invocación o solo un identificador
        elif self.componente_actual.tipo == Componente.IDENTIFICADOR:

            if self.__componente_venidero().texto == '(': #Revisar con nuestra grámatica el .texto
                nodos_nuevos += [self.__analizar_invocacion()]
            else:
                nodos_nuevos += [self.__verificar_identificador()]
        else:
            raise SyntaxError('Viejo... acá algo se quemó', self.componente_actual)

        return Nodo(TipoNodo.ASIGNACION, nodos=nodos_nuevos)
    
    def __analizar_literal(self): #Listo
        """
        Literal ::= (Número | Texto | ValorVerdad)
        """

        if self.componente_actual.tipo is Componente.TEXTO:
            nodo = self.__verificar_texto()

        elif  self.componente_actual.tipo is Componente.CRUDO_VALOR_VERDAD:
            nodo = self.__verificar_valor_verdad()

        else:
            nodo = self.__analizar_numero()

        return nodo
    
    def __analizar_numero(self): #Listo
        """
        Número ::= (Entero | Flotante)
        """
        if self.componente_actual.tipo == Componente.ENTERO:
            nodo = self.__verificar_entero()
        else:
            nodo = self.__verificar_flotante()

        return nodo

    def __verificar_entero(self): #Listo
        """
        Verifica si el tipo del componente léxico actuales de tipo ENTERO

        Entero ::= -?[0-9]+
        """
        self.__verificar_tipo_componente(Componente.ENTERO)

        nodo = Nodo(TipoNodo.ENTERO, valor =self.componente_actual.texto)
        self.__pasar_siguiente_componente()
        return nodo

    def __verificar_flotante(self): #Listo
        """
        Verifica si el tipo del componente léxico actuales de tipo FLOTANTE

        Flotante ::= -?[0-9]+\.[0-9]+
        """
        self.__verificar_tipo_componente(Componente.FLOTANTE)

        nodo = Nodo(TipoNodo.FLOTANTE, valor =self.componente_actual.texto)
        self.__pasar_siguiente_componente()
        return nodo
    
    def __verificar_valor_verdad(self):#Listo
        """
        CRUDO_VALOR_VERDAD ::= (True | False)
        """
        self.__verificar_tipo_componente(Componente.CRUDO_VALOR_VERDAD)

        nodo = Nodo(TipoNodo.VALOR_VERDAD, valor =self.componente_actual.texto)
        self.__pasar_siguiente_componente()
        return nodo
    
    def __verificar_texto(self): #Listo
        """
        Verifica si el tipo del componente léxico actuales de tipo TEXTO

        Texto ::= ~/\w(\s\w)*)?~
        """
        self.__verificar_tipo_componente(Componente.TEXTO)

        nodo = Nodo(TipoNodo.TEXTO, valor =self.componente_actual.texto)
        self.__pasar_siguiente_componente()
        return nodo
    
    def __analizar_invocacion(self):
        """
        Invocación ::= Identificador ( ParámetrosInvocación )
        """
        nodos_nuevos = []

        #todos son obligatorios en ese orden
        nodos_nuevos += [self.__verificar_identificador()]
        self.__verificar('(')
        nodos_nuevos += [self.__analizar_parametros_invocacion()]
        self.__verificar(')')

        return Nodo(TipoNodo.INVOCACION , nodos=nodos_nuevos)
    
    def __analizar_parametros_invocacion(self): #Listo
        """
        ParametrosInvocación ::= Valor (, Valor)+
        """
        nodos_nuevos = []

        # Fijo un valor tiene que haber
        nodos_nuevos += [self.__analizar_valor()]

        while( self.componente_actual.texto == ','):
            self.__verificar(',')
            nodos_nuevos += [self.__analizar_valor()]

        # Esto funciona con lógica al verrís... Si no revienta con error
        # asumimos que todo bien y seguimos.

        return Nodo(TipoNodo.PARA_INVOCACION , nodos=nodos_nuevos)
    
    def __verificar_identificador(self):
        """
        Verifica si el tipo del componente léxico actual es de tipo
        IDENTIFICADOR

        Identificador ::= [a-zA-Z_]([a-zA-z0-9])*
        """
        self.__verificar_tipo_componente(Componente.IDENTIFICADOR)

        nodo = Nodo(TipoNodo.IDENTIFICADOR, valor =self.componente_actual.texto)
        self.__pasar_siguiente_componente()
        return 
    
    def __verificar_tipo_componente(self, tipo_esperado ):
        """
        Verifica un componente por tipo... no hace mucho pero es para
        centralizar el manejo de errores
        """

        if self.componente_actual.tipo is not tipo_esperado:
            print()
            raise SyntaxError ((tipo_esperado, self.componente_actual.texto))
    
    def __pasar_siguiente_componente(self): #To do, revienta en el del profe también
        """
        Pasa al siguiente componente léxico

        Esto revienta por ahora
        """
        self.posicion_componente_actual += 1

        if self.posicion_componente_actual >= self.cantidad_componentes - 1:
            return

        self.componente_actual = \
                self.componentes_lexicos[self.posicion_componente_actual]

    def __analizar_print(self): #Listo
        """
        Imprimir :: servir (Valor)?
        """
        nodos_nuevos = []

        self.__verificar('servir')

        # Este hay que validarlo para evitar el error en caso de que no
        # aparezca
        if self.componente_actual.tipo in [Componente.IDENTIFICADOR, Componente.ENTERO, Componente.FLOTANTE, Componente.CRUDO_VALOR_VERDAD, Componente.TEXTO] :
            nodos_nuevos += [self.__analizar_valor()]

        # Sino todo bien...
        return Nodo(TipoNodo.PRINT, nodos=nodos_nuevos)
    
    def __analizar_funcion(self): #Listo
        nodos_nuevos = []

        nodos_nuevos += [self.__verificar_identificador()]
        self.__verificar('(')
        nodos_nuevos += [self.__analizar_parametros_funcion()]
        self.__verificar(')')

        self.__verificar('{')
        nodos_nuevos += [self.__analizar_bloque_instrucciones()]
        self.__verificar('}')
        # La función lleva el nombre del identificador
        return Nodo(TipoNodo.FUNCION, \
                valor=nodos_nuevos[0].valor, nodos=nodos_nuevos)

    def __analizar_parametros_funcion(self): #Listo
        """
        ParametrosFunción ::= Identificador (, Identificador)+
        """
        nodos_nuevos = []

        # Fijo un valor tiene que haber
        nodos_nuevos += [self.__verificar_identificador()]

        while( self.componente_actual.texto == ','):
            self.__verificar(',')
            nodos_nuevos += [self.__verificar_identificador()]

        # Esto funciona con lógica al verrís... Si no revienta con error
        # asumimos que todo bien y seguimos.

        return Nodo(TipoNodo.PARA_FUNCION , valor=nodos_nuevos)

    def __verificar(self, texto_esperado ): #Listo

        """
        Verifica si el texto del componente léxico actual corresponde con
        el esperado cómo argumento
        """

        if self.componente_actual.texto != texto_esperado:
            print()
            raise SyntaxError ((texto_esperado,self.componente_actual.texto)) 

        self.__pasar_siguiente_componente()

    def __analizar_retorno(self): #Listo
        """
        Retorno :: return (Valor)?
        """
        nodos_nuevos = []
        self.__verificar('return')

        # Este hay que validarlo para evitar el error en caso de que no
        # aparezca
        if self.componente_actual.tipo in [Componente.IDENTIFICADOR, Componente.ENTERO, Componente.FLOTANTE, Componente.CRUDO_VALOR_VERDAD, Componente.TEXTO] :
            nodos_nuevos += [self.__analizar_valor()]

        # Sino todo bien...
        return Nodo(TipoNodo.RETORNO, nodos=nodos_nuevos)
    
    def __analizar_valor(self): #Listo
        """
        Valor ::= (Identificador | Literal)
        """
        # Acá voy a cambiar el esquema de trabajo y voy a elminar algunos
        # niveles del árbol

        # El uno o el otro
        if self.componente_actual.tipo is Componente.IDENTIFICADOR:
            nodo = self.__verificar_identificador()
        else:
            nodo = self.__analizar_literal()

        return nodo