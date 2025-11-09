import csv
import os
import re
from datetime import datetime


mascotas = []
atenciones = []

sig_mascota_id = 1
sig_atencion_id = 1

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

def validar_fecha(date_str: str): #
    try:
        fecha= datetime.strptime(date_str, "%Y-%m-%d")
        return fecha.strftime("%Y-%m-%d")
    except ValueError:
        raise ValueError("Fecha inválida. Formato esperado AAAA-MM-DD")

