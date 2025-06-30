
def carrera_caracoles(comida, temperatura, humedad):
 meta = 10
 A = 0
 B = 0
 t = 0
 print("CARRERA DE CARACOLES")
 print("Condiciones ambientales recibidas")
 while A < meta:
    if B < meta:
         t = t + 1
         mueveA = 1
         if temperatura > 30:
                mueveA = mueveA + 2
         if comida < 5:
                mueveA = mueveA + 0
         if mueveA > 0:
                A = A + mueveA
                print("A avanza")
         mueveB = 1
         if humedad < 15:
                mueveB = mueveB + 3
         if temperatura > 20:
                if temperatura < 25:
                         mueveB = mueveB + 3
         if mueveB > 0:
                B = B + mueveB
                print("B avanza")
         print("Turno completado")
 print("CARRERA TERMINADA")
 gana = 0
 if A > B:
    print("Gana A")
 elif B > A:
    print("Gana B")
 else:
    print("Empate")
 print("Fin")
carrera_caracoles(10, 35, 50)

carrera_caracoles(10, 25, 50)