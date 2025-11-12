import csv
import os
import re
from datetime import datetime


mascotas = []
atenciones = []

cont_mascota_id = 1
cont_atencion_id = 1

DATA_DIR = "data"
MASCOTAS_FILE = os.path.join(DATA_DIR, "mascotas.csv")
ATENCIONES_FILE = os.path.join(DATA_DIR, "atenciones.csv")

def aseg_data_dir():
    if not os.path.exists(DATA_DIR): #Para verificar la ruta de DATA_DIR
        os.makedirs(DATA_DIR) #Si no existe crea el directorio (solo se ejecuta si la condición if es verdadera, es decir, no existe)

def validar_int(value_str, field_name="valor"): #Para convertir una cadena de texto en un número entero
    try:
        val = int(value_str) #Intenta realizar la conversión, si value_str es 123, val será nro entero 123, si es abc, está línea lanzará un error
        return val #Si la conversión es exitosa, la función devuelve el nro entero resultante
    except ValueError: #Si la conversion falla, python captura el error.
        raise ValueError(f"{field_name} debe ser un número entero.") #En lugar de dejar que el programa se detenga con el msje predeterminado de python, la función levanta la excepción con un mensaje personalizado.
    
def validate_positive_int(value_str, field_name="valor"): #Sirve para asegurar que un valor de entrada sea un nro entero y ademas, positivo o cero (no negativo).
    val = validar_int(value_str, field_name) 
    if val < 0: #Si val es menor a 0, lanzará un error con el mensaje de abajo.
        raise ValueError(f"{field_name} debe ser positivo o cero.")
    return val #Si el valor cumple los requisitos (es entero y =+0), la función devuelve el nro entero.

def validate_positive_float(value_str, field_name="valor"): #Función identica a la de arriba, pero para manejar valores decimales.
    try:
        val = float(value_str) #Intenta convertir la cadena de entrada a tipo float
    except ValueError: #Si la cadena no es un numero válido, se captura el error.
        raise ValueError(f"{field_name} debe ser un número (puede tener decimales).")
    if val < 0:
        raise ValueError(f"{field_name} debe ser positivo o cero.")
    return val #Si la caden se convirtió exitosamente a un float y el valor es += 0, la función devuelve un nro decimal.

def validar_rut(rut: str): #Validación básica para RUT 
    rut = rut.strip() #Elimina cualquier espacio en blanco al inicio o al final de la cadena de entrada.
    if not re.fullmatch(r"\d{1,8}-{0-9kK}", rut): #Utiliza esta función para verificar si toda la cadena limpia coincide con el patron esperado ("\d{1-8}"" de 1 a 8 dígitos numéricos(0-9), "-"" un guión, "[0-9kK]" un dígito final que puede ser un nro 0-9 o una letras k-K)
        raise ValueError("RUT inválido. Formato esperado: 12345678-9") #si re.fullmatch falla se lanza un ValueError
    return rut.upper() #Si la validación es exitosa, convierte toda la cadena en mayúsculas y la devuelve.

def validar_fecha(date_str: str): #Para validar una cadena de texto que representa una fecha válida y sigue un formato especifico.
    try: #Está envuelta en un bloque try/except porque la conversión puede fallar de dos maneras: si el formato es incorrecto, o la fecha no existe.
        fecha= datetime.strptime(date_str, "%Y-%m-%d") #Análiza la cadena basandose estrictamente en el formato provisto(año-mes-día). Si no cumple el formato, esta lanza un ValueError, en cambio, si tiene exito crea un objeto "datetime" llamado "fecha".
        return fecha.strftime("%Y-%m-%d") #Si la validación fue exitosa, la función usa (string format time) para formatear de nuevo el objeto "fecha" con el formato "AAAA-MM-DD"
    except ValueError: #Si se captura un nuevo error durante el análisis, la función lanza un ValueError especificando el formato correcto esperado.
        raise ValueError("Fecha inválida. Formato esperado AAAA-MM-DD")
    
