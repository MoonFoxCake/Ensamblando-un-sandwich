from DocumentosUtiles.Arbol import ArbolSintaxisAbstracta, Nodo, TipoNodo

class VisitadorPython:
    tabuladores = 0

    def __visitar(self, nodo: TipoNodo):
        '''Se usa para visitar los nodos del arbol'''
        
        resultado = ''

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
            self.__visitar_bifurcacion(nodo) 

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
            raise Exception('Nunca va a usarse este else, pero es por si acaso')

        return resultado
        
    def __visitar_programa(self, nodo_actual):
        pass
    def __visitar_asignacion(self, nodo_actual):
        pass

    def __visitar_bifurcacion(self, nodo_actual):
        pass

    def __visitar_bloque_instrucciones(self, nodo_actual):
        pass

    def __visitar_comparacion(self, nodo_actual):
        pass

    def __visitar_comparador(self, nodo_actual):
        pass

    def __visitar_condicion(self, nodo_actual):
        pass

    def __visitar_funcion(self, nodo_actual):
        pass

    def __visitar_entero(self, nodo_actual):
        pass

    def __visitar_error(self, nodo_actual):
        pass

    def __visitar_expresion_matematica(self, nodo_actual):
        pass

    def __visitar_matematica(self, nodo_actual):
        pass

    def __visitar_flotante(self, nodo_actual):
        pass

    def __visitar_identificador(self, nodo_actual):
        pass

    def __visitar_instruccion(self, nodo_actual):
        pass

    def __visitar_invocacion(self, nodo_actual):
        pass

    def __visitar_operador(self, nodo_actual):
        pass

    def __visitar_palabra_clave(self, nodo_actual):
        pass

    def _visitar_parametros(self, nodo_actual):
        pass

    def _visitar_parametros_funcion(self, nodo_actual):
        pass

    def _visitar_parametros_invocacion(self, nodo_actual):
        pass

    def __visitar_michelin(self, nodo_actual):
        pass

    def __visitar_print(self, nodo_actual):
        pass

    def __visitar_repeticion(self, nodo_actual):
        pass

    def __visitar_retorno(self, nodo_actual):
        pass

    def __visitar_texto(self, nodo_actual):
        pass

    def __visitar_auxiliar(self, nodo_actual):
        pass

    def __visitar_valor_verdadero(self, nodo_actual):
        pass
    
    