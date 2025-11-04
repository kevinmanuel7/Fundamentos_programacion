turistas = {
    "001": ["John Doe", "Estados Unidos", "12-01-2024"],
    "002": ["Emily Smith", "Estados Unidos", "23-03-2024"],
    "012": ["Julian Martinez", "Argentina", "19-09-2023"],
    "014": ["Agustin Morales", "Argentina", "28-03-2024"],
    "005": ["Carlos Garcia", "Mexico", "10-05-2024"],
    "006": ["Maria Lopez", "Mexico", "08-12-2023"],
    "007": ["Joao Silva", "Brasil", "20-06-2024"],
    "003": ["Michael Brown", "Estados Unidos", "05-07-2023"],
    "004": ["Jessica Davis", "Estados Unidos", "15-11-2024"],
    "008": ["Ana Santos", "Brasil", "03-10-2023"],
    "010": ["Martin Fernandez", "Argentina", "13-02-2023"],
    "011": ["Sofia Gomez", "Argentina", "07-04-2024"],
}

def turistas_por_pais(pais: str):
    pais_buscado = pais.strip().lower()
    nombres_encontrados = []

    print(f'Turista de {pais.title()}')

    for datos in turistas.values():
        pais_origen = datos[1].lower()

        if pais_origen == pais_buscado:
            nombre = datos[0]
            nombres_encontrados.append(nombre)
    
    if nombres_encontrados:
        for nombre in nombres_encontrados:
            print(f'{nombre}')
    else:
        print(f'No se encontraron turistas registrados de {pais.title()}')


def turistas_por_mes():
    while True:
        try:
            mes = input('Ingresa el numero del mes (1-12)')
            mes_int = int(mes)
            if 1 <= mes_int <= 12:
                mes_muestra = f'{mes_int:02d}'
                break
            else:
                print('Error: el mes debe ser un numero entre 1 y 12')
        except ValueError:
            print('Error: ingrese un valor numerico de 1 a 12')
    
    contador_mes = 0
    total_turistas = len(turistas)

    for datos in turistas.values():
        fecha_ingreso = datos[2]
        mes_ingreso = fecha_ingreso[3:5]

        if mes_ingreso == mes_muestra:
            contador_mes +=1

    if total_turistas == 0:
        return 0.0
    
    porcentaje = (contador_mes/total_turistas)*100
    return round(porcentaje, 1)

def eliminar_turista():
    nombre_a_eliminar = input('Ingrese el nombre completo del turista a eliminar: ').strip().lower()
    id_a_eliminar = None

    for id_turista, datos in list(turistas.items()):
        nombre_turista_dic = datos[0].lower()

        if nombre_turista_dic == nombre_a_eliminar:
            id_a_eliminar = id_turista
            break

    if id_a_eliminar:
        del turistas[id_a_eliminar]
        print('Turista eliminado con exito!')
    else:
        print('Turista no encontrado, no se pudo eliminar')

while True:
    print('\n' + '='*20)
    print('***MENU PRINCIPAL***')
    print('1. Turistas por país')
    print('2. Turistas por mes')
    print('3. Eliminar turista')
    print('4. Salir')
    print('='*20)
    
    opcion = (input('Selecciona una opción (1-4): ')).strip()
    print('-'*20)

    if opcion == '1':
        pais = input('Ingrese el nombre del país a buscar: ')
        turistas_por_pais(pais)

    elif opcion == '2':
        porcentaje = turistas_por_mes()
        print(f'El porcentaje de turistas que ingresó este mes es: {porcentaje:.1f}%')

    elif opcion == '3':
        eliminar_turista()
        
    elif opcion == '4':
        print('Programa terminado')
        break

    else:
        print('Opción no válida, seleccione un número entre 1 y 4.')