los_fortificados = []
los_iluminados = []

def ent_fortificados():
    nombre = input('Ingrese nombre comprador: ').strip
    for n in los_fortificados:
        if n['nombre'].lower() == nombre.lower():
            print('El comprador ya existe')
            return
        else:
            print('Nombre registrado exitosamente')

    entrada = input('Seleccione el tipo de entrada que desea (G = General - V = VIP): ').upper()
    if entrada not in ["G", "V"]:
        print('Error: tipo de entrada invalida. Solo: "G" o "V"')
        return
        
    codigo = input('Ingrese código: ').strip()

    if len(codigo) < 6:
        print('Error: El código debe tener al menos 6 carácteres')
        return
    else:
        print('Código ingresado con éxito')

    los_fortificados.append({
        "nombre": nombre,
        "entrada": entrada,
        "codigo": codigo
    })
    print('***Entrada comprada exitosamente***')


def ent_iluminados():
    nombre = input('Ingrese nombre comprador: ').strip
    for n in los_iluminados:
        if n['nombre'].lower() == nombre.lower():
            print('El comprador ya existe')
            return
        else:
            print('Nombre registrado exitosamente')

    entrada = input('Seleccione el tipo de entrada que desea (CV = Cancha vip - PAL = Palco): ').upper()
    if entrada not in ["CV", "PAL"]:
        print('Error: tipo de entrada invalida. Solo: "CV" o "PAL"')
        return
        
    codigo = input('Ingrese código: ').strip()

    if len(codigo) < 6:
        print('Error: El código debe tener al menos 6 carácteres')
        return
    else:
        print('Código ingresado con éxito')

    los_iluminados.append({
        "nombre": nombre,
        "entrada": entrada,
        "codigo": codigo
    })
    print('***Entrada comprada exitosamente***')


def salir():
    print('Programa terminado...')
    exit()


def main():
    while True:
        print('-'*30)
        print('TOTEM AUTOSERVICIO CONCIERTOS ROCK AND CHILE')
        print('1. Comprar entrada a Los Fortificados')
        print('2. Comprar entrada a Los Iluminados')
        print('3. Stock de entradas para ambos conciertos')
        print('4. Salir')
        print('-'*30)
        opcion_menu = int(input('Seleccione una opción: '))

        if opcion_menu == 1:
            ent_fortificados()
        elif opcion_menu == 2:
            ent_iluminados()
        elif opcion_menu == 4:
            salir()
        else:
            print('Debe ingresar un número entre 1 y 4')

main()