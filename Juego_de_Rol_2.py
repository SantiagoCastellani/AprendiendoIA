import random
import time
import os

def limpiar_pantalla():
    """Limpia la consola para mejorar la presentación del juego."""
    os.system('cls' if os.name == 'nt' else 'clear')

class Entidad:
    """Clase base para cualquier ser en el juego."""
    def __init__(self, nombre, hp, ataque, defensa=0):
        self.nombre = nombre
        self.hp = hp
        self.hp_max = hp
        self.ataque = ataque
        self.defensa = defensa

    def esta_vivo(self):
        return self.hp > 0

    def recibir_dano(self, dano):
        """Calcula y aplica el daño considerando la defensa."""
        dano_real = max(0, dano - self.defensa)
        self.hp -= dano_real
        if self.hp < 0:
            self.hp = 0
        return dano_real

class Personaje(Entidad):
    """Clase para el jugador principal, con inventario y magia."""
    def __init__(self, nombre):
        super().__init__(nombre, hp=150, ataque=20, defensa=5)
        self.mp = 50
        self.mp_max = 50
        self.oro = 50
        self.nivel = 1
        self.xp = 0
        self.inventario = {"Pocion de Vida": 3, "Pocion de Mana": 1}
        self.arma_equipada = "Espada de Madera"

    def mostrar_estado(self):
        print("="*40)
        print(f"🦸 {self.nombre} - Nivel {self.nivel}")
        print(f"❤️ HP: {self.hp}/{self.hp_max} | 💧 MP: {self.mp}/{self.mp_max}")
        print(f"⚔️ Ataque: {self.ataque} | 🛡️ Defensa: {self.defensa}")
        print(f"💰 Oro: {self.oro} | ⭐ XP: {self.xp}/{self.nivel*100}")
        print(f"🗡️ Arma: {self.arma_equipada}")
        print("="*40)

    def usar_objeto(self):
        """Permite al jugador consumir objetos curativos."""
        objetos_disponibles = [k for k, v in self.inventario.items() if v > 0]
        if not objetos_disponibles:
            print("Tu inventario está vacío.")
            return False

        print("Inventario:")
        for i, obj in enumerate(objetos_disponibles):
            print(f"{i + 1}. {obj} (x{self.inventario[obj]})")
        print("0. Cancelar")
        
        try:
            opcion = int(input("Elige un objeto a usar: "))
            if opcion == 0:
                return False
            
            obj_seleccionado = objetos_disponibles[opcion - 1]
            if obj_seleccionado == "Pocion de Vida":
                curacion = 50
                self.hp = min(self.hp + curacion, self.hp_max)
                self.inventario[obj_seleccionado] -= 1
                print(f"Te curas {curacion} HP. Tienes {self.hp}/{self.hp_max} HP.")
                return True
            elif obj_seleccionado == "Pocion de Mana":
                recuperacion = 30
                self.mp = min(self.mp + recuperacion, self.mp_max)
                self.inventario[obj_seleccionado] -= 1
                print(f"Recuperas {recuperacion} MP. Tienes {self.mp}/{self.mp_max} MP.")
                return True
        except (ValueError, IndexError):
            print("Opción inválida.")
            return False

    def atacar_basico(self, objetivo):
        """Ataque estándar con algo de aleatoriedad."""
        dano = int(self.ataque * random.uniform(0.8, 1.2))
        dano_real = objetivo.recibir_dano(dano)
        print(f"⚔️ {self.nombre} ataca a {objetivo.nombre} causando {dano_real} de daño.")

    def lanzar_hechizo(self, objetivo):
        """Permite elegir entre diferentes habilidades mágicas."""
        hechizos = [
            ("Bola de Fuego", 15, 2.5),  # (Nombre, Costo MP, Multiplicador Daño)
            ("Rayo de Hielo", 25, 3.5),
            ("Curación Menor", 20, 0)
        ]
        print("\n--- Magias Disponibles ---")
        for i, (nombre, costo, mult) in enumerate(hechizos):
            print(f"{i + 1}. {nombre} ({costo} MP)")
        print("0. Cancelar")

        try:
            opcion = int(input("Elige un hechizo: "))
            if opcion == 0:
                return False

            hechizo = hechizos[opcion - 1]
            nombre_hechizo, costo_mp, mult_dano = hechizo

            if self.mp < costo_mp:
                print("¡No tienes suficiente maná!")
                return False

            self.mp -= costo_mp

            if nombre_hechizo == "Curación Menor":
                curacion = int(self.hp_max * 0.4)
                self.hp = min(self.hp + curacion, self.hp_max)
                print(f"✨ Lanzas Curación Menor y recuperas {curacion} HP.")
            else:
                dano_magico = int(self.ataque * mult_dano * random.uniform(0.9, 1.1))
                dano_real = objetivo.recibir_dano(dano_magico)
                print(f"🔥 Lanzas {nombre_hechizo} contra {objetivo.nombre} causando {dano_real} de daño mágico!")
            return True

        except (ValueError, IndexError):
            print("Opción inválida.")
            return False

    def ganar_recompensas(self, xp, oro):
        self.xp += xp
        self.oro += oro
        print(f"Obtienes {xp} XP y {oro} monedas de oro.")
        
        while self.xp >= self.nivel * 100:
            self.xp -= self.nivel * 100
            self.subir_nivel()

    def subir_nivel(self):
        self.nivel += 1
        self.hp_max += 25
        self.hp = self.hp_max
        self.mp_max += 15
        self.mp = self.mp_max
        self.ataque += 5
        self.defensa += 2
        print(f"\n🆙 ¡Felicidades! {self.nombre} ha subido al nivel {self.nivel}.")

