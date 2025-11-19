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
                {"titulo":'Rayuela', 
                 "autor":'Julio Cortázar', 
                 "tipo":'físico', 
                 "paginas":600, 
                 "editorial":'Sudamericana', 
                 "idioma":'español'},
        'BK004': {"titulo":'Sapiens', 
                  "autor":'Yuval Noah Harari', 
                  "tipo":'digital', 
                  "paginas":450, 
                  "editorial":'Debate', 
                  "idioma":'inglés'}
            }

inventario = {
            'BK001': {"precio":15990, 
                      "unidaddes_disponibles":3},
            'BK002': {"precio":8990, 
                      "unidades_disponibles":0},
            'BK003': {"precio":18990, 
                      "unidades_disponibles":7},
            'BK004': {"precio":12500, 
                      "unidades_disponibles":5}
                }

def stock_editorial():
    editorial = input("Ingrese nombre de editorial: ").lower()
    total = 0

    for libro in catalogo:
        if libro["editorial"].lower() == editorial:
            id_libro = libro["id"]

            for item in inventario:
                if item["id"] == id_libro:
                    total += item["unidades_disponibles"]
                    break
    print(f"El stock total de la editorial '{editorial}' es: {total}")

def buscar_por_precio(p_min, p_max):
    resultados = []

    for libro in catalogo:
        if p_min <= libro["precio"] <= p_max:
            for item in inventario:
                if item["id"] == libro["id"] and item["stock"] > 0:
                    resultados.append(f"{libro["titulo"]}")


        

    nuevo_precio = int(input("Ingrese nuevo precio: "))

def menu():
    while True:
        print("***MENU PRINCIPAL***")
        print("1. Stock por editorial")
        print("2. Buscar libros por precio")
        print("3. Actualizar precio de libro")
        print("4. Salir")

        opcion = input("Ingrese opción: ")

        if opcion == "1":
            stock_editorial()
        elif opcion == "2":
            buscar_por_precio()
        elif opcion == "3":
            actualizar_libro()
        elif opcion == "4":
            print("Programa finalizado.")
            break
        else:
            print("Debe selecionar una opción válida!!")

menu()