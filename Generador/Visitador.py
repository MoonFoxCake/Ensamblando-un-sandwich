from DocumentosUtiles.Arbol import Nodo, TipoNodo

class VisitadorPython:
    tabuladores = 0

    def visitar(self, nodo: Nodo):
        return self.__visitar(nodo)

    def __visitar(self, nodo: Nodo):
        if nodo is None:
            return ''
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
        elif nodo.tipo in (TipoNodo.ELIF, TipoNodo.ELSE, TipoNodo.IF):
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
            return ''

    def __visitar_programa(self, nodo_actual):
        return '\n'.join(self.visitar(hijo) for hijo in nodo_actual.hijos)

    def __visitar_asignacion(self, nodo_actual):
        # hijos[0]: PALABRA_CLAVE ('incorporar'), hijos[1]: IDENTIFICADOR, hijos[2]: valor
        identificador = self.visitar(nodo_actual.hijos[1])
        valor = self.visitar(nodo_actual.hijos[2])
        return f"{identificador} = {valor}"

    def __visitar_bifurcacion(self, nodo_actual):
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

    def __visitar_condicion(self, nodo_actual):
        # hijos[0]: VARIABLE_MATEMATICA, hijos[1]: COMPARADOR, hijos[2]: VARIABLE_MATEMATICA
        if len(nodo_actual.hijos) == 3:
            izq = self.visitar(nodo_actual.hijos[0])
            comp = self.visitar(nodo_actual.hijos[1])
            der = self.visitar(nodo_actual.hijos[2])
            return f"{izq} {comp} {der}"
        else:
            return ' '.join(self.visitar(hijo) for hijo in nodo_actual.hijos)

    def __visitar_comparador(self, nodo_actual):
        comparadores = {
            'mismo sabor que': '==',
            'mas sazonado que': '>',
            'menos cocido que': '<',
            'tan horneado como': '>=',
            'tan dulce como': '<=',
            'mismo_sabor_que': '==',
            'mas_sazonado_que': '>',
            'menos_cocido_que': '<',
            'tan_horneado_como': '>=',
            'tan_dulce_como': '<=',
        }
        return comparadores.get(str(nodo_actual.valor), str(nodo_actual.valor))

    def __visitar_funcion(self, nodo_actual):
        # hijos[0]: PALABRA_CLAVE ('michelin'), hijos[1]: IDENTIFICADOR, hijos[2]: PARA_FUNCION, hijos[3]: BLOQUE_INSTRUCCIONES
        nombre = self.visitar(nodo_actual.hijos[1]) if len(nodo_actual.hijos) > 1 else "funcion_sin_nombre"
        parametros = self.visitar(nodo_actual.hijos[2]) if len(nodo_actual.hijos) > 2 else ""
        cuerpo = self.visitar(nodo_actual.hijos[3]) if len(nodo_actual.hijos) > 3 else "    pass"
        return f"\ndef {nombre}({parametros}):\n{self.__tabular(cuerpo)}"

    def __visitar_entero(self, nodo_actual):
        return str(nodo_actual.valor)

    def __visitar_error(self, nodo_actual):
        valor = self.visitar(nodo_actual.hijos[0]) if nodo_actual.hijos else ''
        return f"raise Exception({valor})"

    def __visitar_expresion_matematica(self, nodo_actual):
        # hijos[0]: PALABRA_CLAVE ('ajustar'), hijos[1]: IDENTIFICADOR, hijos[2]: VARIABLE_MATEMATICA, hijos[3]: OPERADOR, hijos[4]: VARIABLE_MATEMATICA
        if len(nodo_actual.hijos) == 5:
            identificador = self.visitar(nodo_actual.hijos[1])
            izq = self.visitar(nodo_actual.hijos[2])
            op = self.visitar(nodo_actual.hijos[3])
            der = self.visitar(nodo_actual.hijos[4])
            return f"{identificador} = {izq} {op} {der}"
        else:
            return ' '.join(self.visitar(hijo) for hijo in nodo_actual.hijos)

    def __visitar_matematica(self, nodo_actual):
        # Generalmente solo tiene un hijo (IDENTIFICADOR, ENTERO, FLOTANTE, etc.)
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
            'batir': '+',
            'amasar': '*',
            'colar': '-',
            'partir': '/',
            'sobras': '%',
        }
        return operadores.get(str(nodo_actual.valor), str(nodo_actual.valor))

    def __visitar_palabra_clave(self, nodo_actual):
        traducciones = {
            'michelin': '',
            'integrar': '',
            'incorporar': '',
            'ajustar': '',
            'servir': 'print',
            'quemo': 'raise Exception',
            'pelar': 'pelar',
            'marinar': 'marinar',
            'True': 'True',
            'False': 'False',
            'batir': '+',
            'amasar': '*',
            'colar': '-',
            'partir': '/',
            'sobras': '%',
            'mismo sabor que': '==',
            'mas sazonado que': '>',
            'menos cocido que': '<',
            'tan horneado como': '>=',
            'tan dulce como': '<=',
        }
        return traducciones.get(str(nodo_actual.valor), str(nodo_actual.valor))

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
        condicion = self.visitar(nodo_actual.hijos[1]) if len(nodo_actual.hijos) > 1 else ''
        cuerpo = self.visitar(nodo_actual.hijos[2]) if len(nodo_actual.hijos) > 2 else ''
        return f"while {condicion}:\n{self.__tabular(cuerpo)}"

    def __visitar_retorno(self, nodo_actual):
        # hijos[0]: PALABRA_CLAVE ('dingding'), hijos[1]: valor de retorno (opcional)
        if len(nodo_actual.hijos) > 1:
            valor = self.visitar(nodo_actual.hijos[1])
        elif len(nodo_actual.hijos) == 1:
            valor = self.visitar(nodo_actual.hijos[0])
            if valor == 'dingding':
                valor = 'None'
        else:
            valor = 'None'
        return f"return {valor}"

    def __visitar_texto(self, nodo_actual):
        valor = str(nodo_actual.valor)
        if valor.startswith('"') and valor.endswith('"'):
            valor = valor[1:-1]
        return f'"{valor}"'

    def __visitar_auxiliar(self, nodo_actual):
        return self.visitar(nodo_actual.hijos[0]) if nodo_actual.hijos else ''

    def __visitar_valor_verdadero(self, nodo_actual):
        return str(nodo_actual.valor)

    def __tabular(self, texto):
        tab = " " * self.tabuladores
        return '\n'.join(tab + linea if linea.strip() else '' for linea in texto.split('\n'))