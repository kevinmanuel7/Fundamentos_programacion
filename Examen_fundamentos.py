catalogo = {
        'BK001': {
                "id": 'BK001',
                "titulo":'El Quijote', 
                "autor":'Miguel de Cervantes', 
                "tipo":'físico', 
                "paginas":1200, 
                "editorial":'Editorial Planeta', 
                "idioma":'español'
                },

        'BK002':{
                "id": 'BK002',
                "titulo":'1984',
                "autor":'George Orwell', 
                "tipo":'digital', 
                "paginas":328, 
                "editorial":'Penguin', 
                "idioma":'inglés'
                },
        'BK003': 
                {
                "id": 'BK003',
                "titulo":'Rayuela', 
                "autor":'Julio Cortázar', 
                "tipo":'físico', 
                "paginas":600, 
                "editorial":'Sudamericana', 
                "idioma":'español'},

        'BK004': 
                {
                "id":'BK004',
                "titulo":'Sapiens', 
                "autor":'Yuval Noah Harari', 
                "tipo":'digital', 
                "paginas":450, 
                "editorial":'Debate', 
                "idioma":'inglés'}
            }

inventario = {
            'BK001': {"precio":15990, 
                      "unidades_disponibles":3},
            'BK002': {"precio":8990, 
                      "unidades_disponibles":0},
            'BK003': {"precio":18990, 
                      "unidades_disponibles":7},
            'BK004': {"precio":12500, 
                      "unidades_disponibles":5}
                }

def stock_editorial(editorial):
    editorial = editorial.lower()
    total = 0

    for codigo in catalogo:
        datos = catalogo[codigo]

        if datos["editorial"].lower() == editorial:
            total += inventario[codigo]["unidades_disponibles"]
    
    print("Stock total disponible para la editorial: ", editorial, "=", total)


def buscar_por_precio():
    try:
        p_min = int(input("Ingrese precio mínimo: "))
        p_max = int(input("Ingrese precio máximo: "))
    except:
        print("debe ingresar valores numericos")
        return
    
    resultados = []

    for codigo in catalogo:
        precio = inventario[codigo]["precio"]
        stock = inventario[codigo]["unidades_disponibles"]

        if precio >= p_min and precio <= p_max and stock > 0:
            titulo = catalogo[codigo]["titulo"]
            resultados.append(titulo +" - "+ codigo)
        
    if len(resultados) == 0:
            print("No hay libros disponibles en ese rango de precio.")

    else:
        resultados.sort()
        print("Libros encontrados:")
        for item in resultados:
            print(item)


def actualizar_libro():
    ingr_codigo = input("Ingresar codigo del libro: ").upper()

    existe = False
    for codigo in inventario:
        if ingr_codigo == codigo:
            existe = True
            break
    
    if existe == False:
        print("El código que buscas no existe en inventario.")
        return
    
    try:
        nuevo_precio = int(input("Ingrese nuevo precio: "))
        inventario[codigo]["precio"] = nuevo_precio
        print("Precio actualizado con exito")
    except:
        print("Debe ingresar un número válido.")

    
def menu():
    while True:
        print("***MENU PRINCIPAL***")
        print("1. Stock por editorial")
        print("2. Buscar libros por precio")
        print("3. Actualizar precio de libro")
        print("4. Salir")

        opcion = input("Ingrese opción: ")

        if opcion == "1":
            editorial_ingresada = input("ingresa editorial: ")
            stock_editorial(editorial_ingresada)
        elif opcion == "2":
            buscar_por_precio()
        elif opcion == "3":
            actualizar_libro()
        elif opcion == "4":
            print("Programa finalizado.")
            break
        else:
            prInt("Debe selecionar una opción válida!!")

menu()