def encontrar_mascota_por_id(mid: int): #Esta función tiene la tarea de buscar y devolver una mascota especifica dentro de una lista o colección.
    for m in mascotas: #Esta función recorre cada elemento de la colección "mascotas"
        if m.get("id") == mid: #Intenta obtener el valor asociado a la clave id. Y lo compara con el valor "id" que se pasó como argumento a la función mid(mascotaid)
            return m #Si la condición es verdadera (si el id de mascota coincide con el mid) la función devuelve inmediatamente el diccionario completo de la mascota(m) y termina la ejecución.
    return None #Si el ciclo for termina de recorrer toda la lista sin encontrar ninguna coincidencia, finalmente la función devuelve el valor especial None.

def duplicado_mascota(nombre: str, rut_dueño: str, excluir_id: int = None): #Esta función se utiliza para verificar si ya existe una mascota inscrita con el mismo nombre bajo el mismo dueño (rut).
    nombre_norm = nombre.strip().lower() #Para que no existan fallos relacionados a espacios, mayusculas o minusculas la función debe normalizar las entradas.
    rut_norm = rut_dueño.strip().upper() #Aquí aplica lo mismo que en el caso del nombre.
    for m in mascotas: #Itera sobre cada mascosa "m" en la lista global "mascotas".
        if excluir_id is not None and m.get("id") == excluir_id: #Para que la f
            continue
    if m.get("nombre", "").strip().lower() == nombre_norm and m.get("rut_dueño", "").strip().upper() == rut_norm: #Esta función realiza una doble comprobación para la mascota actual(m). Comprueba si el nombre normalizado coincide con el de la entrada, y hace lo mismo con el RUT. Si ambas condiciones son verdaderas, se ha encontrado un duplicado y la función inmediatamente devuelve un True.
        return True 
    return False #Si el ciclo for termina de recorrer todas las mascotas sin encontrar una coincidencia que cumpla ambas condiciones, la función devuelve False, indicando que no existe un duplicado.

#--- CRUD ---
#CREATE
def add_mascota(nombre, especie, raza, edad, rut_dueño): #Función para registrar una nueva mascota en el sistema.
    global cont_mascota_id #Permite a la función acceder y modificar la variable cont_mascota_id que está definida fuera de la función
    nombre = nombre.strip()
    especie = especie.strip()
    raza = raza.strip()
    edad = int(edad) #El rut se convierte a un entero
    rut_dueño = rut_dueño.strip().upper() #El rut se convierte a mayusculas (K) para estandarización

    if duplicado_mascota(nombre, rut_dueño): #Llama a la función de validación para comprobar si una mascota con el mismo nombre y el mismo RUT de dueño ya existe.
        raise ValueError("Ya existe una mascota con ese nombre para el mismo RUT.") #Si se encuentra duplicado lanza un error y detiene la ejecución, evitando la adición de datos repetidos.

    mascota = { #Creacion del registro: Se crea un diccionario con el nombre "mascota" que agrupa todos los datos limpios y validados.
        "id": cont_mascota_id, #El campo id toma el valor actual de cont_mascota_id, asegurando un id único para el nuevo registro
        "nombre": nombre,
        "especie": especie,
        "raza": raza,
        "edad": edad,
        "rut_dueño": rut_dueño,
    }
    mascotas.append(mascota) #El diccionario recién creado se añade a la lista global "mascotas"
    cont_mascota_id += 1 #El contador global se incrementa en 1
    return mascota #La función devuelve el diccionario de la mascota que acaba de ser creada y añadida.

#UPDATE
def update_mascota(mid: int, updates): #Función para actualizar registro de mascotas
    m = encontrar_mascota_por_id(mid)
    if not m:
        raise ValueError("Mascota no encontrada.")


    nuevo_nombre = updates.get("nombre", m["nombre"]).strip()
    nuevo_rut = updates.get("rut_dueño", m["rut_dueño"]).strip().upper()
    if duplicado_mascota(nuevo_nombre, nuevo_rut, exclude_id=mid):
        raise ValueError("Actualización produciría un duplicado (misma mascota ya registrada para ese RUT).")

    for key in ("nombre", "especie", "raza", "edad", "rut_dueño"):
        if key in updates and updates[key] is not None:
            if key == "edad":
                m[key] = int(updates[key])
            else:
                m[key] = updates[key].strip()
    return m

