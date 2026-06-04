"""
=============================================================================
🧠 GUÍA DE APRENDIZAJE: JUEGO DE ROL (RPG) EN CONSOLA
=============================================================================
Este programa está diseñado para enseñarte conceptos intermedios de Python
mientras juegas. Al leer este código, presta especial atención a:

1. MÓDULOS: Cómo importar funcionalidades extra de Python (random para azar, 
   time para pausas, os para enviar comandos a la terminal).
2. PROGRAMACIÓN ORIENTADA A OBJETOS (POO): Cómo estructurar código usando 
   'Clases' (Personaje, Jugador, Enemigo) que agrupan datos (atributos como 
   vida y ataque) y comportamiento (métodos como atacar o curarse).
3. HERENCIA: Cómo 'Jugador' y 'Enemigo' heredan (reutilizan) el código de 
   la clase padre 'Personaje' usando super(), ahorrando decenas de líneas.
4. BUCLES PRINCIPALES (Game Loop): Cómo un bucle 'while' principal mantiene 
   el juego funcionando turno tras turno hasta que alguien gana o pierde.
=============================================================================
"""

import random
import os
import time

# ==========================================
# CLASES BASE (POO - Programación Orientada a Objetos)
# ==========================================

class Personaje:
    """Clase base para todos los personajes del juego."""
    def __init__(self, nombre, hp_maximo, ataque):
        self.nombre = nombre
        self.hp_maximo = hp_maximo
        self.hp_actual = hp_maximo
        self.ataque = ataque

    def esta_vivo(self):
        return self.hp_actual > 0

    def recibir_dano(self, dano):
        self.hp_actual -= dano
        if self.hp_actual < 0:
            self.hp_actual = 0

    def atacar(self, objetivo):
        # El daño tiene una variación aleatoria de +/- 20%
        variacion = random.uniform(0.8, 1.2)
        dano_final = int(self.ataque * variacion)
        objetivo.recibir_dano(dano_final)
        print(f"⚔️  {self.nombre} ataca a {objetivo.nombre} causando {dano_final} de daño!")

# Herencia: Jugador hereda de Personaje
class Jugador(Personaje):
    def __init__(self, nombre):
        # Usamos super() para inicializar la clase padre
        super().__init__(nombre, hp_maximo=100, ataque=20)
        self.pociones = 3
        self.nivel = 1
        self.experiencia = 0

    def curarse(self):
        if self.pociones > 0:
            curacion = 35
            self.hp_actual += curacion
            if self.hp_actual > self.hp_maximo:
                self.hp_actual = self.hp_maximo
            self.pociones -= 1
            print(f"🧪 {self.nombre} usa una poción y recupera vida. (HP: {self.hp_actual}/{self.hp_maximo})")
            print(f"   Pociones restantes: {self.pociones}")
        else:
            print("❌ ¡No te quedan pociones!")

    def ganar_experiencia(self, xp):
        self.experiencia += xp
        print(f"🌟 ¡Has ganado {xp} puntos de experiencia!")
        
        # Fórmula para subir de nivel: Nivel * 50 puntos de XP
        if self.experiencia >= self.nivel * 50:
            self.subir_nivel()

    def subir_nivel(self):
        self.nivel += 1
        self.experiencia = 0 # Reiniciamos la XP
        self.hp_maximo += 25  # Más vida máxima
        self.hp_actual = self.hp_maximo # Al subir de nivel te curas al máximo
        self.ataque += 5      # Más ataque
        print(f"\n🆙 ¡NIVEL ARRIBA! {self.nombre} ha alcanzado el nivel {self.nivel}.")
        print(f"   -> HP Máximo: {self.hp_maximo} | Daño Base: {self.ataque}")

# Herencia: Enemigo hereda de Personaje
class Enemigo(Personaje):
    def __init__(self, nivel_jugador):
        nombres = ["Orco Peligroso", "Duende Ladrón", "Lobo Rabioso", "Esqueleto", "Troll"]
        nombre = random.choice(nombres)
        
        # Los stats del enemigo escalan con el nivel del jugador
        hp_enemigo = 30 + (nivel_jugador * 15)
        ataque_enemigo = 8 + (nivel_jugador * 3)
        
        super().__init__(nombre, hp_maximo=hp_enemigo, ataque=ataque_enemigo)
        
        # Cuanto más nivel, más XP da el enemigo
        self.xp_otorgada = 20 + (nivel_jugador * 10)

