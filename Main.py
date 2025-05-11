import os
from Explorador import Explorador
from Analizador import Analizador

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

    # Obtener los componentes y pasarlos al analizador
    componentes_lexicos = explorador.obtener_componentes()

    # Crear el analizador y analizar el árbol
    analizador = Analizador(componentes_lexicos)
    analizador.analizarArbol()
    
    # Imprimir el árbol generado
    analizador.imprimirarbolAbstracto()