#DELETE
def delete_mascota(mid: int): #Esta función se encarga de eliminar una mascota espedifica de la colección
    global atenciones
    m = encontrar_mascota_por_id(mid)
    if not m:
        raise ValueError("Mascota no encontrada.")
    mascotas.remove(m)

    atenciones = [a for a in atenciones if a.get("id_mascota") != mid]
    return True

#READ
def list_mascotas(): #Esta función tiene la tarea de imprimir en la consola una lista formateada de todas las mascotas registradas en el sistema.
    if not mascotas:
        print("No hay mascotas registradas.")
        return
    print("\nListado de mascotas:")
    for m in mascotas:
        print(f"ID: {m['id']} | Nombre: {m['nombre']} | Especie: {m['especie']} | Raza: {m['raza']} | Edad: {m['edad']} | RUT Dueño: {m['rut_dueño']}")

#--- ATENCIONES ---

def registro_atencion(id_mascota: int, fecha: str, descripcion: str, costo: float, veterinario: str): #Función para crear y registrar una nueva atención veterinaria asociada a una mascota existente
    global cont_atencion_id
    m = encontrar_mascota_por_id(id_mascota)
    if not m:
        raise ValueError("Mascota no encontrada para registrar atención.")


    fecha_val = validar_fecha(fecha)
    descripcion = descripcion.strip()
    costo_val = float(costo)
    if costo_val < 0:
        raise ValueError("Costo debe ser positivo o cero.")
    veterinario = veterinario.strip()


    atencion = {
        "id": cont_atencion_id,
        "id_mascota": id_mascota,
        "fecha": fecha_val,
        "descripcion": descripcion,
        "costo": costo_val,
        "veterinario": veterinario,
    }
    atenciones.append(atencion)
    cont_atencion_id += 1
    return atencion


def lista_atenciones_por_mascota(id_mascota: int): #Esta función tiene como objetivo filtrar y mostrar todas las atenciones veterinarias que han sido registradas para una mascota especifica determinada por su ID.
    res = [a for a in atenciones if a.get("id_mascota") == id_mascota]
    if not res:
        print("No hay atenciones para esa mascota.")
        return
    for a in res:
        print(f"ID: {a['id']} | Fecha: {a['fecha']} | Descripción: {a['descripcion']} | Costo: {a['costo']} | Veterinario: {a['veterinario']}")


#--- REPORTES ---
def gasto_por_rut(rut_dueño: str): #Tiene como objetivo calcular y mostrar el gasto veterinario total incurrido por un RUT, desglosando este gasto por cada una de sus mascotas
    rut_norm = rut_dueño.strip().upper() #Normaliza el RUT de entrada (limpia espacios y convierte a mayúsculas)
#Encontrar mascota por dueño
    mascotas_del_dueño = [m for m in mascotas if m.get("rut_dueño", "").upper() == rut_norm] #Filtra la lista global "mascotas" para encontrar todas las mascotas cuyo dueño coincide con el "rut_norm".
    if not mascotas_del_dueño: 
        print("No se encontraron mascotas para ese RUT.") #Si la lista está vacía, imprime un mensaje de no encontrado y finaliza.
        return
    total = 0.0 #Contador de gasto total
    detalle = [] #Lista que almacenará tuplas con el desglose del gasto
    for m in mascotas_del_dueño: #Inicio de bucle del cálculo. 
        m_atenciones = [a for a in atenciones if a.get("id_mascota") == m.get("id")] #Para cada mascota filtra la lista global "atenciones" para encontrar solo sus atenciones.
        sum_m = sum(a.get("costo", 0.0) for a in m_atenciones) #Calcula la suma de los costos de esas atenciones.
        detalle.append((m, sum_m, m_atenciones)) #Almacena el resultado de la mascota en la lista detalle
        total += sum_m #Acumula el subtotal al "total" general 
