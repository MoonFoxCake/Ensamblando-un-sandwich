from DocumentosUtiles.Arbol import ArbolSintaxisAbstracta, Nodo, TipoNodo
from DocumentosUtiles.TiposDato import TiposDato

class TablaSimbolos:
    """Almacena informacion para el arbol con info del tipo y alcance.
    
    Trabaja con niveles de profundidad para manejar scopes anidados.
    """
    
    def __init__(self):
        self.simbolos = []
        self.profundidad = 0
        self.cambios_realizados = False

    def abrir_bloque(self):
        """Aumenta la profundidad del bloque."""
        self.profundidad += 1
        self.cambios_realizados = True
        print(f"[TABLA] Abriendo bloque -> Profundidad: {self.profundidad}")
    
    def cerrar_bloque(self):
        """Termina un bloque y quita todo lo que este dentro de este, reduce la profundidad."""
        print(f"[TABLA] Cerrando bloque <- Profundidad: {self.profundidad}")
        
        # Crear lista de simbolos a remover
        simbolos_a_remover = [
            registro for registro in self.simbolos 
            if registro['Profundidad'] == self.profundidad
        ]
        
        # Remover los simbolos
        for registro in simbolos_a_remover:
            self.simbolos.remove(registro)
            
        self.profundidad -= 1
        self.cambios_realizados = True
    
    def nuevo_registro(self, nodo, tipo, nombre_registro=''):
        """Añade un registro nuevo."""
        diccionario = {
            'Nombre': nodo.valor,
            'Profundidad': self.profundidad,
            'Referencia': nodo,
            'Tipo': tipo,
            'NombreRegistro': nombre_registro
        }
        
        self.simbolos.append(diccionario)
        self.cambios_realizados = True
        print(f"[TABLA] Registrado: {nodo.valor} ({tipo.name})")
        
    def verificar_existencia(self, nombre):
        """Verifica si existe un registro con el nombre dado."""
        for registro in self.simbolos:
            if (registro['Nombre'] == nombre and 
                registro['Profundidad'] <= self.profundidad):
                return registro
        
        raise Exception(f"ERROR: Variable '{nombre}' no esta definida")

    def imprimir_estado(self):
        """Imprime el estado actual de la tabla de simbolos."""
        if not self.cambios_realizados:
            return
            
        print(f"\n[TABLA] Estado actual - Profundidad: {self.profundidad}")
        
        if not self.simbolos:
            print("[TABLA] Tabla vacia")
        else:
            for registro in self.simbolos:
                tipo_nombre = registro['Tipo'].name if hasattr(registro['Tipo'], 'name') else str(registro['Tipo'])
                print(f"  - {registro['Nombre']} : {tipo_nombre} (Prof: {registro['Profundidad']})")
        
        self.cambios_realizados = False

    def obtener_simbolos_usados(self):
        """Retorna solo los simbolos que no son del ambiente estandar."""
        simbolos_usuario = [
            s for s in self.simbolos 
            if s['Nombre'] not in ['pelar', 'marinar', 'quemo']
        ]
        return simbolos_usuario

    def __str__(self):
        resultado = "Tabla de Simbolos:\n"
        resultado += f"Profundidad: {self.profundidad}\n"
        for registro in self.simbolos:
            resultado += f"{registro}\n"
        return resultado

