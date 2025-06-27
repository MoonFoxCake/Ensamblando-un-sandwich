import os
from Analizador.AnalizadorLimpio import Analizador
from Explorador.Explorador import Explorador
from Verificador.Verificador import Verificador
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

archivo_ejemplo = 'miniprogra.sdw'

with open(archivo_ejemplo, 'r', encoding='utf-8') as archivo:
    contenido = archivo.readlines()

# 1. Explorador
input("\n==========\nPresiona Enter para ejecutar el EXPLORADOR...\n==========")
print("\n========== INICIO EXPLORADOR ==========")
explorador = Explorador(contenido)
explorador.explorar()
componentes = explorador.componentes
print("\n=== COMPONENTES LÉXICOS ===")
for componente in componentes:
    print(f"{componente.tipo}: {componente.texto}")
print("========== FIN EXPLORADOR ==========\n")

# 2. Analizador
input("==========\nPresiona Enter para ejecutar el ANALIZADOR...\n==========")
print("\n========== INICIO ANALIZADOR ==========")
analizador = Analizador(componentes)
analizador.analizar()
print("\n=== ÁRBOL DE SINTAXIS ABSTRACTA (ASA) ===")
imprimir_arbol(analizador.asa.raiz)
print("========== FIN ANALIZADOR ==========\n")

# 3. Verificador
input("==========\nPresiona Enter para ejecutar el VERIFICADOR...\n==========")
print("\n========== INICIO VERIFICADOR ==========")
verificador = Verificador(analizador.asa)
verificador.verificar()
print("\n=== VERIFICACIÓN COMPLETADA ===")
print("========== FIN VERIFICADOR ==========\n")

# 4. Generador
input("==========\nPresiona Enter para ejecutar el GENERADOR...\n==========")
print("\n========== INICIO GENERADOR ==========")
generador = Generador(analizador.asa)
codigo_python = generador.generar_codigo()
print("\n=== CÓDIGO PYTHON GENERADO ===\n")
print(codigo_python)
print("========== FIN GENERADOR ==========")
# Guardar el código generado en un archivo .py
# DESCOMENTAR LO DE ABAJO SI SE DESEA GUARDAR LOS ARCHIVOS COMO .PY
#nombre_salida = os.path.splitext(archivo_ejemplo)[0] + ".py"
#with open(nombre_salida, 'w', encoding='utf-8') as archivo_py:
#    archivo_py.write(codigo_python)
#print(f"\nEl código Python se guardó en: {nombre_salida}")