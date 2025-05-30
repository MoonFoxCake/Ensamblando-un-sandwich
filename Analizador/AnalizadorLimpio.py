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
        Metodo principal que inicia el analisis siguiendo el esquema de
        analisis por descenso recursivo
        """
        self.asa.raiz = self.__analizar_programa()
    
    def __analizar_programa(self): #Listo
        nodos_nuevos = []
        # pueden venir multiples asignaciones, funciones o prints (servir) 
        while (True):

            # Si es ciclo
            if (self.componente_actual.texto == 'michelin'): 
                nodos_nuevos += [self.__analizar_def_funcion()]

            else:
                if self.componente_actual ==  self.componentes_lexicos[-1]:
                    break
                else:
                    nodos_nuevos += [self.__analizar_instruccion()]

        return Nodo(TipoNodo.PROGRAMA, nodos_nuevos)

    def __analizar_palabra_clave(self): #Listo
        """
        PalabraClave ::= (michelin | servir | ajustar | dingding | marinar | pelar)
        """
        self.__verificar_tipo_componente(Componente.PALABRA_CLAVE)

        nodo = Nodo(TipoNodo.PALABRA_CLAVE, valor =self.componente_actual.texto)
        self.__pasar_siguiente_componente()
        return nodo

    def __analizar_repeticion(self): 
        """
        Repeticion ::= Integrar ( Condicion ) BloqueInstrucciones
        """
        nodos_nuevos = []
        # Todos presentes en ese orden... sin opciones
        
        nodos_nuevos += [self.__analizar_palabra_clave()]
        self.__verificar('(')
        # Toma los parametros de la condicion
        nodos_nuevos += [self.__analizar_condicion()]

        self.__verificar(')')
        # Ahora pasamos al bloque de instrucciones
        self.__verificar('{')
        nodos_nuevos += [self.__analizar_bloque_instrucciones()]
        self.__verificar('}')

        return Nodo(TipoNodo.REPETICION, nodos_nuevos)
    
    def __analizar_bloque_instrucciones(self): #Listo
        """
        Analiza un bloque de instrucciones.
        Estructura:

            BloqueInstrucciones ::= { Instruccion+ }

        """
        nodos_nuevos = []

        # minimo una
        nodos_nuevos += [self.__analizar_instruccion()]

        # Aca todo puede venir uno o mas 
        while self.componente_actual.texto in ['integrar', 'if', 'dingding', 'servir' , 'else', 'elif', 'ajustar', 'incorporar', 'marinar', 'pelar','michelin'] \
                or self.componente_actual.tipo == Componente.IDENTIFICADOR:  
        
            nodos_nuevos += [self.__analizar_instruccion()]

        return Nodo(TipoNodo.BLOQUE_INSTRUCCIONES, nodos_nuevos)
    
    def __analizar_instruccion(self): #Listo
        """
        Instruccion ::= (Repeticion | Bifurcacion | Asignacion | Invocacion | Retorno | Error | Comentario )

        Aca hay un error en la gramatica por que no reconoce las
        Invocaciones por la falta de corregir un error en la gramatica LL

        Invocacion y Asignacion ... ambas dos inician con un Identificador
        y aca no se sabe por cual empezar.
        ...
        La solucion en codigo que yo presento aca esta seria como algo asi

        Instruccion ::= (Repeticion | Bifurcacion | (Asignacion | Invocacion) | Retorno | Error | Comentario )

                                                    ^                       ^
        Ojo los parentesis extra                    |                       |
        """

        nodos_nuevos = []        
        # Aca todo con if por que son opcionales
        if self.componente_actual.texto == 'integrar':
            nodos_nuevos += [self.__analizar_repeticion()]

        elif self.componente_actual.texto == 'michelin':
            nodos_nuevos += [self.__analizar_def_funcion()]

        elif self.componente_actual.texto == 'if':
            nodos_nuevos += [self.__analizar_bifurcacion()]

        elif self.componente_actual.texto == 'incorporar':
            nodos_nuevos += [self.__analizar_asignacion()]

        elif self.componente_actual.texto == 'servir': #Revisar con nuestra gramatica
            nodos_nuevos += [self.__analizar_print()]

        elif self.componente_actual.texto == 'dingding': #Revisar con nuestra gramatica
            nodos_nuevos += [self.__analizar_retorno()]

        elif self.componente_actual.texto == 'ajustar': #Revisar con nuestra gramatica
            nodos_nuevos += [self.__analizar_expresion()]

        elif self.componente_actual.texto == 'marinar' or self.componente_actual.texto == 'pelar':
            nodos_nuevos += [self.__analizar_auxiliar()]
        
        elif self.componente_actual.tipo == Componente.IDENTIFICADOR:
            nodos_nuevos += [self.__analizar_invocacion()]

        
        else: # Muy apropiado el chiste de ir a revisar si tiene error al ultimo.
            nodos_nuevos += [self.__analizar_error()]

        # Ignorado el comentario

        # Aca yo deberia volarme el nivel Intruccion por que no aporta nada
        return Nodo(TipoNodo.INSTRUCCION, nodos_nuevos)
    
    def __analizar_auxiliar(self): #Listo
        """
        Auxiliar ::= (marinar|pelar) (Valor)?
        """
        nodos_nuevos = []

        # Este hay que validarlo para evitar el error en caso de que no
        # aparezca
        nodos_nuevos += [self.__analizar_palabra_clave()]
        # Reconoce la variable
        if self.componente_actual.tipo in [Componente.IDENTIFICADOR] :
            nodos_nuevos += [self.__analizar_valor()]
        else:
            raise SyntaxError('Una función auxiliar requiere de una variable.', self.componente_actual)
        
        return Nodo(TipoNodo.AUXILIAR, nodos_nuevos)

    def __analizar_error(self): #Listo
        self.__verificar_tipo_componente(Componente.ERROR)
        nodo = Nodo(TipoNodo.ERROR, contenido =self.componente_actual.texto)
        self.__pasar_siguiente_componente()
        return nodo

    def __analizar_bifurcacion(self):
        """
        Bifurcacion ::= if (elif)* (else)?
        """

        nodos_nuevos = []

        if self.componente_actual.texto == 'if':
            nodos_nuevos += [self.__analizar_if()]

        # Cero o mas elif
        while self.componente_actual.texto == 'elif':
            nodos_nuevos += [self.__analizar_elif()]

        # Opcional un else
        if self.componente_actual.texto == 'else':
            nodos_nuevos += [self.__analizar_else()]

        return Nodo(TipoNodo.BIFURCACION, nodos_nuevos)
     

    
    def __analizar_if(self):
        """
        if ::= if BloqueInstrucciones (elif BloqueInstrucciones)* (else BloqueInstrucciones)?
        """
        nodos_nuevos = []

        self.__verificar('if')

        self.__verificar('(')
        nodos_nuevos += [self.__analizar_condicion()]
        self.__verificar(')')
        self.__verificar('{')
        nodos_nuevos += [self.__analizar_bloque_instrucciones()]
        self.__verificar('}')

        return Nodo(TipoNodo.IF, nodos_nuevos)

    def __analizar_else(self): #Listo
        """
        Else ::= else BloqueInstrucciones
        """

        nodos_nuevos = []

        # Todos presentes en ese orden... sin opciones
        self.__verificar('else')
        self.__verificar('{')
        nodos_nuevos += [self.__analizar_bloque_instrucciones()]
        self.__verificar('}')

        return Nodo(TipoNodo.ELSE, nodos_nuevos)

    def __analizar_elif(self): #Listo
        """
        Elif ::= elif BloqueInstrucciones
        """

        nodos_nuevos = []

        # Todos presentes en ese orden... sin opciones
        self.__verificar('elif')
        self.__verificar('(')
        nodos_nuevos += [self.__analizar_condicion()]
        self.__verificar(')')
        self.__verificar('{')
        nodos_nuevos += [self.__analizar_bloque_instrucciones()]
        self.__verificar('}')

        return Nodo(TipoNodo.ELIF, nodos_nuevos)

    def __analizar_expresion(self): #Listo
        """
        Expresion ::= ajustar ExpresionMatematica Operador ExpresionMatematica
        """

        nodos_nuevos = []

        nodos_nuevos += [self.__analizar_palabra_clave()]
        nodos_nuevos += [self.__verificar_identificador()]
        self.__verificar('=') # Aca no hay nada que hacer todas son obligatorias en esas
        # Aca no hay nada que hacer todas son obligatorias en esas
        # posiciones
        nodos_nuevos += [self.__analizar_expresion_matematica()]

        nodos_nuevos += [self.__verificar_operador()]

        nodos_nuevos += [self.__analizar_expresion_matematica()]

        return Nodo(TipoNodo.EXPRESION_MATEMATICA, nodos_nuevos)
    
    def __analizar_expresion_matematica(self): #Listo
        """
        ExpresionMatematica ::= (Expresion) | Numero | Identificador
        """

        nodos_nuevos = []
        
        

        # Aca yo se que estan bien formados por que eso lo hizo el
        # explorador... es nada mas revisar las posiciones.
        if self.componente_actual.tipo == Componente.ENTERO:
            nodos_nuevos += [self.__verificar_entero()]

        elif self.componente_actual.tipo == Componente.FLOTANTE:
            nodos_nuevos += [self.__verificar_flotante()]

        # Este codigo se simplifica si invierto la opcion anterior y esta
        elif self.componente_actual.tipo == Componente.IDENTIFICADOR:
            nodos_nuevos += [self.__verificar_identificador()]

        else:
            nodos_nuevos += [self.__verificar_texto()]

        return Nodo(TipoNodo.VARIABLE_MATEMATICA, nodos_nuevos)

    def __verificar_operador(self): #Listo
        """
        Operador ::= (batir|colar|amasar|partir|sobras)
        """
        self.__verificar_tipo_componente(Componente.OPERADOR)

        nodo = Nodo(TipoNodo.OPERADOR, valor =self.componente_actual.texto)
        self.__pasar_siguiente_componente()

        return nodo

    def __analizar_asignacion(self):  #Listo
        nodos_nuevos = []
        nodos_nuevos += [self.__analizar_palabra_clave()]
        nodos_nuevos += [self.__verificar_identificador()]
        self.__verificar('=')
        # El siguiente bloque es de opcionales
        if self.componente_actual.tipo in [Componente.ENTERO, Componente.FLOTANTE, Componente.CRUDO_VALOR_VERDAD, Componente.TEXTO]: 
            nodos_nuevos += [self.__analizar_literal()]

        # Aca tengo que decidir si es Invocacion o solo un identificador
        elif self.componente_actual.tipo == Componente.IDENTIFICADOR:

            if self.__componente_venidero().texto == '(': 
                nodos_nuevos += [self.__analizar_invocacion()]
            else:
                nodos_nuevos += [self.__verificar_identificador()]
        else:
            raise SyntaxError('Viejo... aca algo se quemo', self.componente_actual)

        return Nodo(TipoNodo.ASIGNACION, nodos_nuevos)
    
    def __analizar_literal(self): #Listo
        """
        Literal ::= (Numero | Texto | ValorVerdad)
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
        Numero ::= (Entero | Flotante)
        """
        if self.componente_actual.tipo == Componente.ENTERO:
            nodo = self.__verificar_entero()
        else:
            nodo = self.__verificar_flotante()

        return nodo

    def __verificar_entero(self): #Listo
        """
        Verifica si el tipo del componente lexico actuales de tipo ENTERO

        Entero ::= -?[0-9]+
        """
        self.__verificar_tipo_componente(Componente.ENTERO)

        nodo = Nodo(TipoNodo.ENTERO, valor =self.componente_actual.texto)
        self.__pasar_siguiente_componente()
        return nodo

    def __verificar_flotante(self): #Listo
        """
        Verifica si el tipo del componente lexico actuales de tipo FLOTANTE

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
        Verifica si el tipo del componente lexico actuales de tipo TEXTO

        Texto ::= ~/\w(\s\w)*)?~
        """
        self.__verificar_tipo_componente(Componente.TEXTO)

        nodo = Nodo(TipoNodo.TEXTO, valor =self.componente_actual.texto)
        self.__pasar_siguiente_componente()
        return nodo
    
    def __analizar_invocacion(self):
        """
        Invocacion ::= Identificador ( ParametrosInvocacion )
        """
        nodos_nuevos = []

        #todos son obligatorios en ese orden
        nodos_nuevos += [self.__verificar_identificador()]
        if self.componente_actual.texto == '=' and self.__componente_venidero().tipo == Componente.IDENTIFICADOR: 
                                                     
            nodos_nuevos += [self.__verificar('=')]
            nodos_nuevos += [self.__verificar_identificador()]

        elif self.componente_actual.texto == '=' and self.__componente_venidero().tipo == Componente.ENTERO: 
            nodos_nuevos += [self.__verificar('=')]
            nodos_nuevos += [self.__verificar_entero()]
        elif self.componente_actual.texto == '=' and self.__componente_venidero().tipo == Componente.FLOTANTE:  
            nodos_nuevos += [self.__verificar('=')]
            nodos_nuevos += [self.__verificar_flotante()]
        elif self.componente_actual.texto == '=' and self.__componente_venidero().tipo == Componente.CRUDO_VALOR_VERDAD:
            nodos_nuevos += [self.__verificar('=')]
            nodos_nuevos += [self.__verificar_valor_verdad()]   
        elif self.componente_actual.texto == '=' and self.__componente_venidero().tipo == Componente.TEXTO:
            nodos_nuevos += [self.__verificar('=')]
            nodos_nuevos += [self.__verificar_texto()] 
        else:
            self.__verificar('(')
            nodos_nuevos += [self.__analizar_parametros_invocacion()]
            self.__verificar(')')

        return Nodo(TipoNodo.INVOCACION , nodos_nuevos)
    
    def __analizar_parametros_invocacion(self): #Listo
        """
        ParametrosInvocacion ::= Valor (, Valor)+
        """
        nodos_nuevos = []

        # Fijo un valor tiene que haber
        nodos_nuevos += [self.__analizar_valor()]

        while( self.componente_actual.texto == ','):
            self.__verificar(',')
            nodos_nuevos += [self.__analizar_valor()]

        # Esto funciona con logica al verris... Si no revienta con error
        # asumimos que todo bien y seguimos.

        return Nodo(TipoNodo.PARA_INVOCACION , nodos_nuevos)
    
    def __verificar_identificador(self):
        """
        Verifica si el tipo del componente lexico actual es de tipo
        IDENTIFICADOR

        Identificador ::= [a-zA-Z_]([a-zA-z0-9])*
        """
        self.__verificar_tipo_componente(Componente.IDENTIFICADOR)

        nodo = Nodo(TipoNodo.IDENTIFICADOR, valor =self.componente_actual.texto)
        self.__pasar_siguiente_componente()
        return nodo
    
    def __verificar_tipo_componente(self, tipo_esperado ):
        """
        Verifica un componente por tipo... no hace mucho pero es para
        centralizar el manejo de errores
        """

        if self.componente_actual.tipo is not tipo_esperado:
            print()
            raise SyntaxError ((tipo_esperado, self.componente_actual.tipo))
    
    def __pasar_siguiente_componente(self): #To do, revienta en el del profe tambien
        """
        Pasa al siguiente componente lexico

        Esto revienta por ahora
        """
        self.posicion_componente_actual += 1

        if self.posicion_componente_actual >= self.cantidad_componentes:
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
        return Nodo(TipoNodo.PRINT, nodos_nuevos)
    
    def __analizar_def_funcion(self): #Listo
        nodos_nuevos = []

        
        nodos_nuevos += [self.__analizar_palabra_clave()]
        nodos_nuevos += [self.__verificar_identificador()]

        if self.componente_actual.texto == '(' and self.__componente_venidero().texto == ')':
            self.__verificar('(')
            self.__verificar(')')
        else:
            self.__verificar('(')
            nodos_nuevos += [self.__analizar_parametros_funcion()]
            self.__verificar(')')

        self.__verificar('{')
        nodos_nuevos += [self.__analizar_bloque_instrucciones()]
        self.__verificar('}')
        return Nodo(TipoNodo.DEF_FUNCION, valor=nodos_nuevos)

    def __analizar_parametros_funcion(self): #Listo
        """
        ParametrosFuncion ::= Identificador (, Identificador)+
        """
        nodos_nuevos = []

        # Fijo un valor tiene que haber
        
        if self.__componente_venidero == ')':
            return Nodo(TipoNodo.PARAMETROS, nodos_nuevos)
        else:
            nodos_nuevos += [self.__verificar_identificador()]
            while( self.componente_actual.texto == ','):
                self.__verificar(',')
                nodos_nuevos += [self.__verificar_identificador()]

            # Esto funciona con logica al verris... Si no revienta con error
            # asumimos que todo bien y seguimos.

            return Nodo(TipoNodo.PARA_FUNCION , valor=nodos_nuevos)

    def __verificar(self, texto_esperado ): #Listo

        """
        Verifica si el texto del componente lexico actual corresponde con
        el esperado como argumento
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
        if self.componente_actual.texto == 'dingding':
            nodos_nuevos += [self.__analizar_palabra_clave()]
        # Este hay que validarlo para evitar el error en caso de que no
        # aparezca
        if self.componente_actual.tipo in [Componente.IDENTIFICADOR, Componente.ENTERO, Componente.FLOTANTE, Componente.CRUDO_VALOR_VERDAD, Componente.TEXTO] :
            nodos_nuevos += [self.__analizar_valor()]

        # Sino todo bien...
        return Nodo(TipoNodo.RETORNO, nodos_nuevos)
    
    def __analizar_valor(self): #Listo
        """
        Valor ::= (Identificador | Literal)
        """
        # Aca voy a cambiar el esquema de trabajo y voy a elminar algunos
        # niveles del arbol

        # El uno o el otro
        if self.componente_actual.tipo is Componente.IDENTIFICADOR:
            nodo = self.__verificar_identificador()
        else:
            nodo = self.__analizar_literal()

        return nodo
    
    def __componente_venidero(self, avance=1): #Listo
        """
        Retorna el componente lexico que esta 'avance' posiciones mas adelante... por default el siguiente. Esto sin adelantar el
        contador del componente actual.
        """
        return self.componentes_lexicos[self.posicion_componente_actual+avance]
    
    def __verificar_comparador(self):#Listo
        """
        Comparador ::= mismo_sabor_que|mas_sazonado_que|menos_cocido_que|tan_horneado_como|tan_dulce_como
        """
        self.__verificar_tipo_componente(Componente.COMPARADOR)

        nodo = Nodo(TipoNodo.COMPARADOR, valor =self.componente_actual.texto)
        self.__pasar_siguiente_componente()
        return nodo
    
    def __analizar_condicion(self):
        """
        Condicion ::= Comparador (ExpresionMatematica Operador ExpresionMatematica)
        """
        nodos_nuevos = []
        # Aca consumimos un numero o variable, luego un comparador y luego numero o variable
        
        nodos_nuevos += [self.__analizar_expresion_matematica()]
        nodos_nuevos += [self.__verificar_comparador()]
        nodos_nuevos += [self.__analizar_expresion_matematica()]
        return Nodo(TipoNodo.CONDICION, nodos_nuevos)