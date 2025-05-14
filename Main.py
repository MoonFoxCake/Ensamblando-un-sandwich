import os
#from Analizador import Analizador
from Explorador.Explorador import Explorador


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
    for componente in componentes:
        print(componente.tipo, componente.texto)  # Imprimir los componentes generados

    
    #Si se comenta todo lo que está debajo de esto funciona hasta el explorador
    
    """ # Crear el analizador
    analizador = Analizador(componentes)
    
    # Analizar el contenido y crear el árbol
    arbol = analizador.analizar()
    
    # Imprimir el árbol resultante
    print(arbol) """
