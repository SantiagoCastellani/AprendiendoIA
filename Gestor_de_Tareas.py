import os

def mostrar_menu():
    """Muestra el menú principal en la consola."""
    print("\n" + "="*35)
    print("📋 MI GESTOR DE TAREAS TERMINAL")
    print("="*35)
    print("1. Ver tareas pendientes")
    print("2. Agregar una nueva tarea")
    print("3. Marcar tarea como completada")
    print("4. Salir")
    print("="*35)

def ver_tareas(tareas):
    """Muestra la lista actual de tareas."""
    if not tareas:
        print("\n✨ ¡No tienes tareas pendientes! Todo al día.")
    else:
        print("\n📌 Tareas pendientes:")
        for i, tarea in enumerate(tareas):
            print(f"  [{i + 1}] {tarea}")

def main():
    # Esta lista guardará nuestras tareas en memoria
    tareas = []
    
    # Limpiamos la pantalla de la consola al iniciar
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Bucle infinito hasta que el usuario decida salir
    while True:
        mostrar_menu()
        opcion = input("Elige una opción (1-4): ")
        
        if opcion == '1':
            # Ver tareas
            ver_tareas(tareas)
            
        elif opcion == '2':
            # Agregar tarea
            nueva_tarea = input("\n📝 Escribe la nueva tarea: ")
            if nueva_tarea.strip(): # Verifica que no sean puros espacios vacíos
                tareas.append(nueva_tarea.strip())
                print(f"✅ Tarea agregada con éxito.")
            else:
                print("❌ La tarea no puede estar vacía.")
                
        elif opcion == '3':
            # Completar tarea
            ver_tareas(tareas)
            if tareas: # Solo pide número si hay tareas en la lista
                try:
                    num_tarea = int(input("\n✅ ¿Qué número de tarea terminaste?: "))
                    # Validamos que el número esté dentro del rango de la lista
                    if 1 <= num_tarea <= len(tareas):
                        tarea_completada = tareas.pop(num_tarea - 1)
                        print(f"🎉 ¡Excelente! Has completado: '{tarea_completada}'")
                    else:
                        print("❌ Número de tarea inválido.")
                except ValueError:
                    print("❌ Por favor, ingresa un número válido (no letras).")
                    
        elif opcion == '4':
            # Salir del bucle y del programa
            print("\n👋 ¡Hasta luego! Sigue siendo productivo.\n")
            break
            
        else:
            # Opción incorrecta
            print("❌ Opción no válida. Intenta de nuevo.")

# Este bloque asegura que main() solo se ejecute si corres el script directamente
if __name__ == "__main__":
    main()
