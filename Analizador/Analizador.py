from Explorador.Explorador import Componente, info_lexico
from DocumentosUtiles.Arbol import ArbolSintaxisAbstracta, Nodo, TipoNodo

class Analizador:

    componentes_léxicos : list
    cantidad_componentes: int
    componente_actual : info_lexico
 
    def __init__(self, lista_componentes): #Listo

        self.componentes_léxicos = lista_componentes
        self.cantidad_componentes = len(lista_componentes)

        self.posición_componente_actual = 0
        self.componente_actual = lista_componentes[0]

        self.asa = ArbolSintaxisAbstracta()

    def imprimir_asa(self): #Listo
        """
        Imprime el árbol de sintáxis abstracta
        """
            
        if self.asa.raiz is None:
            print([])
        else:
            self.asa.imprimir_preorden()


    def analizar(self): #Listo
        """
        Método principal que inicia el análisis siguiendo el esquema de
        análisis por descenso recursivo
        """
        self.asa.raiz = self.__analizar_programa()


    def __analizar_programa(self): #Listo
       

        nodos_nuevos = []

        # pueden venir múltiples asignaciones, funciones o prints (servir) 
        while (True):

            # Si es asignación
            if self.componente_actual.texto == 'incorporar':
                nodos_nuevos = [self.__analizar_asignación()]

            # Si es función
            elif (self.componente_actual.texto == 'servir'): 
                nodos_nuevos += [self.__analizar_print()]


            # Si es función
            elif (self.componente_actual.texto == 'michelin'): 
                nodos_nuevos += [self.__analizar_función()]

            else:
                break

        
        return Nodo(TipoNodo.PROGRAMA, nodos=nodos_nuevos)
        

    def __analizar_asignación(self):  #Listo

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
                nodos_nuevos += [self.__analizar_invocación()]
            else:
                nodos_nuevos += [self.__verificar_identificador()]

        else:
            raise SyntaxError('Viejo... acá algo se quemó', self.componente_actual)

        return Nodo(TipoNodo.ASIGNACION, nodos=nodos_nuevos)
    

    def __analizar_expresión_matemática(self): #Listo
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





    def __analizar_expresión(self): #Listo
        """
        Expresión ::= ajustar ExpresiónMatemática Operador ExpresiónMatemática
        """

        nodos_nuevos = []

        self.__verificar('ajustar')

        nodos_nuevos += [self.__analizar_expresión()]

        # Acá no hay nada que hacer todas son obligatorias en esas
        # posiciones
        nodos_nuevos += [self.__analizar_expresión_matemática()]

        nodos_nuevos += [self.__verificar_operador()]

        nodos_nuevos += [self.__analizar_expresión_matemática()]

        return Nodo(TipoNodo.EXPRESION , nodos=nodos_nuevos)

    def __analizar_función(self): #Listo
  

        nodos_nuevos = []

        # Esta sección es obligatoria en este orden
        self.__verificar('michelin')

        nodos_nuevos += [self.__verificar_identificador()]
        self.__verificar('(')
        nodos_nuevos += [self.__analizar_parámetros_función()]
        self.__verificar(')')

        self.__verificar('{')
        nodos_nuevos += [self.__analizar_bloque_instrucciones()]
        self.__verificar('}')
        # La función lleva el nombre del identificador
        return Nodo(TipoNodo.FUNCION, \
                contenido=nodos_nuevos[0].valor, nodos=nodos_nuevos) #revisar .contenido como se maneja en arbol

    def __analizar_invocación(self): #Listo
        """
        Invocación ::= Identificador ( ParámetrosInvocación )
        """
        nodos_nuevos = []

        #todos son obligatorios en ese orden
        nodos_nuevos += [self.__verificar_identificador()]
        self.__verificar('(')
        nodos_nuevos += [self.__analizar_parámetros_invocación()]
        self.__verificar(')')

        return Nodo(TipoNodo.INVOCACION , nodos=nodos_nuevos)
    


    def __analizar_parámetros_función(self): #Listo
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
    

    def __analizar_parámetros_invocación(self): #Listo
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
        


    def __analizar_instrucción(self): #Listo
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
            nodos_nuevos += [self.__analizar_repetición()]

        elif self.componente_actual.texto == 'if':
            nodos_nuevos += [self.__analizar_bifurcación()]

        elif self.componente_actual.tipo == Componente.IDENTIFICADOR:


            if self.__componente_venidero().texto == "integrar": #Revisar con nuestra grámatica
                nodos_nuevos += [self.__analizar_asignación()]
            else:
                nodos_nuevos += [self.__analizar_invocación()]

        elif self.componente_actual.texto == 'servir': #Revisar con nuestra grámatica
            nodos_nuevos += [self.__analizar_print()]

        elif self.componente_actual.texto == 'return': #Revisar con nuestra grámatica
            nodos_nuevos += [self.__analizar_retorno()]

        else: # Muy apropiado el chiste de ir a revisar si tiene error al último.
            nodos_nuevos += [self.__analizar_error()]

        # Ignorado el comentario

        # Acá yo debería volarme el nivel Intrucción por que no aporta nada
        return Nodo(TipoNodo.INSTRUCCION, nodos=nodos_nuevos)


    def __analizar_repetición(self): #LISTO
        """
        Repetición ::= Integrar ( Condición ) BloqueInstrucciones
        """
        nodos_nuevos = []

        # Todos presentes en ese orden... sin opciones
        self.__verificar('integrar')
        
        #nodos_nuevos += [self.__analizar_condición()] #No se usa en nuestra gramática

        # Yo acá tengo dos elecciones... creo otro nivel con Bloque de
        # instrucciones o pongo directamente las instrucciones en este
        # nivel... yo voy con la primera por facilidad... pero eso hace más
        # grande el árbol
        nodos_nuevos += [self.__analizar_bloque_instrucciones()]

        return Nodo(TipoNodo.REPETICION, nodos=nodos_nuevos)
        

    def __analizar_bifurcación(self): #Listo
        """
        Bifurcación ::= if  elif (else)? | else
        """
        nodos_nuevos = []

        # el sino es opcional
        nodos_nuevos += [self.__analizar_if()]

        if self.componente_actual.texto == 'else':
            nodos_nuevos += [self.__analizar_else()]
        elif self.componente_actual.texto == 'elif':
            nodos_nuevos += [self.__analizar_elif()]
        # y sino era solo el 'diay siii'
        return Nodo(TipoNodo.BIFURCACION, nodos=nodos_nuevos)

    def __analizar_if(self): #Listo
        """
        if ::= if ( Condición ) BloqueInstrucciones
        """
        nodos_nuevos = []

        # Todos presentes en ese orden... sin opciones
        self.__verificar('if')
        #nodos_nuevos += [self.__analizar_condición()] #No se usa en nuestra gramática
        

        nodos_nuevos += [self.__analizar_bloque_instrucciones()]

        return Nodo(TipoNodo.IF, nodos=nodos_nuevos)

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




    """   
    def __analizar_condición(self):
            
        # Condición ::= Comparación ((divorcio|casorio) Comparación)?
            
        nodos_nuevos = []

        # La primera sección obligatoria la comparación
        nodos_nuevos += [self.__analizar_comparación()]

        # Esta parte es opcional
        if self.componente_actual.tipo == Componente.PALABRA_CLAVE:

            # Acá estoy en problemas por que esto debió ser un nuevo nivel
            # en el árbol algo ási cómo OperadorLógico...  voy a hacer una
            # porquería... pero a ustedes les toca arreglarlo

            # opcional el AND o el OR
            if componente_actual.texto == 'divorcio':
                nodo(TipoNodo.OPERADOR_LÓGICO, contenido='divorcio')
                nodos_nuevos += [nodo]
                self.__verificar('divorcio')


            else: # Aquí hay potencial horrible para fallo
                nodo = Nodo(TipoNodo.OPERADOR_LÓGICO, contenido='casorio')
                nodos_nuevos += [nodo]

                self.__verificar('casorio')

            # Un poco tieso, pero funcional
            nodos_nuevos += [self.__analizar_comparación()]

        # Si no ha reventado vamos bien
        return Nodo(TipoNodo.CONDICIÓN, nodos=nodos_nuevos)
    """   

















    def __analizar_comparación(self): #Listo
        """
        Comparación ::= Valor Comparador Valor
        """
        nodos_nuevos = []

        # Sin opciones, todo se analiza
        nodos_nuevos += [self.__analizar_valor()]
        nodos_nuevos += [self.__verificar_comparador()]
        nodos_nuevos += [self.__analizar_valor()]

        return Nodo(TipoNodo.COMPARACIÓN, nodos=nodos_nuevos)
 
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

    def __analizar_error(self): #Listo
        
        #Error ::= Error Valor
        
        nodos_nuevos = []        

        # Sin opciones
        self.__verificar_tipo_componente(Componente.ERROR)
        nodo = Nodo(TipoNodo.ERROR, contenido =self.componente_actual.texto)
        self.__pasar_siguiente_componente()
        return nodo
    


    """
    def __analizar_principal(self):
        
        # Esta versión esta chocha por que no cumple con ser una gramática LL  Principal ::= (Comentario)?  mae (jefe | jefa) BloqueInstrucciones
        
        nodos_nuevos = []
        # Ya en este punto estoy harto de poner comentarios

        if self.componente_actual.texto == 'jefa':
            self.__verificar('jefa')
        else:
            self.__verificar('jefe')

        self.__verificar('mae')

        nodos_nuevos += [self.__analizar_bloque_instrucciones()]

        return Nodo(TipoNodo.PRINCIPAL, nodos=nodos_nuevos)
    """


    def __analizar_literal(self): #Listo
        """
        Literal ::= (Número | Texto | ValorVerdad)
        """

        # Acá le voy a dar vuelta por que me da pereza tanta validación
        if self.componente_actual.tipo is Componente.TEXTO:
            nodo = self.__verificar_texto()

        elif  self.componente_actual.tipo is Componente.CRUDO_VALOR_VERDAD:
            nodo = self.__verificar_valor_verdad()

        else:
            nodo = self.__analizar_número()

        return nodo

    def __analizar_número(self): #Listo
        """
        Número ::= (Entero | Flotante)
        """
        if self.componente_actual.tipo == Componente.ENTERO:
            nodo = self.__verificar_entero()
        else:
            nodo = self.__verificar_flotante()

        return nodo
    




    # NO ENTENDIIIII ESSTO, PORFA REVISAR



    def __analizar_bloque_instrucciones(self): #Listo
        """
        Este es nuevo y me lo inventé para simplicicar un poco el código...
        correspondería actualizar la gramática.

        BloqueInstrucciones ::= { Instrucción+ }
        """
        nodos_nuevos = []

        # mínimo una
        nodos_nuevos += [self.__analizar_instrucción()]

        # Acá todo puede venir uno o más 
        while self.componente_actual.texto in ['integrar', 'if', 'return', 'quemo'] \
                or self.componente_actual.tipo == Componente.IDENTIFICADOR:  #Se puso quemo en vez de Error
        
            nodos_nuevos += [self.__analizar_instrucción()]

        return Nodo(TipoNodo.BLOQUE_INSTRUCCIONES, nodos=nodos_nuevos)













    def __verificar_operador(self): #Listo
        """
        Operador ::= (batir|colar|amasar|partir|sobras)
        """
        self.__verificar_tipo_componente(Componente.OPERADOR)

        nodo = Nodo(TipoNodo.OPERADOR, contenido =self.componente_actual.texto)
        self.__pasar_siguiente_componente()

        return nodo

    def __verificar_valor_verdad(self):#Listo
        """
        CRUDO_VALOR_VERDAD ::= (True | False)
        """
        self.__verificar_tipo_componente(Componente.CRUDO_VALOR_VERDAD)

        nodo = Nodo(TipoNodo.VALOR_VERDAD, contenido =self.componente_actual.texto)
        self.__pasar_siguiente_componente()
        return nodo

    def __verificar_comparador(self):#Listo
        """
        Comparador ::= mismo_sabor_que|mas_sazonado_que|menos_cocido_que|tan_horneado_como|tan_dulce_como
        """
        self.__verificar_tipo_componente(Componente.COMPARADOR)

        nodo = Nodo(TipoNodo.COMPARADOR, contenido =self.componente_actual.texto)
        self.__pasar_siguiente_componente()
        return nodo

    def __verificar_texto(self): #Listo
        """
        Verifica si el tipo del componente léxico actuales de tipo TEXTO

        Texto ::= ~/\w(\s\w)*)?~
        """
        self.__verificar_tipo_componente(Componente.TEXTO)

        nodo = Nodo(TipoNodo.TEXTO, contenido =self.componente_actual.texto)
        self.__pasar_siguiente_componente()
        return nodo


    def __verificar_entero(self): #Listo
        """
        Verifica si el tipo del componente léxico actuales de tipo ENTERO

        Entero ::= -?[0-9]+
        """
        self.__verificar_tipo_componente(Componente.ENTERO)

        nodo = Nodo(TipoNodo.ENTERO, contenido =self.componente_actual.texto)
        self.__pasar_siguiente_componente()
        return nodo


    def __verificar_flotante(self): #Listo
        """
        Verifica si el tipo del componente léxico actuales de tipo FLOTANTE

        Flotante ::= -?[0-9]+\.[0-9]+
        """
        self.__verificar_tipo_componente(Componente.FLOTANTE)

        nodo = Nodo(TipoNodo.FLOTANTE, contenido =self.componente_actual.texto)
        self.__pasar_siguiente_componente()
        return nodo


    def __verificar_identificador(self): #Listo
        """
        Verifica si el tipo del componente léxico actuales de tipo
        IDENTIFICADOR

        Identificador ::= [a-zA-Z_]([a-zA-z0-9])*
        """
        self.__verificar_tipo_componente(Componente.IDENTIFICADOR)

        nodo = Nodo(TipoNodo.IDENTIFICADOR, valor =self.componente_actual.texto)
        self.__pasar_siguiente_componente()
        return nodo


    def __verificar(self, texto_esperado ): #Listo

        """
        Verifica si el texto del componente léxico actual corresponde con
        el esperado cómo argumento
        """

        if self.componente_actual.texto != texto_esperado:
            print()
            raise SyntaxError ((texto_esperado,self.componente_actual.texto)) 

        self.__pasar_siguiente_componente()


    def __verificar_tipo_componente(self, tipo_esperado ): #Listo
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
        self.posición_componente_actual += 1

        if self.posición_componente_actual >= self.cantidad_componentes - 1:
            return

        self.componente_actual = \
                self.componentes_léxicos[self.posición_componente_actual]


    def __componente_venidero(self, avance=1): #Listo
        """
        Retorna el componente léxico que está 'avance' posiciones más adelante... por default el siguiente. Esto sin adelantar el
        contador del componente actual.
        """
        return self.componentes_léxicos[self.posición_componente_actual+avance]




