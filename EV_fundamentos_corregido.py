fortificados = []
iluminados = []

stock_fortificados = 500
stock_iluminados = 500

#---VALIDACIONES 

def validar_nombre(nombre, lista_concierto):
    for entrada in lista_concierto:
        if entrada["nombre"].lower() == nombre.lower():
            return False
    return True


def validar_codigo_fortificados(codigo):
    if len(codigo) < 6:
        return False
    if not any(c.isupper() for c in codigo):
        return False
    if not any(c.isdigit() for c in codigo):
        return False
    if " " in codigo:
        return False
    return True


def validar_codigo_iluminados(codigo):
    if len(codigo) < 5:
        return False
    mayusculas = sum(1 for c in codigo if c.isupper())
    if mayusculas < 3:
        return False
    if not any (c.isdigit() for c in codigo):
        return False
    if " " in codigo:
        return False
    return True


def compra_fortificados():
    global fortificados

    if len(fortificados) >= stock_fortificados:
        print("No queda stock para 'Los Fortificados'.")
        return
    
    nombre = input("Ingrese nombre de comprador: ").strip()
    if not validar_nombre(nombre, fortificados):
        print("Este nombre ya fue registrado. Compra rechazada.")
        return
    
    tipo = input("Ingrese tipo de entrada (G/V): ").upper()
    if tipo not in ("G", "V"):
        print("Tipo de entrada no válido.")
        return
    
    while True:
        codigo = input("Ingrese código de confirmación: ")
        if validar_codigo_fortificados(codigo):
            print("Código validado.")
            break
        else:
            print("Código no válido. Intente otra vez")

    fortificados.append({
        "nombre": nombre,
        "tipo": tipo,
        "codigo": codigo
    })
    print("Entrada registrada con éxito para 'Los Fortificados'")


def compra_iluminados():
    global iluminados

    if len(iluminados) >= stock_iluminados:
        print("No queda stock para 'Los Iluminados'")
        return
    
    nombre = input('Ingresar nombre de comprador: ')
    if not validar_nombre(nombre, iluminados):
        print('El nombre ya fue registrado. Compra rechazada.')
        return
    
    tipo = input("Ingrese tipo de entrada (CV/PAL):").upper()
    if tipo not in ("CV", "PAL"):
        print("Tipo de entrada no válido.")
        return
    
    while True:
        codigo = input('Ingrese código de confirmación: ')
        if validar_codigo_iluminados(codigo):
            print("Codigo validado.")
            break
        else:
            print("Código no válido. Intente otra vez")

    iluminados.append({
        "nombre": nombre,
        "tipo": tipo,
        "codigo": codigo
    })
    print("Entrada registrada con éxito para 'Los iluminados'")

def mostrar_stock():
    restantes_f = stock_fortificados - len(fortificados)
    restantes_i = stock_iluminados - len(iluminados)

    print(f"Entradas disponibles para 'Los Fortificados': {restantes_f}")
    print(f"Entradas dispobles para 'Los Iluminados': {restantes_i}")


def menu():
    while True:
        print("\nTOTEM AUTOSERVICIO CONCIERTOS ROCK AND CHILE")
        print("1. Comprar entrada a los fortificados")
        print("2. Comprar entrada a los iluminados")
        print("3. Revisar stock entradas")
        print("4. Salir")

        opcion = input("Ingrese opción: ")

        if opcion == "1":
            compra_fortificados()
        elif opcion == "2":
            compra_iluminados()
        elif opcion == "3":
            mostrar_stock()
        elif opcion == "4":
            print("Adios. Gracias por su compra")
            break
        else:
            print("Debe ingresar una opción válida.")

menu()