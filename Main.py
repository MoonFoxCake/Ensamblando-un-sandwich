import os
from Analizador.AnalizadorLimpio import Analizador
from Explorador.Explorador import Explorador
from Verificador.Verificador import Verificador
#from Generador.Visitador import VisitadorPython   
from Generador.generador import Generador


def imprimir_arbol(nodo, nivel=0, indice=None):
    if nodo is None:
        return
    indent = "  " * nivel
    indice_str = f"[{indice}]" if indice is not None else ""

    extras = []
    if hasattr(nodo, 'valor'):
        extras.append(f"valor={getattr(nodo, 'valor', '')!r}")
    if hasattr(nodo, 'tipo'):
        extras.append(f"tipo={getattr(nodo, 'tipo', '')}")
    if hasattr(nodo, 'atributos'):
        extras.append(f"atributos={getattr(nodo, 'atributos', '')}")
    extras_str = ", ".join(extras)
    print(f"{indent}{indice_str}{nodo.tipo.name}: {extras_str}")
    for i, hijo in enumerate(getattr(nodo, 'hijos', [])):
        imprimir_arbol(hijo, nivel + 1, i)

# Ruta de la carpeta con los archivos de ejemplo
directorio_ejemplos = 'Ejemplos de Codigo'

# Obtener todos los archivos con extensión '.sdw' en el directorio de ejemplos
archivos_ejemplos = [f for f in os.listdir(directorio_ejemplos) if f.endswith('.sdw')]

# Procesar cada archivo de ejemplo
for archivo_nombre in archivos_ejemplos:
    print(f"\nProcesando archivo: {archivo_nombre}")
    
    # Cargar el archivo de ejemplo
    with open(os.path.join(directorio_ejemplos, archivo_nombre), 'r', encoding='utf-8') as archivo:
        contenido = archivo.readlines()

    # Crear el explorador con el contenido
    explorador = Explorador(contenido)
    explorador.explorar()  # Explorar para generar los componentes léxicos
    componentes = explorador.componentes  # Obtener los componentes generados
    #for componente in componentes:
        #print(componente.tipo, componente.texto)  # Imprimir los componentes generados

    
    #Si se comenta todo lo que está debajo de esto funciona hasta el explorador
    
    # Crear el analizador
    analizador = Analizador(componentes)

    analizador.analizar()
    #analizador.asa.imprimir()  # Imprimir el árbol de sintaxis abstracta en preorden   

    ##Pruebas de generación de código
    verificador = Verificador(analizador.asa)
    verificador.verificar()
    #verificador.print_arbol()

    #print("\nÁrbol de Sintaxis Abstracta:")
    #imprimir_arbol(analizador.asa.raiz)


    #visitador = VisitadorPython()
    #codigo_python = visitador.visitar(analizador.asa.raiz)  # O el nodo raíz de tu AST
    #print("\nCódigo Python generado:\n")
    #print(codigo_python)
    
    generador = Generador(analizador.asa)
    codigo_python = generador.generar_codigo()  # Esto ya incluye el ambiente estándar
    print("\nCódigo Python generado:\n")
    print(codigo_python)
    #Guardar el código generado en un archivo .py  
    # DESCOMENTAR LO DE ABAJO SI SE DESEA GUARDAR LOS ARCHIVOS COMO .PY
    #nombre_salida = os.path.splitext(archivo_nombre)[0] + ".py"
    #ruta_salida = os.path.join(directorio_ejemplos, nombre_salida)
    #with open(ruta_salida, 'w', encoding='utf-8') as archivo_py:
    #    archivo_py.write(codigo_python)
    #print(f"\nEl código Python se guardó en: {ruta_salida}")



    