class Enemigo(Entidad):
    """Clase para los monstruos, cuyos atributos escalan con el nivel del jugador."""
    def __init__(self, nivel_jugador):
        tipos = [
            ("Lobo Feroz", 0.8, 0.8),
            ("Bandido", 1.0, 1.0),
            ("Esqueleto", 0.9, 1.1),
            ("Orco Guerrero", 1.5, 1.2),
            ("Tigre Dientes de Sable", 1.2, 1.5)
        ]
        nombre, mod_hp, mod_atk = random.choice(tipos)
        
        hp_base = int(40 * nivel_jugador * mod_hp)
        atk_base = int(12 * nivel_jugador * mod_atk)
        defensa = int(nivel_jugador * 2)

        super().__init__(nombre, hp_base, atk_base, defensa)
        self.recompensa_xp = int(45 * nivel_jugador * mod_hp)
        self.recompensa_oro = int(20 * nivel_jugador * random.uniform(0.8, 1.5))

    def actuar(self, objetivo):
        """IA básica del enemigo."""
        dano = int(self.ataque * random.uniform(0.8, 1.2))
        dano_real = objetivo.recibir_dano(dano)
        print(f"👹 {self.nombre} ataca causando {dano_real} de daño.")

class Tienda:
    """Clase para vender mejoras al jugador."""
    def __init__(self):
        self.objetos = {
            "Pocion de Vida": 20,
            "Pocion de Mana": 25,
            "Espada de Hierro": 100,
            "Escudo de Roble": 80
        }

    def visitar(self, jugador):
        while True:
            limpiar_pantalla()
            print("⛺ --- MERCADER VIAJERO ---")
            print(f"Tu oro: {jugador.oro}")
            print("\nArtículos a la venta:")
            
            items = list(self.objetos.items())
            for i, (nombre, precio) in enumerate(items):
                print(f"{i + 1}. {nombre} - {precio} oro")
            print("0. Salir de la tienda")
            
            try:
                opcion = int(input("\n¿Qué deseas comprar?: "))
                if opcion == 0:
                    print("¡Vuelve pronto!")
                    break
                
                nombre_item, precio = items[opcion - 1]
                if jugador.oro >= precio:
                    jugador.oro -= precio
                    if "Espada" in nombre_item:
                        jugador.ataque += 15
                        jugador.arma_equipada = nombre_item
                        print(f"¡Has equipado {nombre_item}! Ataque +15")
                        del self.objetos[nombre_item] # Solo se puede comprar una vez
                    elif "Escudo" in nombre_item:
                        jugador.defensa += 10
                        print(f"¡Has mejorado tu defensa con {nombre_item}! Defensa +10")
                        del self.objetos[nombre_item] # Solo se puede comprar una vez
                    else:
                        jugador.inventario[nombre_item] = jugador.inventario.get(nombre_item, 0) + 1
                        print(f"Has comprado {nombre_item}.")
                else:
                    print("No tienes suficiente oro.")
                time.sleep(1.5)
            except (ValueError, IndexError):
                print("Opción inválida.")
                time.sleep(1)

