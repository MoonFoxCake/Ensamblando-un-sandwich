from DocumentosUtiles.Arbol import Nodo, TipoNodo

class VisitadorPython:
    tabuladores = 0

    def visitar(self, nodo: Nodo):
        return self.__visitar(nodo)

    def __visitar(self, nodo: Nodo):
        if nodo.tipo is TipoNodo.PROGRAMA:
            return self.__visitar_programa(nodo)
        
        elif nodo.tipo is TipoNodo.ASIGNACION:
            return self.__visitar_asignacion(nodo)
        
        elif nodo.tipo is TipoNodo.BIFURCACION:
            return self.__visitar_bifurcacion(nodo)
        
        elif nodo.tipo is TipoNodo.BLOQUE_INSTRUCCIONES:
            return self.__visitar_bloque_instrucciones(nodo)
        
        elif nodo.tipo is TipoNodo.COMPARACION:
            return self.__visitar_comparacion(nodo)
        
        elif nodo.tipo is TipoNodo.COMPARADOR:
            return self.__visitar_comparador(nodo)
        
        elif nodo.tipo is TipoNodo.CONDICION:
            return self.__visitar_condicion(nodo)
        
        elif nodo.tipo is TipoNodo.DEF_FUNCION or nodo.tipo is TipoNodo.FUNCION:
            return self.__visitar_funcion(nodo)
        
        elif nodo.tipo is TipoNodo.ELIF or nodo.tipo is TipoNodo.ELSE or nodo.tipo is TipoNodo.IF:
            return self.__visitar_bifurcacion(nodo)
        
        elif nodo.tipo is TipoNodo.ENTERO:
            return self.__visitar_entero(nodo)
        
        elif nodo.tipo is TipoNodo.ERROR:
            return self.__visitar_error(nodo)
        
        elif nodo.tipo is TipoNodo.EXPRESION_MATEMATICA:
            return self.__visitar_expresion_matematica(nodo)
        
        elif nodo.tipo is TipoNodo.VARIABLE_MATEMATICA:
            return self.__visitar_matematica(nodo)
        
        elif nodo.tipo is TipoNodo.FLOTANTE:
            return self.__visitar_flotante(nodo)
        
        elif nodo.tipo is TipoNodo.IDENTIFICADOR:
            return self.__visitar_identificador(nodo)
        
        elif nodo.tipo is TipoNodo.INSTRUCCION:
            return self.__visitar_instruccion(nodo)
        
        elif nodo.tipo is TipoNodo.INVOCACION:
            return self.__visitar_invocacion(nodo)
        
        elif nodo.tipo is TipoNodo.OPERADOR:
            return self.__visitar_operador(nodo)
        
        elif nodo.tipo is TipoNodo.PALABRA_CLAVE:
            return self.__visitar_palabra_clave(nodo)
        
        elif nodo.tipo is TipoNodo.PARAMETROS:
            return self._visitar_parametros(nodo)
        
        elif nodo.tipo is TipoNodo.PARA_FUNCION:
            return self._visitar_parametros_funcion(nodo)
        
        elif nodo.tipo is TipoNodo.PARA_INVOCACION:
            return self._visitar_parametros_invocacion(nodo)
        
        elif nodo.tipo is TipoNodo.PRINCIPAL:
            return self.__visitar_michelin(nodo)
        
        elif nodo.tipo is TipoNodo.PRINT:
            return self.__visitar_print(nodo)
        
        elif nodo.tipo is TipoNodo.REPETICION:
            return self.__visitar_repeticion(nodo)
        
        elif nodo.tipo is TipoNodo.RETORNO:
            return self.__visitar_retorno(nodo)
        
        elif nodo.tipo is TipoNodo.TEXTO:
            return self.__visitar_texto(nodo)
        
        elif nodo.tipo is TipoNodo.AUXILIAR:
            return self.__visitar_auxiliar(nodo)
        
        elif nodo.tipo is TipoNodo.VALOR_VERDAD:
            return self.__visitar_valor_verdadero(nodo)
        
        else:
            raise Exception('Tipo de nodo no soportado')

    def __visitar_programa(self, nodo_actual):
        return '\n'.join(self.visitar(hijo) for hijo in nodo_actual.hijos)

    def __visitar_asignacion(self, nodo_actual):
        izq = self.visitar(nodo_actual.hijos[0])
        der = self.visitar(nodo_actual.hijos[1])
        return f"{izq} = {der}"

    def __visitar_bifurcacion(self, nodo_actual):
        # Soporta IF, ELSE, ELIF y BIFURCACION
        if nodo_actual.tipo is TipoNodo.IF or nodo_actual.tipo is TipoNodo.BIFURCACION:
            condicion = self.visitar(nodo_actual.hijos[0])
            cuerpo = self.visitar(nodo_actual.hijos[1])
            return f"if {condicion}:\n{self.__tabular(cuerpo)}"
        
        elif nodo_actual.tipo is TipoNodo.ELIF:
            condicion = self.visitar(nodo_actual.hijos[0])
            cuerpo = self.visitar(nodo_actual.hijos[1])
            return f"elif {condicion}:\n{self.__tabular(cuerpo)}"
        
        elif nodo_actual.tipo is TipoNodo.ELSE:
            cuerpo = self.visitar(nodo_actual.hijos[0])
            return f"else:\n{self.__tabular(cuerpo)}"
        
        else:
            return ''

    def __visitar_bloque_instrucciones(self, nodo_actual):
        self.tabuladores += 4
        instrucciones = [self.__tabular(self.visitar(hijo)) for hijo in nodo_actual.hijos]
        self.tabuladores -= 4
        
        return '\n'.join(instrucciones)

    def __visitar_comparacion(self, nodo_actual):
        izq = self.visitar(nodo_actual.hijos[0])
        comp = self.visitar(nodo_actual.hijos[1])
        der = self.visitar(nodo_actual.hijos[2])
        
        return f"{izq} {comp} {der}"

    def __visitar_comparador(self, nodo_actual):
        comparadores = {
            'mismo_sabor_que': '==',
            'mas_sazonado_que': '>',
            'menos_cocido_que': '<',
            'tan_horneado_como': '>=',
            'tan_dulce_como': '<=',
        }
        
        return comparadores.get(nodo_actual.valor, nodo_actual.valor)

    def __visitar_condicion(self, nodo_actual):
        
        return ' '.join(self.visitar(hijo) for hijo in nodo_actual.hijos)

    def __visitar_funcion(self, nodo_actual):
        nombre = nodo_actual.valor
        parametros = self.visitar(nodo_actual.hijos[0]) if nodo_actual.hijos else ''
        cuerpo = self.visitar(nodo_actual.hijos[1]) if len(nodo_actual.hijos) > 1 else ''
        
        return f"\ndef {nombre}({parametros}):\n{cuerpo}"

    def __visitar_entero(self, nodo_actual):
        
        return str(nodo_actual.valor)

    def __visitar_error(self, nodo_actual):
        valor = self.visitar(nodo_actual.hijos[0]) if nodo_actual.hijos else ''
        
        return f"print({valor}, file=sys.stderr)"

    def __visitar_expresion_matematica(self, nodo_actual):
        
        return ' '.join(self.visitar(hijo) for hijo in nodo_actual.hijos)

    def __visitar_matematica(self, nodo_actual):
        
        return ' '.join(self.visitar(hijo) for hijo in nodo_actual.hijos)

    def __visitar_flotante(self, nodo_actual):
        
        return str(nodo_actual.valor)

    def __visitar_identificador(self, nodo_actual):
        
        return str(nodo_actual.valor)

    def __visitar_instruccion(self, nodo_actual):
        
        return self.visitar(nodo_actual.hijos[0]) if nodo_actual.hijos else ''

    def __visitar_invocacion(self, nodo_actual):
        nombre = self.visitar(nodo_actual.hijos[0])
        parametros = self.visitar(nodo_actual.hijos[1]) if len(nodo_actual.hijos) > 1 else ''
        
        return f"{nombre}({parametros})"

    def __visitar_operador(self, nodo_actual):
        operadores = {
            'echele': '+',
            'quitele': '-',
            'chuncherequee': '*',
            'desmadeje': '/',
        }
        
        return operadores.get(nodo_actual.valor, nodo_actual.valor)

    def __visitar_palabra_clave(self, nodo_actual):
        
        return str(nodo_actual.valor)

    def _visitar_parametros(self, nodo_actual):
        
        return ', '.join(self.visitar(hijo) for hijo in nodo_actual.hijos)

    def _visitar_parametros_funcion(self, nodo_actual):
        
        return ', '.join(self.visitar(hijo) for hijo in nodo_actual.hijos)

    def _visitar_parametros_invocacion(self, nodo_actual):
        
        return ', '.join(self.visitar(hijo) for hijo in nodo_actual.hijos)

    def __visitar_michelin(self, nodo_actual):
        cuerpo = self.visitar(nodo_actual.hijos[0]) if nodo_actual.hijos else ''
        
        return f"\ndef principal():\n{cuerpo}\n\nif __name__ == '__main__':\n    principal()"

    def __visitar_print(self, nodo_actual):
        valor = self.visitar(nodo_actual.hijos[0]) if nodo_actual.hijos else ''
        
        return f"print({valor})"

    def __visitar_repeticion(self, nodo_actual):
        condicion = self.visitar(nodo_actual.hijos[0])
        cuerpo = self.visitar(nodo_actual.hijos[1]) if len(nodo_actual.hijos) > 1 else ''
        
        return f"while {condicion}:\n{self.__tabular(cuerpo)}"

    def __visitar_retorno(self, nodo_actual):
        valor = self.visitar(nodo_actual.hijos[0]) if nodo_actual.hijos else ''
        
        return f"return {valor}"

    def __visitar_texto(self, nodo_actual):
        
        return f'"{nodo_actual.valor}"'

    def __visitar_auxiliar(self, nodo_actual):
        
        return self.visitar(nodo_actual.hijos[0]) if nodo_actual.hijos else ''

    def __visitar_valor_verdadero(self, nodo_actual):
        
        return str(nodo_actual.valor)

    def __tabular(self, texto):
        tab = " " * self.tabuladores
        
        return '\n'.join(tab + linea if linea.strip() else '' for linea in texto.split('\n'))