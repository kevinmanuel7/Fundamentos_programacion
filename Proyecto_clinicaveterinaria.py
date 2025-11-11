import csv
import os
import re
from datetime import datetime


mascotas = []
atenciones = []

cont_mascota_id = 1
cont_atencion_id = 1

DATA_DIR = "data"
MASCOTAS_ARCH = os.path.join(DATA_DIR, "mascotas.csv")
ATENCION_ARCH = os.path.join(DATA_DIR, "atenciones.csv")

def aseg_data_dir():
    if not os.path.exists(DATA_DIR): #Para verificar la ruta de DATA_DIR
        os.makedirs(DATA_DIR) #Si no existe crea el directorio (solo se ejecuta si la condición if es verdadera, es decir, no existe)

def validar_int(value_str, field_name="valor"): #Para convertir una cadena de texto en un número entero
    try:
        val = int(value_str) #Intenta realizar la conversión, si value_str es 123, val será nro entero 123, si es abc, está línea lanzará un error
        return val #Si la conversión es exitosa, la función devuelve el nro entero resultante
    except ValueError: #Si la conversion falla, python captura el error.
        raise ValueError(f"{field_name} debe ser un número entero.") #En lugar de dejar que el programa se detenga con el msje predeterminado de python, la función levanta la excepción con un mensaje personalizado.
    
def validate_positivo_int(value_str, field_name="valor"): #Sirve para asegurar que un valor de entrada sea un nro entero y ademas, positivo o cero (no negativo).
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