class Visitante:
    """Visitante para recorrer el arbol de sintaxis abstracta y realizar verificaciones semanticas."""
    
    def __init__(self, nueva_tabla_simbolos):
        self.tabla_simbolos = nueva_tabla_simbolos
        self.errores = []
        self.profundidad_impresion = 0
    
    def agregar_error(self, mensaje, nodo=None):
        """Agrega un error a la lista de errores."""
        if nodo:
            error = f"ERROR: {mensaje} (en {nodo.tipo.name})"
        else:
            error = f"ERROR: {mensaje}"
        self.errores.append(error)
    
    def verificar_compatibilidad_tipos(self, tipo1, tipo2, operacion="operacion"):
        """Verifica si dos tipos son compatibles para una operacion."""
        # Casos especiales donde cualquier tipo es compatible
        if tipo1 == TiposDato.CUALQUIERA or tipo2 == TiposDato.CUALQUIERA:
            return True
            
        # En operaciones matemáticas, NINGUNO no es válido
        if tipo1 == TiposDato.NINGUNO or tipo2 == TiposDato.NINGUNO:
            return False
            
        # Numeros son compatibles entre si
        tipos_numericos = {TiposDato.NUMERO, TiposDato.ENTERO, TiposDato.FLOTANTE}
        if tipo1 in tipos_numericos and tipo2 in tipos_numericos:
            return True
            
        # Mismo tipo
        if tipo1 == tipo2:
            return True
            
        return False
    
    def obtener_tipo_resultante(self, tipo1, tipo2):
        """Determina el tipo resultante de una operación entre dos tipos."""
        # Si uno es CUALQUIERA, retorna el otro
        if tipo1 == TiposDato.CUALQUIERA:
            return tipo2
        if tipo2 == TiposDato.CUALQUIERA:
            return tipo1
            
        # Si ambos son el mismo tipo, retorna ese tipo
        if tipo1 == tipo2:
            return tipo1
            
        # Para operaciones numéricas
        tipos_numericos = {TiposDato.NUMERO, TiposDato.ENTERO, TiposDato.FLOTANTE}
        if tipo1 in tipos_numericos and tipo2 in tipos_numericos:
            # Si uno es FLOTANTE, el resultado es FLOTANTE
            if tipo1 == TiposDato.FLOTANTE or tipo2 == TiposDato.FLOTANTE:
                return TiposDato.FLOTANTE
            # Si ambos son ENTERO, el resultado puede ser NUMERO (más general)
            elif tipo1 == TiposDato.ENTERO and tipo2 == TiposDato.ENTERO:
                return TiposDato.ENTERO
            # Cualquier otra combinación numérica da NUMERO
            else:
                return TiposDato.NUMERO
                
        # Si no son compatibles, retorna CUALQUIERA
        return TiposDato.CUALQUIERA
    
    def visitar(self, nodo):
        """Metodo publico que llama al metodo privado de visita."""
        resultado = self.__visitar(nodo)
        self.tabla_simbolos.imprimir_estado()
        return resultado
    
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
            

    def __visitar_asignacion(self, nodo_actual):
        """Procesa nodos de asignacion de variables."""
        # Inspirado en el verificador de ciruelas
        # Buscar el identificador y el valor asignado
        identificador = None
        valor_asignado = None
        es_nueva_declaracion = False
        
        for hijo in nodo_actual.hijos:
            if hijo is not None:
                if hijo.tipo == TipoNodo.IDENTIFICADOR and identificador is None:
                    # Tomar el primer identificador encontrado
                    identificador = hijo
                elif hijo.tipo not in [TipoNodo.PALABRA_CLAVE]:
                    valor_asignado = hijo
        
        # Verificar si es una declaración nueva ('incorporar') o una reasignación
        for hijo in nodo_actual.hijos:
            if hijo.tipo == TipoNodo.PALABRA_CLAVE and hijo.valor == 'incorporar':
                es_nueva_declaracion = True
                break
        
        # Registrar la variable en la tabla de símbolos PRIMERO (como en ciruelas)
        # Solo registrar si es una nueva variable (con 'incorporar')
        if identificador is not None and es_nueva_declaracion:
            # Solo registrar nuevas variables
            self.tabla_simbolos.nuevo_registro(identificador, TiposDato.CUALQUIERA)
            print(f"[TABLA] Registrado: {identificador.valor} (CUALQUIERA)")
            self.tabla_simbolos.imprimir_estado()
        
        # Visitar todos los hijos
        for nodo in nodo_actual.hijos:
            if nodo is not None:
                # Verificar identificadores antes de visitarlos
                if nodo.tipo == TipoNodo.IDENTIFICADOR:
                    # Si es el identificador de la declaración nueva, no verificar existencia
                    if es_nueva_declaracion and nodo == identificador:
                        # Este es el identificador que se está declarando, no verificar
                        pass
                    else:
                        # Este es un identificador usado en la expresión, verificar existencia
                        try:
                            registro = self.tabla_simbolos.verificar_existencia(nodo.valor)
                        except:
                            self.agregar_error(f"Variable '{nodo.valor}' no está definida", nodo)
                            nodo.atributos['tipo'] = TiposDato.ERROR
                            continue
                nodo.visitar(self)
        
        # Asignar el tipo del valor al identificador (como en ciruelas)
        if identificador is not None and valor_asignado is not None:
            if 'tipo' in valor_asignado.atributos:
                tipo_valor = valor_asignado.atributos['tipo']
                
                # Actualizar el tipo en la tabla de símbolos
                try:
                    registro = self.tabla_simbolos.verificar_existencia(identificador.valor)
                    registro['Tipo'] = tipo_valor
                    if 'Referencia' in registro:
                        registro['Referencia'].atributos['tipo'] = tipo_valor
                except:
                    if not ('tipo' in identificador.atributos and identificador.atributos['tipo'] == TiposDato.ERROR):
                        self.agregar_error(f"Variable '{identificador.valor}' no está definida", identificador)
                        identificador.atributos['tipo'] = TiposDato.ERROR
                        nodo_actual.atributos['tipo'] = TiposDato.ERROR
                        return
                
                # Asignar el tipo al identificador y a la asignación
                identificador.atributos['tipo'] = tipo_valor
                nodo_actual.atributos['tipo'] = tipo_valor
            else:
                identificador.atributos['tipo'] = TiposDato.CUALQUIERA
                nodo_actual.atributos['tipo'] = TiposDato.CUALQUIERA
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

    def __visitar_bifurcacion(self, nodo_actual):
        '''Bifurcacion es un if o un else'''
        
        if nodo_actual.tipo == TipoNodo.BIFURCACION:
            for nodo in nodo_actual.hijos:
                nodo.visitar(self)
            nodo_actual.atributos['tipo'] = TiposDato.CUALQUIERA
            
        elif nodo_actual.tipo == TipoNodo.IF:
            self.tabla_simbolos.abrir_bloque()
            for nodo in nodo_actual.hijos:
                nodo.visitar(self)
            
            # Los nodos IF son estructurales y no deberían tener tipo
            nodo_actual.atributos['tipo'] = TiposDato.NINGUNO
                
            self.tabla_simbolos.cerrar_bloque()
            
        elif nodo_actual.tipo == TipoNodo.ELIF:
            self.tabla_simbolos.abrir_bloque()
            for nodo in nodo_actual.hijos:
                nodo.visitar(self)
                
            # Los nodos ELIF son estructurales y no deberían tener tipo
            nodo_actual.atributos['tipo'] = TiposDato.NINGUNO
                
            self.tabla_simbolos.cerrar_bloque()
            
        elif nodo_actual.tipo == TipoNodo.ELSE:
            self.tabla_simbolos.abrir_bloque()
            for nodo in nodo_actual.hijos:
                nodo.visitar(self)
                
            # Los nodos ELSE son estructurales y no deberían tener tipo
            nodo_actual.atributos['tipo'] = TiposDato.NINGUNO
                
            self.tabla_simbolos.cerrar_bloque()
        


    def __visitar_bloque_instrucciones(self,  nodo_actual):
        """
        Visita un bloque de instrucciones.
        Estructura:

            BloqueInstrucciones ::= { Instruccion+ }

        """
        for nodo in nodo_actual.hijos:
            if nodo is not None:
                nodo.visitar(self)

        # Los bloques de instrucciones son estructurales y no deberían tener tipo
        # Solo asignar tipo si hay una instrucción de retorno
        nodo_actual.atributos['tipo'] = TiposDato.NINGUNO
        
        for nodo in nodo_actual.hijos:
            if (nodo is not None and 'tipo' in nodo.atributos and 
                hasattr(nodo, 'hijos') and nodo.hijos and 
                nodo.hijos[0] is not None and 
                nodo.hijos[0].tipo == TipoNodo.RETORNO):
                # Solo heredar tipo de instrucciones de retorno
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
        
        # Verificar comparación entre 3 valores: valor comparador valor
        if len(nodo_actual.hijos) >= 3:
            valor_izquierdo = nodo_actual.hijos[0]
            comparador = nodo_actual.hijos[1]
            valor_derecho = nodo_actual.hijos[2]

            # Obtener tipos de los valores
            tipo_izq = valor_izquierdo.atributos.get('tipo', TiposDato.CUALQUIERA)
            tipo_der = valor_derecho.atributos.get('tipo', TiposDato.CUALQUIERA)
            
            # Verificar si el comparador requiere tipos específicos
            if 'requiere_tipo' in comparador.atributos:
                tipos_requeridos = comparador.atributos['requiere_tipo']
                
                # Si el comparador requiere tipos numéricos
                if TiposDato.NUMERO in tipos_requeridos and TiposDato.CUALQUIERA not in tipos_requeridos:
                    tipos_numericos = {TiposDato.NUMERO, TiposDato.ENTERO, TiposDato.FLOTANTE}
                    
                    if tipo_izq not in tipos_numericos and tipo_izq != TiposDato.CUALQUIERA:
                        self.agregar_error(f"El comparador '{comparador.valor}' requiere valores numéricos, pero el valor izquierdo es {tipo_izq.name if hasattr(tipo_izq, 'name') else tipo_izq}", nodo_actual)
                    
                    if tipo_der not in tipos_numericos and tipo_der != TiposDato.CUALQUIERA:
                        self.agregar_error(f"El comparador '{comparador.valor}' requiere valores numéricos, pero el valor derecho es {tipo_der.name if hasattr(tipo_der, 'name') else tipo_der}", nodo_actual)

            # El resultado de una comparación siempre es un valor de verdad
            nodo_actual.atributos['tipo'] = TiposDato.VALOR_VERDAD
        else:
            # Comparación simple - debe ser booleano
            nodo_actual.atributos['tipo'] = TiposDato.VALOR_VERDAD

    def __visitar_comparador(self,  nodo_actual):
        """
        Comparador ::= mismo_sabor_que|mas_sazonado_que|menos_cocido_que|tan_horneado_como|tan_dulce_como
        """
        '''Comparador que determina qué tipos de datos puede comparar'''

        # Los comparadores no tienen tipo propio, son operadores que requieren ciertos tipos
        # Definir qué tipos acepta cada comparador
        if nodo_actual.valor in ['mas_sazonado_que', 'menos_cocido_que', 'tan_horneado_como']:
            # Estos comparadores requieren tipos numéricos
            nodo_actual.atributos['tipo'] = TiposDato.NINGUNO  # Los comparadores no tienen tipo
            nodo_actual.atributos['requiere_tipo'] = [TiposDato.NUMERO, TiposDato.ENTERO, TiposDato.FLOTANTE]
        elif nodo_actual.valor in ['mismo_sabor_que', 'tan_dulce_como']:
            # Estos pueden comparar cualquier tipo
            nodo_actual.atributos['tipo'] = TiposDato.NINGUNO  # Los comparadores no tienen tipo
            nodo_actual.atributos['requiere_tipo'] = [TiposDato.CUALQUIERA]
        else:
            nodo_actual.atributos['tipo'] = TiposDato.NINGUNO  # Los comparadores no tienen tipo
            nodo_actual.atributos['requiere_tipo'] = [TiposDato.CUALQUIERA]

    def __visitar_condicion(self,  nodo_actual):
        '''Condición que puede contener comparaciones'''
        
        # Visitar todos los hijos
        for nodo in nodo_actual.hijos:
            if nodo is not None:
                if nodo.tipo == TipoNodo.IDENTIFICADOR:
                    try:
                        registro = self.tabla_simbolos.verificar_existencia(nodo.valor)
                        # Actualizar el tipo del identificador
                        if 'Tipo' in registro and registro['Tipo'] != TiposDato.CUALQUIERA:
                            nodo.atributos['tipo'] = registro['Tipo']
                    except:
                        self.agregar_error(f"Variable '{nodo.valor}' no definida en condición", nodo)
                        nodo.atributos['tipo'] = TiposDato.ERROR
                
                nodo.visitar(self)
        
        # Verificar si es una comparación (valor1 comparador valor2)
        if len(nodo_actual.hijos) >= 3:
            valor_izquierdo = nodo_actual.hijos[0]
            comparador = nodo_actual.hijos[1]
            valor_derecho = nodo_actual.hijos[2]
            
            # Verificar que el nodo central es un comparador
            if comparador.tipo == TipoNodo.COMPARADOR:
                tipo_izq = valor_izquierdo.atributos.get('tipo', TiposDato.CUALQUIERA)
                tipo_der = valor_derecho.atributos.get('tipo', TiposDato.CUALQUIERA)
                
                # Si el comparador requiere tipos específicos, verificar
                if 'requiere_tipo' in comparador.atributos:
                    tipos_requeridos = comparador.atributos['requiere_tipo']
                    
                    # Si el comparador requiere tipos numéricos
                    if (TiposDato.NUMERO in tipos_requeridos and 
                        TiposDato.CUALQUIERA not in tipos_requeridos):
                        
                        tipos_numericos = {TiposDato.NUMERO, TiposDato.ENTERO, TiposDato.FLOTANTE}
                        
                        if (tipo_izq not in tipos_numericos and 
                            tipo_izq not in [TiposDato.CUALQUIERA, TiposDato.ERROR]):
                            self.agregar_error(f"El comparador '{comparador.valor}' requiere valores numéricos, pero el valor izquierdo es {tipo_izq.name if hasattr(tipo_izq, 'name') else tipo_izq}", nodo_actual)
                        
                        if (tipo_der not in tipos_numericos and 
                            tipo_der not in [TiposDato.CUALQUIERA, TiposDato.ERROR]):
                            self.agregar_error(f"El comparador '{comparador.valor}' requiere valores numéricos, pero el valor derecho es {tipo_der.name if hasattr(tipo_der, 'name') else tipo_der}", nodo_actual)

        # Las condiciones siempre resultan en un valor de verdad
        nodo_actual.atributos['tipo'] = TiposDato.VALOR_VERDAD

    def __visitar_entero(self,  nodo_actual):
        """
        Verifica si el tipo del componente lexico actuales de tipo ENTERO

        Entero ::= -?[0-9]+
        """
        nodo_actual.atributos['tipo'] = TiposDato.ENTERO  # Mantener ENTERO como tipo específico
    
    def __visitar_error(self,  nodo_actual):
        '''Error, no deberia de llegar aca, pero para poder poner el error por si no se agarra con el analizador, o bueno si se pone quemar'''
        for nodo in nodo_actual.hijos:
            if nodo.tipo == TipoNodo.IDENTIFICADOR:
                registro = self.tabla_simbolos.verificar_existencia(nodo.valor)
            nodo.visitar(self)

    def __visitar_expresion_matematica(self, nodo_actual):
        '''Expresion matematica con verificacion de tipos'''
        
        # Primero visitar todos los hijos
        for nodo in nodo_actual.hijos:
            if nodo is not None:
                # Verificar identificadores antes de visitarlos
                if nodo.tipo == TipoNodo.IDENTIFICADOR:
                    try:
                        registro = self.tabla_simbolos.verificar_existencia(nodo.valor)
                        # Actualizar el tipo del identificador con el de la tabla
                        if 'Tipo' in registro and registro['Tipo'] != TiposDato.CUALQUIERA:
                            nodo.atributos['tipo'] = registro['Tipo']
                    except Exception as e:
                        self.agregar_error(f"Variable '{nodo.valor}' no definida en expresion matematica", nodo)
                        nodo.atributos['tipo'] = TiposDato.ERROR
                
                nodo.visitar(self)
        
        # Verificar si es una expresión binaria (operando1 operador operando2)
        if len(nodo_actual.hijos) >= 3:
            # Buscar los operandos y el operador
            operandos = []
            operador = None
            
            for hijo in nodo_actual.hijos:
                if hijo is not None:
                    if hijo.tipo == TipoNodo.OPERADOR:
                        operador = hijo
                    elif hijo.tipo not in [TipoNodo.PALABRA_CLAVE]:  # Ignorar palabras clave como 'ajustar'
                        operandos.append(hijo)
            
            if len(operandos) >= 2 and operador is not None:
                tipo1 = operandos[0].atributos.get('tipo', TiposDato.CUALQUIERA)
                tipo2 = operandos[1].atributos.get('tipo', TiposDato.CUALQUIERA)
                
                # Verificar si alguno es ERROR
                if tipo1 == TiposDato.ERROR or tipo2 == TiposDato.ERROR:
                    nodo_actual.atributos['tipo'] = TiposDato.ERROR
                    return
                
                # Verificar compatibilidad para operaciones matemáticas
                if tipo1 == TiposDato.TEXTO or tipo2 == TiposDato.TEXTO:
                    # No se pueden hacer operaciones matemáticas con texto
                    if tipo1 == TiposDato.TEXTO and tipo2 in [TiposDato.NUMERO, TiposDato.ENTERO, TiposDato.FLOTANTE]:
                        self.agregar_error("No se puede operar texto con numero", nodo_actual)
                        nodo_actual.atributos['tipo'] = TiposDato.ERROR
                        return
                    elif tipo2 == TiposDato.TEXTO and tipo1 in [TiposDato.NUMERO, TiposDato.ENTERO, TiposDato.FLOTANTE]:
                        self.agregar_error("No se puede operar numero con texto", nodo_actual)
                        nodo_actual.atributos['tipo'] = TiposDato.ERROR
                        return
                
                # Determinar el tipo resultante
                if self.verificar_compatibilidad_tipos(tipo1, tipo2, "operacion matematica"):
                    nodo_actual.atributos['tipo'] = self.obtener_tipo_resultante(tipo1, tipo2)
                else:
                    self.agregar_error(f"Tipos incompatibles en operacion: {tipo1.name if hasattr(tipo1, 'name') else tipo1} y {tipo2.name if hasattr(tipo2, 'name') else tipo2}", nodo_actual)
                    nodo_actual.atributos['tipo'] = TiposDato.ERROR
            else:
                # Expresión con estructura diferente
                nodo_actual.atributos['tipo'] = TiposDato.CUALQUIERA
        
        elif nodo_actual.hijos:
            # Expresión simple - hereda el tipo del último hijo no-palabra-clave
            tipo_resultado = TiposDato.CUALQUIERA
            for hijo in reversed(nodo_actual.hijos):
                if hijo is not None and hijo.tipo != TipoNodo.PALABRA_CLAVE and 'tipo' in hijo.atributos:
                    tipo_resultado = hijo.atributos['tipo']
                    break
            nodo_actual.atributos['tipo'] = tipo_resultado
        else:
            nodo_actual.atributos['tipo'] = TiposDato.CUALQUIERA
         


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

    
    def __visitar_funcion(self, nodo_actual):
        '''Funcion o definicion de funcion'''
        
        # Buscar el identificador de la funcion
        nombre_funcion = None
        for hijo in nodo_actual.hijos:
            if hijo is not None and hijo.tipo == TipoNodo.IDENTIFICADOR:
                nombre_funcion = hijo
                break
        
        # Registrar la funcion primero (antes de abrir el bloque)
        if nombre_funcion is not None:
            # Asignar tipo FUNCION al identificador de la función
            nombre_funcion.atributos['tipo'] = TiposDato.FUNCION
            self.tabla_simbolos.nuevo_registro(nombre_funcion, TiposDato.FUNCION, nombre_funcion.valor)
        
        # Abrir bloque para la funcion
        self.tabla_simbolos.abrir_bloque()
        
        # Visitar todos los hijos
        for nodo in nodo_actual.hijos:
            if nodo is not None:
                nodo.visitar(self)
        
        # Cerrar bloque de la funcion
        self.tabla_simbolos.cerrar_bloque()

        # Determinar tipo de retorno de la funcion
        if len(nodo_actual.hijos) > 2 and nodo_actual.hijos[2] is not None and 'tipo' in nodo_actual.hijos[2].atributos:
            nodo_actual.atributos['tipo'] = nodo_actual.hijos[2].atributos['tipo']
        else:
            nodo_actual.atributos['tipo'] = TiposDato.NINGUNO

    def __visitar_flotante(self,  nodo_actual):
        """
        Verifica si el tipo del componente lexico actuales de tipo FLOTANTE

        Flotante ::= -?[0-9]+.[0-9]+
        """
        nodo_actual.atributos['tipo'] = TiposDato.FLOTANTE  # Mantener FLOTANTE como tipo específico

    def __visitar_identificador(self, nodo_actual):
        """Procesa identificadores y verifica su existencia en la tabla de simbolos."""
        try:
            registro = self.tabla_simbolos.verificar_existencia(nodo_actual.valor)
            
            # Priorizar el tipo explícito de la tabla de símbolos
            if 'Tipo' in registro and registro['Tipo'] != TiposDato.CUALQUIERA:
                nodo_actual.atributos['tipo'] = registro['Tipo']
            elif 'Referencia' in registro and 'tipo' in registro['Referencia'].atributos:
                tipo_ref = registro['Referencia'].atributos['tipo']
                if tipo_ref != TiposDato.CUALQUIERA:
                    nodo_actual.atributos['tipo'] = tipo_ref
                else:
                    nodo_actual.atributos['tipo'] = TiposDato.CUALQUIERA
            else:
                nodo_actual.atributos['tipo'] = TiposDato.CUALQUIERA
                
        except Exception:
            # Error amigable para desarrollador
            self.agregar_error(f"Variable '{nodo_actual.valor}' no esta definida", nodo_actual)
            nodo_actual.atributos['tipo'] = TiposDato.ERROR

    def __visitar_invocacion(self,  nodo_actual):
        """
        Invocacion ::= Identificador ( ParametrosInvocacion )
        """
        '''Invocacion es una funcion que se invoca, o sea se llama'''

        # Verificar que hay hijos y el primer hijo es válido
        if not nodo_actual.hijos or not nodo_actual.hijos[0]:
            self.agregar_error("Invocación malformada: no hay identificador", nodo_actual)
            nodo_actual.atributos['tipo'] = TiposDato.ERROR
            # Aún así visitar los hijos restantes
            for nodo in nodo_actual.hijos[1:]:
                if nodo is not None:
                    nodo.visitar(self)
            return

        identificador_funcion = nodo_actual.hijos[0]
        
        # Verificar si es realmente una invocación de función o una asignación mal interpretada
        # Una invocación válida debe tener un identificador seguido de parámetros o parentesis
        # Si solo tiene identificadores consecutivos, probablemente es una asignación mal interpretada
        if len(nodo_actual.hijos) == 2 and all(h.tipo == TipoNodo.IDENTIFICADOR for h in nodo_actual.hijos):
            # Esto parece una asignación mal interpretada (ej: "a = b" sin palabra clave)
            # Reportar error de sintaxis
            var_destino = nodo_actual.hijos[0]
            var_origen = nodo_actual.hijos[1]
            
            self.agregar_error(f"Asignación mal formada: '{var_destino.valor} = {var_origen.valor}'. Falta palabra clave 'ajustar'", nodo_actual)
            
            # Tratar como asignación implícita
            # Visitar el identificador origen primero
            var_origen.visitar(self)
            
            # Verificar que la variable origen existe
            try:
                registro_origen = self.tabla_simbolos.verificar_existencia(var_origen.valor)
                tipo_origen = registro_origen.get('Tipo', TiposDato.CUALQUIERA)
                var_origen.atributos['tipo'] = tipo_origen
            except:
                self.agregar_error(f"Variable '{var_origen.valor}' no está definida", var_origen)
                var_origen.atributos['tipo'] = TiposDato.ERROR
                tipo_origen = TiposDato.ERROR
            
            # Verificar que la variable destino existe
            try:
                registro_destino = self.tabla_simbolos.verificar_existencia(var_destino.valor)
                # Actualizar el tipo de la variable destino
                if tipo_origen != TiposDato.ERROR:
                    registro_destino['Tipo'] = tipo_origen
                    if 'Referencia' in registro_destino:
                        registro_destino['Referencia'].atributos['tipo'] = tipo_origen
                    var_destino.atributos['tipo'] = tipo_origen
                    nodo_actual.atributos['tipo'] = tipo_origen
                else:
                    var_destino.atributos['tipo'] = TiposDato.ERROR
                    nodo_actual.atributos['tipo'] = TiposDato.ERROR
            except:
                self.agregar_error(f"Variable '{var_destino.valor}' no está definida", var_destino)
                var_destino.atributos['tipo'] = TiposDato.ERROR
                nodo_actual.atributos['tipo'] = TiposDato.ERROR
            
            return
        
        try:
            # Buscar la función en la tabla de símbolos
            busqueda = self.tabla_simbolos.verificar_existencia(identificador_funcion.valor)
            
            # Verificar que realmente es una función
            if busqueda['Tipo'] != TiposDato.FUNCION:
                self.agregar_error(f"'{identificador_funcion.valor}' no es una función", nodo_actual)
                # Asegurar que el identificador tenga tipo ERROR
                identificador_funcion.atributos['tipo'] = TiposDato.ERROR
                nodo_actual.atributos['tipo'] = TiposDato.ERROR
                
                # Aún así, visitar los parámetros para detectar otros errores
                for nodo in nodo_actual.hijos[1:]:
                    if nodo is not None:
                        nodo.visitar(self)
                return
            
            # Asignar tipo FUNCION al identificador de función
            identificador_funcion.atributos['tipo'] = TiposDato.FUNCION
            
            # Visitar todos los hijos (parámetros)
            for nodo in nodo_actual.hijos:
                if nodo is not None:
                    nodo.visitar(self)
            
            # Determinar el tipo de retorno de la función
            if 'Referencia' in busqueda and hasattr(busqueda['Referencia'], 'atributos'):
                if 'tipo' in busqueda['Referencia'].atributos:
                    nodo_actual.atributos['tipo'] = busqueda['Referencia'].atributos['tipo']
                else:
                    nodo_actual.atributos['tipo'] = TiposDato.NINGUNO
            else:
                nodo_actual.atributos['tipo'] = TiposDato.NINGUNO
                
        except Exception as e:
            # Si la función no existe
            self.agregar_error(f"Función '{identificador_funcion.valor}' no está definida", nodo_actual)
            
            # Asegurar que el identificador tenga tipo ERROR
            identificador_funcion.atributos['tipo'] = TiposDato.ERROR
            
            # Aún así, visitar los hijos para detectar otros errores
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
        
        # Las instrucciones son nodos estructurales y no deberían tener tipo
        # Solo asignar tipo si es una instrucción que retorna un valor (como retorno)
        if (nodo_actual.hijos and nodo_actual.hijos[0] is not None and 
            nodo_actual.hijos[0].tipo == TipoNodo.RETORNO and 
            'tipo' in nodo_actual.hijos[0].atributos):
            nodo_actual.atributos['tipo'] = nodo_actual.hijos[0].atributos['tipo']
        else:
            # Para otros tipos de instrucciones, no asignar tipo
            nodo_actual.atributos['tipo'] = TiposDato.NINGUNO

    ##def __visitar_literal(self,  nodo_actual):
    ##    '''Literal es un valor literal, o sea un numero, una cadena, un booleano, etc'''

    def __visitar_matematica(self,  nodo_actual):
        '''Variable matematica - representa un identificador en contexto matemático'''
        
        for nodo in nodo_actual.hijos:
            if nodo is not None:
                if nodo.tipo == TipoNodo.IDENTIFICADOR:
                    try:
                        registro = self.tabla_simbolos.verificar_existencia(nodo.valor)
                        # Actualizar el tipo del identificador con el de la tabla
                        if 'Tipo' in registro and registro['Tipo'] != TiposDato.CUALQUIERA:
                            nodo.atributos['tipo'] = registro['Tipo']
                        else:
                            nodo.atributos['tipo'] = TiposDato.CUALQUIERA
                    except:
                        self.agregar_error(f"Variable '{nodo.valor}' no definida", nodo)
                        nodo.atributos['tipo'] = TiposDato.ERROR
                
                nodo.visitar(self)
        
        # El tipo de VARIABLE_MATEMATICA es el mismo que su identificador hijo
        if nodo_actual.hijos and nodo_actual.hijos[0] is not None:
            primer_hijo = nodo_actual.hijos[0]
            if 'tipo' in primer_hijo.atributos:
                nodo_actual.atributos['tipo'] = primer_hijo.atributos['tipo']
            else:
                nodo_actual.atributos['tipo'] = TiposDato.CUALQUIERA
        else:
            nodo_actual.atributos['tipo'] = TiposDato.CUALQUIERA

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
            if nodo is not None:
                if nodo.tipo == TipoNodo.IDENTIFICADOR:
                    try:
                        registro = self.tabla_simbolos.verificar_existencia(nodo.valor)
                        # Actualizar el tipo del identificador
                        if 'Tipo' in registro and registro['Tipo'] != TiposDato.CUALQUIERA:
                            nodo.atributos['tipo'] = registro['Tipo']
                        else:
                            nodo.atributos['tipo'] = TiposDato.CUALQUIERA
                    except:
                        self.agregar_error(f"Variable '{nodo.valor}' no definida en parámetros de invocación", nodo)
                        nodo.atributos['tipo'] = TiposDato.ERROR
                else:
                    # Para otros tipos de nodos, asegurar que se visiten
                    nodo.visitar(self)
        
        # Los parámetros no tienen un tipo específico como conjunto
        nodo_actual.atributos['tipo'] = TiposDato.NINGUNO

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
            # Si no hay hijos, el retorno es NINGUNO
            nodo_actual.atributos['tipo'] = TiposDato.NINGUNO
            return
        
        # Visitar todos los hijos primero
        for nodo in nodo_actual.hijos:
            if nodo.tipo == TipoNodo.IDENTIFICADOR:
                try:
                    # Verificar que el identificador existe
                    registro = self.tabla_simbolos.verificar_existencia(nodo.valor)
                    # Obtener el tipo del registro
                    if 'Tipo' in registro and registro['Tipo'] != TiposDato.CUALQUIERA:
                        nodo.atributos['tipo'] = registro['Tipo']
                    elif 'Referencia' in registro and 'tipo' in registro['Referencia'].atributos:
                        nodo.atributos['tipo'] = registro['Referencia'].atributos['tipo']
                    else:
                        nodo.atributos['tipo'] = TiposDato.CUALQUIERA
                except:
                    self.agregar_error(f"Variable '{nodo.valor}' no definida en retorno", nodo)
                    nodo.atributos['tipo'] = TiposDato.ERROR
            else:
                nodo.visitar(self)
        
        # El tipo de retorno es el tipo del primer hijo
        if nodo_actual.hijos and nodo_actual.hijos[0] is not None:
            primer_hijo = nodo_actual.hijos[0]
            if 'tipo' in primer_hijo.atributos:
                nodo_actual.atributos['tipo'] = primer_hijo.atributos['tipo']
            else:
                nodo_actual.atributos['tipo'] = TiposDato.CUALQUIERA
        else:
            nodo_actual.atributos['tipo'] = TiposDato.NINGUNO

    def __visitar_texto(self,  nodo_actual):
        """
        Verifica si el tipo del componente lexico actuales de tipo TEXTO

        Texto ::= ~"[^"]*"~
        """

        nodo_actual.atributos['tipo'] = TiposDato.TEXTO
        #Di mae....el tipo es texto asi que lo ponemos como texto

    def __visitar_valor_verdadero(self,  nodo_actual):
    
        """
        CRUDO_VALOR_VERDAD ::= (True | False)
        """

        nodo_actual.atributos['tipo'] = TiposDato.VALOR_VERDAD

        #Se le pone el tipo de valor que es verdadero, creo que booleano podria ir aca? pero puse ese por si las varas I guess

    def imprimir_arbol_decorado(self, nodo, nivel=0):
        """Imprime el arbol con informacion de tipos de forma más legible."""
        if nodo is None:
            return
            
        indentacion = "  " * nivel
        tipo_info = nodo.atributos.get('tipo', 'SIN_TIPO')
        
        # Formatear mejor la salida
        valor_str = f"'{nodo.valor}'" if nodo.valor is not None else "''"
        tipo_str = str(tipo_info).split('.')[-1] if hasattr(tipo_info, 'name') else str(tipo_info)
        
        print(f"{indentacion} .> {nodo.tipo.name}: {valor_str} .> [{tipo_str}]")
        
        # Imprimir hijos
        if hasattr(nodo, 'hijos') and nodo.hijos:
            for hijo in nodo.hijos:
                if hijo is not None:
                    self.imprimir_arbol_decorado(hijo, nivel + 1)