def turno_combate(jugador, enemigo):
    """Maneja el flujo principal de un combate."""
    print(f"\n⚠️ ¡Un {enemigo.nombre} salvaje ha aparecido!")
    time.sleep(1)
    
    while jugador.esta_vivo() and enemigo.esta_vivo():
        limpiar_pantalla()
        jugador.mostrar_estado()
        print(f"👹 {enemigo.nombre} - ❤️ HP: {enemigo.hp}/{enemigo.hp_max}")
        
        print("\n¿Qué deseas hacer?")
        print("1. Atacar ⚔️")
        print("2. Magia ✨")
        print("3. Objetos 🎒")
        print("4. Huir 🏃")
        
        accion = input("Elige tu acción: ")
        
        turno_jugador_completado = False
        if accion == '1':
            jugador.atacar_basico(enemigo)
            turno_jugador_completado = True
        elif accion == '2':
            turno_jugador_completado = jugador.lanzar_hechizo(enemigo)
        elif accion == '3':
            turno_jugador_completado = jugador.usar_objeto()
        elif accion == '4':
            if random.random() > 0.4:
                print("💨 ¡Has escapado con éxito!")
                return True # Sobrevive pero no gana recompensas
            else:
                print("❌ ¡No pudiste escapar!")
                turno_jugador_completado = True
        else:
            print("Acción no reconocida.")
            
        if not turno_jugador_completado:
            time.sleep(1)
            continue
            
        time.sleep(1.5)
        
        if enemigo.esta_vivo():
            enemigo.actuar(jugador)
            time.sleep(1.5)

    if jugador.esta_vivo():
        print(f"\n🏆 ¡Has derrotado a {enemigo.nombre}!")
        jugador.ganar_recompensas(enemigo.recompensa_xp, enemigo.recompensa_oro)
        return True
    else:
        return False

def juego_principal():
    limpiar_pantalla()
    print("="*50)
    print("🗡️  CRÓNICAS DEL REINO OSCURO (RPG AVANZADO)  🛡️")
    print("="*50)
    
    nombre_jugador = input("\nIngresa el nombre de tu campeón: ")
    if not nombre_jugador.strip():
        nombre_jugador = "Caballero sin nombre"
        
    jugador = Personaje(nombre_jugador)
    tienda = Tienda()
    combates_ganados = 0
    
    print(f"\n¡El viaje comienza, {jugador.nombre}! Te adentras en tierras peligrosas.")
    time.sleep(2)
    
    while jugador.esta_vivo():
        limpiar_pantalla()
        print("\nExplorando el mapa...")
        time.sleep(1)
        
        evento = random.random()
        
        if evento < 0.2 and combates_ganados > 0: # 20% probabilidad de tienda
            tienda.visitar(jugador)
        elif evento < 0.3: # 10% probabilidad de encontrar objeto
            print("✨ ¡Has encontrado una Pocion de Vida en el camino!")
            jugador.inventario["Pocion de Vida"] = jugador.inventario.get("Pocion de Vida", 0) + 1
            time.sleep(2)
        else:
            enemigo_actual = Enemigo(jugador.nivel)
            sobrevive = turno_combate(jugador, enemigo_actual)
            
            if not sobrevive:
                break
                
            if enemigo_actual.hp <= 0:
                combates_ganados += 1
                
            print("\n¿Deseas seguir explorando o acampar?")
            print("1. Continuar el viaje")
            print("2. Acampar y descansar (Recupera HP/MP, pero atrae peligros)")
            print("3. Retirarse del juego")
            
            opcion = input("Opción: ")
            if opcion == '2':
                print("🏕️ Armas un campamento y descansas...")
                jugador.hp = min(jugador.hp + 30, jugador.hp_max)
                jugador.mp = min(jugador.mp + 20, jugador.mp_max)
                time.sleep(1)
                if random.random() < 0.3: # 30% de que te ataquen durmiendo
                    print("⚠️ ¡Te han emboscado mientras dormías!")
                    time.sleep(1)
                    turno_combate(jugador, Enemigo(jugador.nivel))
            elif opcion == '3':
                print("\nDecides retirarte a un lugar seguro. Fin del viaje por ahora.")
                break

    print("\n" + "="*50)
    print("💀  FIN DE LA PARTIDA  💀" if not jugador.esta_vivo() else "🏁  FIN DEL JUEGO  🏁")
    print("="*50)
    print(f"Héroe: {jugador.nombre} (Nivel {jugador.nivel})")
    print(f"Combates ganados: {combates_ganados}")
    print(f"Oro recolectado: {jugador.oro}")
    print("¡Gracias por jugar!")

if __name__ == "__main__":
    juego_principal()