#Mostrar
    print(f"\nGasto total para RUT {rut_norm}: {total}") #Imprime el monto total gastado por el dueño en todas sus mascotas
    for m, sum_m, m_at in detalle: #Itera sobre la lista "detalle" e imprime el gasto desglosado por cada mascota
        print(f"- Mascota ID {m['id']} {m['nombre']}: {sum_m} (Atenciones: {len(m_at)})")


#--- CSV IMPORTACIÓN Y EXPORTACIÓN ---
def exportar_a_csv(mascotas_file=MASCOTAS_FILE, atenciones_file=ATENCIONES_FILE): #Es la encargada de guardar los datos. Toma los datos de las colecciones globales y los escribe en archivos de texto con el formato CSV
    aseg_data_dir() #Llama a una función auxiliar para asegurar que el directorio donde se guardaran los archivos exista.
# Exportar mascotas
    with open(mascotas_file, mode="w", newline='', encoding='utf-8') as f: #Abre el archivo especificado en modo de escritura
        writer = csv.DictWriter(f, fieldnames=["id", "nombre", "especie", "raza", "edad", "rut_dueño"]) #Crea un objeto "dicwriter" qie es ideal para escribir diccionarios en CSV
        writer.writeheader()
    for m in mascotas: #Itera sobre cada diccionario de mascota.
        writer.writerow({k: m.get(k, "") for k in ("id", "nombre", "especie", "raza", "edad", "rut_dueño")}) #Escribe cada mascota como una fila.
# Exportar atenciones
    with open(atenciones_file, mode="w", newline='', encoding='utf-8') as f: #El proceso se repite de manera identica para la lista "atenciones"
        writer = csv.DictWriter(f, fieldnames=["id", "id_mascota", "fecha", "descripcion", "costo", "veterinario"])
        writer.writeheader()
    for a in atenciones:
        writer.writerow({k: a.get(k, "") for k in ("id", "id_mascota", "fecha", "descripcion", "costo", "veterinario")})
    print(f"Datos exportados a: {mascotas_file} y {atenciones_file}") #Imprime un mensaje confirmando que la operación se completó exitosamente.


