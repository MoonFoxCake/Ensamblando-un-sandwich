import os
from Explorador.Explorador import Explorador
from Analizador.Analizador import Analizador

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

    # Generar la lista lista_lexica con los datos crudos
    lista_lexica = [comp.to_lista() for comp in componentes]

    # Ahora ya podés pasar esto directamente al analizador:
    print(lista_lexica)
