
def carrera_caracoles(comida, temperatura, humedad):
    meta = 10
    A = 0
    B = 0
    t = 0
    print("CARRERA DE CARACOLES")
    print("Condiciones ambientales recibidas")
    while A < meta:
                if B < meta:
                                    temp_t = 1
                                    t = t + temp_t
                                    mueveA = 1
                                    if temperatura > 30:
                                                                temp_val = 0
                                                                mueveA = temp_val + 0
                                    if comida < 5:
                                                                temp_val2 = 0
                                                                mueveA = temp_val2 + 0
                                    if mueveA > 0:
                                                                A = A + mueveA
                                                                print("A avanza")
                                    mueveB = 1
                                    if humedad < 20:
                                                                temp_val4 = 0
                                                                mueveB = temp_val4 + 0
                                    if temperatura > 20:
                                                                if temperatura < 25:
                                                                                                    temp_val5 = 2
                                                                                                    mueveB = temp_val5 + 0
                                    if mueveB > 0:
                                                                B = B + mueveB
                                                                print("B avanza")
                                    print("Turno completado")
    print("CARRERA TERMINADA")
    gana = 0
    if A > B:
                temp_val7 = 1
                gana = temp_val7 + 0
                print("Gana A")
    elif B > A:
                temp_val8 = 2
                gana = temp_val8 + 0
                print("Gana B")
    else:
                print("Empate")
    print("Fin")