# ==========================================
# LÓGICA DEL JUEGO
# ==========================================

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_estado(jugador, enemigo):
    print("\n" + "="*45)
    print(f"🦸 {jugador.nombre} (Nvl {jugador.nivel})")
    print(f"❤️ HP: {jugador.hp_actual}/{jugador.hp_maximo}  |  🧪 Pociones: {jugador.pociones}  |  ⭐ XP: {jugador.experiencia}/{jugador.nivel*50}")
    print("-" * 45)
    print(f"👹 {enemigo.nombre}")
    print(f"❤️ HP: {enemigo.hp_actual}/{enemigo.hp_maximo}")
    print("="*45 + "\n")

def turno_combate(jugador, enemigo):
    """Maneja el bucle de un combate contra un enemigo específico."""
    while jugador.esta_vivo() and enemigo.esta_vivo():
        mostrar_estado(jugador, enemigo)
        
        print("¿Qué deseas hacer?")
        print("1. Atacar ⚔️")
        print("2. Usar Poción curativa 🧪")
        print("3. Intentar huir 🏃")
        
        opcion = input("\nElige tu acción (1-3): ")
        limpiar_pantalla()
        
        if opcion == '1':
            jugador.atacar(enemigo)
        elif opcion == '2':
            jugador.curarse()
        elif opcion == '3':
            if random.random() > 0.5: # 50% de probabilidad de escapar
                print("💨 ¡Has escapado con éxito del combate!")
                return False # Falso porque no ganaste, escapaste
            else:
                print("❌ ¡No pudiste escapar! El enemigo te bloquea el paso.")
        else:
            print("❌ Acción inválida. ¡Pierdes el turno por dudar en batalla!")
        
        # Pausamos 1 segundo para poder leer lo que pasó
        time.sleep(1)
        
        # Turno del enemigo (solo ataca si sigue vivo)
        if enemigo.esta_vivo():
            enemigo.atacar(jugador)
            time.sleep(1)
            
    # Al salir del bucle while, evaluamos quién ganó
    if jugador.esta_vivo():
        print(f"\n🏆 ¡Has derrotado a {enemigo.nombre}!")
        jugador.ganar_experiencia(enemigo.xp_otorgada)
        
        # 40% de probabilidad de que el enemigo suelte una poción
        if random.random() > 0.6:
            jugador.pociones += 1
            print("🎁 ¡Encontraste una poción de curación en el suelo!")
        return True # Victoria
    else:
        print(f"\n💀 Has muerto a manos de {enemigo.nombre}...")
        return False # Derrota

def juego_principal():
    limpiar_pantalla()
    print("="*50)
    print("🗡️  AVENTURA RPG EN CONSOLA  🛡️")
    print("="*50)
    
    nombre_jugador = input("¿Cuál es el nombre de tu valiente héroe?: ")
    if not nombre_jugador.strip():
        nombre_jugador = "Caballero sin nombre"
        
    jugador = Jugador(nombre_jugador)
    enemigos_derrotados = 0
    
    print(f"\n¡Bienvenido, {jugador.nombre}! Entrando a la mazmorra oscura...")
    time.sleep(2)
    
    # Bucle principal de la aventura
    while jugador.esta_vivo():
        limpiar_pantalla()
        print("\nCaminando por los pasillos oscuros...")
        time.sleep(1.5)
        
        enemigo_actual = Enemigo(jugador.nivel)
        print(f"\n⚠️  ¡Un {enemigo_actual.nombre} salvaje ha aparecido bloqueando el camino!")
        time.sleep(1.5)
        
        limpiar_pantalla()
        victoria = turno_combate(jugador, enemigo_actual)
        
        # Si el jugador muere, se rompe el bucle
        if not jugador.esta_vivo():
            break
            
        # Si ganó, sumamos al contador
        if victoria:
            enemigos_derrotados += 1
            
        print("\n¿Deseas seguir explorando o salir de la mazmorra a descansar?")
        print("1. Continuar")
        print("2. Retirarse al pueblo")
        opcion_salir = input("Opción (1-2): ")
        
        if opcion_salir == '2':
            print("\n🏠 Te retiras a salvo al pueblo a descansar.")
            break

    # Pantalla final de estadísticas
    print("\n" + "="*50)
    print("🎮  FIN DE LA PARTIDA")
    print("="*50)
    print(f"Héroe: {jugador.nombre} (Nivel {jugador.nivel})")
    print(f"Monstruos derrotados: {enemigos_derrotados}")
    print("¡Gracias por jugar!")

# Punto de entrada del script
if __name__ == "__main__":
    juego_principal()
