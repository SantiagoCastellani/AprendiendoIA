"""
GUÍA COMPLETA DE SINTAXIS EN PYTHON (NIVEL INICIAL - INTERMEDIO - AVANZADO)
Este archivo cubre desde lo más básico hasta características modernas de Python.
Está pensado para ser ejecutado o simplemente leído como referencia.
"""

# ==========================================
# 1. VARIABLES, TIPOS DE DATOS Y TYPE HINTING
# ==========================================
print("--- 1. Variables y Tipos ---")

# Tipos básicos
entero: int = 42
flotante: float = 3.14159
texto: str = "Hola, Inteligencia Artificial"
booleano: bool = True
nulo: None = None

# Type hinting (Python 3.5+)
# No fuerza el tipo en tiempo de ejecución, pero ayuda a editores y linters.
def sumar_numeros(a: int, b: int) -> int:
    return a + b

# ==========================================
# 2. MANEJO DE STRINGS (CADENAS)
# ==========================================
print("\n--- 2. Strings ---")

nombre = "Python"
version = 3.11

# F-strings (La forma moderna y recomendada de formatear texto)
mensaje = f"Aprendiendo {nombre} versión {version}"
print(mensaje)

# Métodos útiles
print(mensaje.upper())           # Mayúsculas
print(mensaje.replace(" ", "_")) # Reemplazar caracteres
print(mensaje.split(" "))        # Dividir en una lista por espacios

# ==========================================
# 3. OPERADORES
# ==========================================
print("\n--- 3. Operadores ---")

# Matemáticos: +, -, *, /, // (división entera), % (módulo), ** (potencia)
print(f"Potencia: 2 ** 3 = {2 ** 3}")
print(f"Módulo (resto): 10 % 3 = {10 % 3}")

# Lógicos: and, or, not
print(f"Lógica: True and False = {True and False}")

# Identidad y Pertenencia: is, is not, in, not in
lista_nums = [1, 2, 3]
print(f"Pertenencia: 2 in lista_nums = {2 in lista_nums}")

# ==========================================
# 4. ESTRUCTURAS DE CONTROL
# ==========================================
print("\n--- 4. Estructuras de Control ---")

edad = 20
if edad < 18:
    print("Menor de edad")
elif edad == 18:
    print("Recién mayor de edad")
else:
    print("Mayor de edad")

# Operador ternario (Condicional en una línea)
estado = "Aprobado" if edad >= 18 else "Rechazado"

# Match-Case (Python 3.10+ - Similar a switch en otros lenguajes)
codigo_error = 404
match codigo_error:
    case 200:
        print("OK")
    case 404:
        print("No encontrado")
    case _:
        print("Error desconocido")

# ==========================================
# 5. COLECCIONES DE DATOS
# ==========================================
print("\n--- 5. Colecciones ---")

# Listas (Mutables, ordenadas)
frutas = ["manzana", "banana", "cereza"]
frutas.append("naranja")
frutas[0] = "kiwi"

# Tuplas (Inmutables, ordenadas)
coordenadas = (10.5, 20.3)
# coordenadas[0] = 15.0 # Esto daría error!

# Sets (Mutables, NO ordenados, elementos únicos)
numeros_unicos = {1, 2, 2, 3, 3, 3, 4}
print(f"Set elimina duplicados: {numeros_unicos}")

# Diccionarios (Pares clave: valor)
usuario = {
    "nombre": "Ana",
    "rol": "Admin",
    "activo": True
}
usuario["edad"] = 28 # Agregar nueva clave
print(f"Usuario: {usuario.get('nombre')}")

# ==========================================
# 6. BUCLES E ITERACIONES
# ==========================================
print("\n--- 6. Bucles ---")

# For con rangos
for i in range(3): # 0, 1, 2
    pass # 'pass' no hace nada, útil para bloques vacíos

# Iterar con índice usando enumerate
for indice, fruta in enumerate(frutas):
    print(f"{indice}: {fruta}")

