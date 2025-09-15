import random
import string

# Listas de nombres y apellidos
nombres = [ "María",  "Ana",  "Laura",  "Sofía", "Adriana", "Camila", "Catalina", "Dayan", "Paula", "Consuelo"]
apellidos = ["Gómez", "Pérez", "Rodríguez", "López", "Martínez", "Fernández", "García", "Ramírez", "Torres", "Castro"]

def generar_identificacion_aleatoria():
    """Genera un número de identificación aleatorio de 8 dígitos."""
    return str(random.randint(10000000, 99999999))

def generar_numero_telefono():
    return str(random.randint(600000000, 699999999))

def generar_correo_aleatorio():
    dominios = ["gmail.com", "hotmail.com", "yahoo.com", "outlook.com"]
    nombre = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"{nombre}@{random.choice(dominios)}"

def generar_nombre_completo():
    """Genera un nombre completo con nombre, primer apellido y segundo apellido por separado."""
    nombre = random.choice(nombres)
    apellido1 = random.choice(apellidos)
    apellido2 = random.choice(apellidos)
    return nombre, apellido1, apellido2