class Verificador:
    """Verificador semantico para el lenguaje de programacion.
    
    Realiza verificacion de tipos, tabla de simbolos y deteccion de errores semanticos.
    """
    
    def __init__(self, nuevo_arbol: ArbolSintaxisAbstracta):
        self.arbol = nuevo_arbol
        self.tabla_simbolos = TablaSimbolos()
        self.visitador = Visitante(self.tabla_simbolos)
        self._configurar_ambiente_estandar()

    def print_arbol(self):
        """Imprime el arbol sintactico normal."""
        if self.arbol.raiz is None:
            print("No hay arbol para mostrar")
        else:
            print("\n" + "="*60)
            print("ARBOL SINTACTICO ABSTRACTO")
            print("="*60)
            self.arbol.imprimir()
    
    def print_arbol_decorado(self):
        """Imprime el arbol decorado con informacion de tipos."""
        if self.arbol.raiz is None:
            print("No hay arbol para mostrar")
        else:
            print("\n" + "="*60)
            print("ARBOL DECORADO CON TIPOS")
            print("="*60)
            self.visitador.imprimir_arbol_decorado(self.arbol.raiz)
            print("="*60)
    
    def imprimir_errores(self):
        """Imprime todos los errores encontrados durante la verificacion."""
        print("\n" + "="*60)
        print("REPORTE DE ERRORES")
        print("="*60)
        
        if not self.visitador.errores:
            print("✓ No se encontraron errores durante la verificacion")
        else:
            print(f"✗ Se encontraron {len(self.visitador.errores)} errores:")
            for i, error in enumerate(self.visitador.errores, 1):
                print(f"  {i}. {error}")
        
        print("="*60)
    
    def imprimir_tabla_final(self):
        """Imprime el estado final de la tabla de simbolos."""
        simbolos_usuario = self.tabla_simbolos.obtener_simbolos_usados()
        
        print("\n" + "="*60)
        print("TABLA DE SIMBOLOS FINAL")
        print("="*60)
        print(f"Profundidad final: {self.tabla_simbolos.profundidad}")
        
        if not simbolos_usuario:
            print("No se definieron simbolos de usuario")
        else:
            print("Simbolos definidos por el usuario:")
            for i, registro in enumerate(simbolos_usuario, 1):
                tipo_nombre = (registro['Tipo'].name 
                             if hasattr(registro['Tipo'], 'name') 
                             else str(registro['Tipo']))
                print(f"  {i}. {registro['Nombre']} - Tipo: {tipo_nombre} - Profundidad: {registro['Profundidad']}")
        
        print("="*60)

    def _configurar_ambiente_estandar(self):
        """Configura las funciones estandar del lenguaje."""
        # Solo se agregan al ambiente, no se muestran a menos que se usen
        funciones_estandar = [
            ('pelar', TiposDato.NINGUNO),
            ('marinar', TiposDato.NINGUNO),
            ('quemo', TiposDato.ERROR)
        ]

        for nombre, tipo in funciones_estandar:
            nodo = Nodo(tipo=TipoNodo.FUNCION, valor=nombre, atributos={'tipo': tipo})
            # No imprimimos el registro de funciones estandar
            diccionario = {
                'Nombre': nombre,
                'Profundidad': 0,
                'Referencia': nodo,
                'Tipo': tipo,
                'NombreRegistro': nombre
            }
            self.tabla_simbolos.simbolos.append(diccionario)

    def verificar(self):
        """Ejecuta la verificacion completa del arbol."""
        print("\n" + "="*60)
        print("INICIANDO VERIFICACION SEMANTICA")
        print("="*60)
        
        if self.arbol.raiz is None:
            print("ERROR: No hay arbol para verificar")
            return False
        
        try:
            # Ejecutar verificacion
            self.visitador._Visitante__visitar(self.arbol.raiz)
            
            # Mostrar resultados
            self.print_arbol_decorado()
            self.imprimir_tabla_final()
            self.imprimir_errores()
            
            # Retornar si hubo errores
            return len(self.visitador.errores) == 0
            
        except Exception as e:
            print(f"ERROR CRITICO durante la verificacion: {e}")
            return False