# Iterar múltiples listas al mismo tiempo usando zip
nombres = ["Alice", "Bob"]
edades = [25, 30]
for n, e in zip(nombres, edades):
    print(f"{n} tiene {e} años")

# While loop
contador = 0
while contador < 2:
    contador += 1
    if contador == 1:
        continue # Salta a la siguiente iteración
    if contador == 5:
        break # Rompe el bucle

# ==========================================
# 7. COMPREHENSIONS (Listas, Diccionarios)
# ==========================================
print("\n--- 7. Comprehensions (Estilo Pythonic) ---")

# Crear listas de forma concisa y eficiente
cuadrados = [x**2 for x in range(5)]
print(f"Cuadrados: {cuadrados}")

# Con condicionales
pares = [x for x in range(10) if x % 2 == 0]
print(f"Pares: {pares}")

# Dictionary comprehension
dict_cuadrados = {x: x**2 for x in range(3)}
print(f"Dict cuadrados: {dict_cuadrados}")

# ==========================================
# 8. FUNCIONES AVANZADAS
# ==========================================
print("\n--- 8. Funciones Avanzadas ---")

# args (tupla de argumentos posicionales) y kwargs (diccionario de argumentos con nombre)
def funcion_flexible(*args, **kwargs):
    print(f"Argumentos posicionales: {args}")
    print(f"Argumentos nombrados: {kwargs}")

funcion_flexible(1, 2, 3, nombre="Juan", modo="oscuro")

# Funciones Lambda (anónimas y de una sola línea)
multiplicar = lambda a, b: a * b
print(f"Lambda: 5 * 4 = {multiplicar(5, 4)}")

# ==========================================
# 9. MANEJO DE ERRORES Y ARCHIVOS
# ==========================================
print("\n--- 9. Errores y Archivos ---")

try:
    resultado = 10 / 0
except ZeroDivisionError as e:
    print(f"Error capturado: No se puede dividir por cero.")
except Exception as e:
    print("Captura cualquier otra excepción")
finally:
    print("Este bloque siempre se ejecuta (ideal para cerrar recursos)")

# Manejo de archivos (Context Managers 'with')
# El bloque 'with' asegura que el archivo se cierre automáticamente al terminar
import os
file_name = "test_file.txt"
with open(file_name, "w", encoding="utf-8") as archivo:
    archivo.write("Escribiendo en un archivo!\n")

with open(file_name, "r", encoding="utf-8") as archivo:
    contenido = archivo.read()
    print(f"Leído del archivo: {contenido.strip()}")

os.remove(file_name) # Limpiamos el archivo de prueba creado

# ==========================================
# 10. PROGRAMACIÓN ORIENTADA A OBJETOS (OOP)
# ==========================================
print("\n--- 10. POO (Clases y Herencia) ---")

class Animal:
    # Atributo de clase (compartido por todas las instancias)
    reino = "Animalia"

    def __init__(self, nombre: str):
        # Atributo de instancia (único para cada objeto)
        self.nombre = nombre

    def hacer_sonido(self):
        raise NotImplementedError("Las subclases deben implementar esto")

# Herencia
class Gato(Animal):
    def hacer_sonido(self):
        return "Miau"

class Perro(Animal):
    def hacer_sonido(self):
        return "Guau"

g = Gato("Michi")
p = Perro("Firulais")
print(f"{g.nombre} dice {g.hacer_sonido()} (Reino: {g.reino})")

# ==========================================
# 11. GENERADORES E ITERADORES
# ==========================================
print("\n--- 11. Generadores ---")

# En lugar de devolver toda la lista a la vez (return), hace 'yield' de un elemento a la vez.
# Ideal para procesar millones de datos sin agotar la memoria RAM.
def generador_fibonacci(limite):
    a, b = 0, 1
    for _ in range(limite):
        yield a
        a, b = b, a + b

print("Fibonacci (primeros 5):", list(generador_fibonacci(5)))

print("\n--- ¡Fin de la guía! ---")