def importar_de_csv(mascotas_file=MASCOTAS_FILE, atenciones_file=ATENCIONES_FILE): #Esta función es responsable de la inicialización y carga de datos en el sistema.
    global mascotas, atenciones, cont_mascota_id, cont_mascota_id #Declara que la función va a reemplazar completamente las listas globales de "mascotas" y "atenciones", y que va a modificar los contadores de ID
    aseg_data_dir() #Asegura que el directorio de datos exista
    loaded_mascotas = [] #Se inicializan las listas temporales
    loaded_atenciones = []

    if os.path.exists(mascotas_file): #Comprueba si el archivo existe
        with open(mascotas_file, mode="r", newline='', encoding='utf-8') as f: #Abre el archivo en modo lectura "r". utiliza csv.DictReader. Este objeto lee cada línea de CSV y la convierte en diccionario.
            reader = csv.DictReader(f) #Utiliza csv.DictReader para leer cada línea del CSV y convertirla en un diccionario
            for row in reader: #El código itera sobre cada "row" (diccionario) del lector.
                try: #Utiliza try/except para intentar convertir el id a entero. Si la conversión falla, esa fila se salta "continue".
                    mid = int(row.get("id", "0"))
                except ValueError:
                    continue
            loaded_mascotas.append({ #Creación del diccionario
                "id": mid,
                "nombre": row.get("nombre", "").strip(),
                "especie": row.get("especie", "").strip(),
                "raza": row.get("raza", "").strip(),
                "edad": int(row.get("edad") or 0),
                "rut_dueño": row.get("rut_dueño", "").strip().upper(),
            })
    else:
        print(f"Archivo {mascotas_file} no encontrado. Se creará al exportar.")

    if os.path.exists(atenciones_file): #Aqui carga el archivo de atenciones. El proceso es similiar al de mascotas
        with open(atenciones_file, mode="r", newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    aid = int(row.get("id", "0"))
                    id_masc = int(row.get("id_mascota", "0"))
                    costo = float(row.get("costo", "0"))
                except ValueError:
                    continue
                loaded_atenciones.append({
                    "id": aid,
                    "id_mascota": id_masc,
                    "fecha": row.get("fecha", "").strip(),
                    "descripcion": row.get("descripcion", "").strip(),
                    "costo": costo,
                    "veterinario": row.get("veterinario", "").strip(),
                })
    else:
        print(f"Archivo {atenciones_file} no encontrado. Se creará al exportar.")

# Reemplazar datos actuales con lo cargado
    mascotas = loaded_mascotas #Las listas globales de trabajo son reemplazadas por los datos recién cargados
    atenciones = loaded_atenciones

# Actualizar contadores de ID para evitar colisiones (Sincronización)
    max_mid = max((m["id"] for m in mascotas), default=0) #Encuentra el ID más alto en la lista de mascotas cargadas
    max_aid = max((a["id"] for a in atenciones), default=0) #El mismo proceso pero en atenciones
    cont_mascota_id = max_mid + 1 #El contador global se establece en el máximo ID encontrado más uno. Esto garantiza que si se añaden nuevas mascotas despues de la importanción, estas tendrán un ID único que no chocará con los datos cargados.
    cont_atencion_id = max_aid + 1 #El mismo proceso que con mascotas


    print(f"Importación completada. Mascotas: {len(mascotas)}, Atenciones: {len(atenciones)}")



#--- MENÚ ---
def mostrar_menu(): #Esta función está encargada de presentar las opciones al usuario
    print("\n=== MENÚ VETERINARIA PETCARE ===")
    print("1. Registrar mascota")
    print("2. Actualizar mascota")
    print("3. Eliminar mascota")
    print("4. Listar mascotas")
    print("5. Registrar atención médica")
    print("6. Listar atenciones de una mascota")
    print("7. Reporte de gasto por RUT")
    print("8. Exportar datos a CSV")
    print("9. Importar datos desde CSV")
    print("0. Salir")


#--- INPUT ---
def input_mascota_interactivo(): #Esta función maneja el flujo interactivo para la creación de un nuevo registro de mascota. Su principal rol es recopilar datos del usuario y utilizar las funciones de validacion.
    try:
        nombre = input("Nombre: ")
        especie = input("Especie: ")
        raza = input("Raza: ")
        edad = validate_positive_int(input("Edad (años): "), "Edad")
        rut_dueño = validar_rut(input("RUT dueño (ej: 12345678-9): "))
        mascota = add_mascota(nombre, especie, raza, edad, rut_dueño)
        print(f"Mascota registrada con ID {mascota['id']}")
    except Exception as e:
        print(f"Error al registrar mascota: {e}")



def input_update_mascota(): #Maneja el flujo interactivo para modificar los datos de una mascota existente. Permite al usuario actualizar solo los campos que desee, dejando los demas con su valor original.
    try:
        mid = validate_positive_int(input("ID de la mascota a actualizar: "), "ID")
        m = encontrar_mascota_por_id(mid)
        if not m:
            print("Mascota no encontrada.")
            return
        print("Dejar en blanco para no cambiar el campo.")
        nuevo_nombre = input(f"Nombre [{m['nombre']}]: ") or m['nombre']
        nueva_especie = input(f"Especie [{m['especie']}]: ") or m['especie']
        nueva_raza = input(f"Raza [{m['raza']}]: ") or m['raza']
        nueva_edad_str = input(f"Edad [{m['edad']}]: ") #Valor de entrada original (string)
        nueva_edad = m['edad'] if nueva_edad_str.strip() == "" else validate_positive_int(nueva_edad_str, "Edad") #Valor procesado, validad y convertido a nro entero (int)
        nuevo_rut_str = input(f"RUT dueño [{m['rut_dueño']}]: ")
        nuevo_rut = m['rut_dueño'] if nuevo_rut_str.strip() == "" else validate_rut(nuevo_rut_str)


        updated = update_mascota(mid, nombre=nuevo_nombre, especie=nueva_especie, raza=nueva_raza, edad=nueva_edad, rut_dueño=nuevo_rut)
        print("Mascota actualizada:")
        print(updated)
    except Exception as e:
        print(f"Error al actualizar mascota: {e}")



def input_delete_mascota(): #Maneja el flujo interactivo para eliminar una mascota especifica, incluyendo un paso de confirmación de seguridad
    try:
        mid = validate_positive_int(input("ID de la mascota a eliminar: "), "ID")
        confirm = input("¿Confirma eliminación? (S/N): ").strip().lower()
        if confirm != 's':
            print("Eliminación cancelada.")
            return
        delete_mascota(mid)
        print("Mascota eliminada (y atenciones relacionadas).")
    except Exception as e:
        print(f"Error al eliminar mascota: {e}")



def input_registrar_atencion(): #Función para registrar una nueva atención veterinaria
    try:
        mid = validate_positive_int(input("ID de la mascota: "), "ID")
        fecha = validar_fecha(input("Fecha (AAAA-MM-DD): "))
        descripcion = input("Descripción: ")
        costo = validate_positive_float(input("Costo: "), "Costo")
        vet = input("Veterinario: ")
        at = validar_fecha(mid, fecha, descripcion, costo, vet)
        print(f"Atención registrada con ID {at['id']}")
    except Exception as e:
        print(f"Error al registrar atención: {e}")



def input_lista_atenciones(): #Permite al usuario consultar el historial de atenciones médicas para una mascota especifica.
    try:
        mid = validate_positive_int(input("ID de la mascota: "), "ID")
        lista_atenciones_por_mascota(mid)
    except Exception as e:
        print(f"Error: {e}")



def input_reporte_gasto(): #Esta funciión maneja la solicitud de un informe de gastos por dueño
    try:
        rut = validar_rut(input("RUT dueño (ej: 12345678-9): "))
        gasto_por_rut(rut)
    except Exception as e:
        print(f"Error al generar reporte: {e}")



def input_exportar(): #Permite al usuario guardar el estado actual de las listas en archivos formato CSV
    try:
        exportar_a_csv()
    except Exception as e:
        print(f"Error al exportar: {e}")



def input_importar(): #Permite al usuario cargar datos previamente guardados desde archivos CSV a las colecciones globales del programa.
    try:
        importar_de_csv()
    except Exception as e:
        print(f"Error al importar: {e}")



#--- ENTRADA ---
def main(): #Esta función es el punto de entrada del programa, su proposito es inicializar el sistema, manejar el ciclo de la aplicación (menú) y dirigir el flujo de ejecución.
    print("Bienvenido a Veterinaria PETCARE - Sistema de Gestión (Consola)")
    # Intentar cargar datos si existen
    importar_de_csv() #Lla a la función de importación para intentar cargar automaticamente los datos de mascotas y atenciones que hayan sido guardados en archivos CSV durante una sesión anterior.
    while True: #Inicia un bucle infinito
        mostrar_menu() #Llama a la función que imprime todas las opciones disponibles en la consola
        opcion = input("Seleccione una opción: ").strip() #Lee la entrada del usuario y limpia de espacios con ".strip"
        if opcion == '1':
            input_mascota_interactivo()
        elif opcion == '2':
            input_update_mascota()
        elif opcion == '3':
            input_delete_mascota()
        elif opcion == '4':
            list_mascotas()
        elif opcion == '5':
            input_registrar_atencion()
        elif opcion == '6':
            input_lista_atenciones()
        elif opcion == '7':
            input_reporte_gasto()
        elif opcion == '8':
            input_exportar()
        elif opcion == '9':
            input_importar()
        elif opcion == '0':
            print("Saliendo. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intente nuevamente.")



if __name__ == "__main__": #Asegura que la función main() solo se ejecute si el script es iniciado directamente por el usuario
    main() 
