from DocumentosUtiles.Arbol import ArbolSintaxisAbstracta, Nodo, TipoNodo

class VisitadorPython:
    tabuladores = 0


    def visitar(self, nodo: TipoNodo):
        """
        jaja, totalmente no es una copia del verificador
        """


        resultado = ""


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
            self.__visitar_bifurcacion(nodo) 
        
        elif nodo.tipo is TipoNodo.ELSE: 
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

        else: 

            raise Exception("Mae mi bro, que putas, aca no deberias estar")
        

    def __visitar_programa(self, nodo_actual):
        '''Programa es el michelin si mal no me acuerdo'''

        instrucciones = []

        for nodo in nodo_actual.hijos:
            self.visitar(nodo)
            instrucciones.append(nodo.visitar(self))

            return "\n".join(instrucciones)
        

    def __visitar_asignacion(self, nodo_actual):
        '''Asignacion es una variable que se le asigna un valor'''

        resultado = """{} = {}"""

        instrucciones = []

        for nodo in nodo_actual.hijos:
            instrucciones.append(nodo.visitar(self))

        return resultado.format(instrucciones[0], instrucciones[1])
    
    def __visitar_expresion_matematica(self, nodo_actual):
        """
        ExpresionMatematica ::= (Expresion) | Numero | Identificador

        Esta mica soportaria textos

        """
        instrucciones = []

        for nodo in nodo_actual.hijos:
            instrucciones += [nodo.visitar(self)]

        return ' '.join(instrucciones)
    
    def __visitar_expresion(self, nodo_actual):

        '''2 expresiones matematicas con su operador'''

        #for nodo in nodo_actual.hijos:

        """
        Expresion ::= ajustar ExpresionMatematica Operador ExpresionMatematica
        """

        instrucciones = []
        for nodo in nodo_actual.hijos:
            instrucciones+= [nodo.visitar(self)]

        return ' '.join(instrucciones)
    
    def __visitar_funcion(self, nodo_actual):
        
        resultado = """\ndef {}({}):\n{}"""

        instrucciones = []

        for nodo in nodo_actual.hijos:

            instrucciones += [nodo.visitar(self)]

        return resultado.format(instrucciones[0], instrucciones[1], '\n'.join(instrucciones[2]))
    
    def __visitar_invocacion(self, nodo_actual):
       resultado = """{}({})"""

       instrucciones = []

       for nodo in nodo_actual.hijos:
           instrucciones += [nodo.visitar(self)]

       return resultado.format(instrucciones[0],instrucciones[1])
    

    def __visitar_parametros_invocacion(self, nodo_actual):

        parametros = []

        for nodo in nodo_actual.hijos:
            parametros.append(nodo.visitar(self))

        if len(parametros) > 0: 
            return ', '.join(parametros)
        else:
            return ''
        

    def __visitar_parametros_funcion(self, nodo_actual):

        parametros = []

        for nodo in nodo_actual.hijos:
            parametros.append(nodo.visitar(self))

        if len(parametros) > 0: 
            return ', '.join(parametros)
        else:
            return ''
        
    def __visitar_instruccion(self, nodo_actual):
        
        valor = ""

        for nodo in nodo_actual.hijos:
            valor += nodo.visitar(self)

        return valor
    
    def __visitar_repeticion(self, nodo_actual):

        resultado = """while {}: \n{}"""

        instrucciones = []

        #Visitamos la condicion 
        for nodo in nodo_actual.hijos:
            instrucciones.append(nodo.visitar(self))

        return resultado.format(instrucciones[0], instrucciones[1])
    
    def __visitar_bifurcacion(self, nodo_actual):

        resultado = """{}{}"""

        instrucciones = []

        for nodo in nodo_actual.hijos:
            instrucciones.append(nodo.visitar(self))

        return resultado.format(instrucciones[0], '')




