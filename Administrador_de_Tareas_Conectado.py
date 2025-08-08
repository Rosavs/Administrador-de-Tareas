import sqlite3

# Conexión y cursor globales
conn = sqlite3.connect("tareas.db")
cursor = conn.cursor()

# Crear tablas si no existen
cursor.execute('''
CREATE TABLE IF NOT EXISTS organizadores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    max_tareas INTEGER NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS tareas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descripcion TEXT NOT NULL,
    estado TEXT NOT NULL,
    organizador_id INTEGER,
    FOREIGN KEY (organizador_id) REFERENCES organizadores(id)
)
''')

conn.commit()

def crear_organizador():
    while True:
        nombre = input("Elige un nombre para el organizador: ").strip()
        max_tareas = input("Elige un número máximo de tareas (de 1 a 10): ").strip()

        if not max_tareas.isdigit():
            print("Sólo números permitidos para el número máximo de tareas.")
            continue

        max_tareas = int(max_tareas)
        if max_tareas < 1 or max_tareas > 10:
            print("Número fuera de rango, debe ser entre 1 y 10.")
            continue

        cursor.execute("INSERT INTO organizadores (nombre, max_tareas) VALUES (?, ?)", (nombre, max_tareas))
        conn.commit()

        cursor.execute("SELECT id, nombre, max_tareas FROM organizadores WHERE nombre = ? ORDER BY id DESC LIMIT 1", (nombre,))
        organizador = cursor.fetchone()  # (id, nombre, max_tareas)

        print(f"Organizador número {organizador[0]}: {organizador[1]} creado.")
        return organizador

def listar_organizadores():
    cursor.execute("SELECT id, nombre FROM organizadores ORDER BY id")
    return cursor.fetchall()

def elegir_organizador():
    while True:
        organizadores = listar_organizadores()
        if organizadores:
            print("\nOrganizadores existentes:")
            for o in organizadores:
                print(f"Organizador número {o[0]}: {o[1]}")
            print("\nElige el número de organizador de los existentes")
            print("o escribe N para crear uno nuevo.\n")

            eleccion = input("Tu elección: ").strip()
            if eleccion.lower() == 'n':
                return crear_organizador()
            elif eleccion.isdigit():
                org_id = int(eleccion)
                cursor.execute("SELECT id, nombre, max_tareas FROM organizadores WHERE id = ?", (org_id,))
                organizador = cursor.fetchone()
                if organizador:
                    print(f"Has elegido el organizador número {organizador[0]}: {organizador[1]}")
                    return organizador
                else:
                    print("No existe un organizador con ese número. Inténtalo de nuevo.")
            else:
                print("Opción no válida. Inténtalo de nuevo.")
        else:
            print("No hay organizadores. Crea uno nuevo.")
            return crear_organizador()

def añadir_tarea(org_id, max_tareas):
    cursor.execute("SELECT COUNT(*) FROM tareas WHERE organizador_id = ?", (org_id,))
    total = cursor.fetchone()[0]
    if total >= max_tareas:
        print(f"No puedes añadir más tareas, límite de {max_tareas} alcanzado.")
        return

    descripcion = input("Descripción de la nueva tarea: ").strip()
    if descripcion:
        cursor.execute("INSERT INTO tareas (descripcion, estado, organizador_id) VALUES (?, ?, ?)", (descripcion, "pendiente", org_id))
        conn.commit()
        print("Tarea añadida.")
    else:
        print("Descripción vacía, tarea no añadida.")

def listar_tareas(org_id):
    cursor.execute("SELECT id, descripcion, estado FROM tareas WHERE organizador_id = ?", (org_id,))
    tareas = cursor.fetchall()
    if not tareas:
        print("No hay tareas para este organizador.")
        return
    print("\n-NÚMERO-  -TAREA (ESTADO)-")
    for idx, (tid, desc, estado) in enumerate(tareas, start=1):
        print(f"{idx}         {desc} ({estado})")

def eliminar_tarea(org_id):
    cursor.execute("SELECT id FROM tareas WHERE organizador_id = ?", (org_id,))
    tareas = cursor.fetchall()
    if not tareas:
        print("No hay tareas para eliminar.")
        return

    listar_tareas(org_id)
    num = input("Número de tarea a eliminar: ").strip()
    if not num.isdigit():
        print("Debes ingresar un número válido.")
        return

    num = int(num)
    cursor.execute("SELECT id FROM tareas WHERE organizador_id = ? ORDER BY id", (org_id,))
    tareas_ids = [t[0] for t in cursor.fetchall()]
    if 1 <= num <= len(tareas_ids):
        tid = tareas_ids[num -1]
        cursor.execute("DELETE FROM tareas WHERE id = ?", (tid,))
        conn.commit()
        print("Tarea eliminada.")
    else:
        print("No vale, número erróneo.")

def completar_tarea(org_id):
    cursor.execute("SELECT id, estado FROM tareas WHERE organizador_id = ?", (org_id,))
    tareas = cursor.fetchall()
    if not tareas:
        print("No hay tareas para completar.")
        return

    listar_tareas(org_id)
    num = input("Número de tarea a completar: ").strip()
    if not num.isdigit():
        print("No vale, número erróneo.")
        return

    num = int(num)
    cursor.execute("SELECT id, estado FROM tareas WHERE organizador_id = ? ORDER BY id", (org_id,))
    tareas_ordenadas = cursor.fetchall()
    if 1 <= num <= len(tareas_ordenadas):
        tid, estado = tareas_ordenadas[num-1]
        if estado == "completo":
            print("La tarea ya estaba completada.")
        else:
            cursor.execute("UPDATE tareas SET estado = ? WHERE id = ?", ("completo", tid))
            conn.commit()
            print("Tarea marcada como completada.")
    else:
        print("No vale, número erróneo.")

def menu(org):
    org_id, nombre, max_tareas = org
    while True:
        print(f"\n--- Organizador de tareas: {nombre} ---")
        print("Opciones:")
        print("A - Añadir tarea")
        print("C - Completar tarea")
        print("L - Listar tareas")
        print("E - Eliminar tarea")
        print("S - Salir")
        opcion = input("Elige una opción: ").strip().lower()

        if opcion == 'a':
            añadir_tarea(org_id, max_tareas)
        elif opcion == 'c':
            completar_tarea(org_id)
        elif opcion == 'l':
            listar_tareas(org_id)
        elif opcion == 'e':
            eliminar_tarea(org_id)
        elif opcion == 's':
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida, inténtalo de nuevo.")

if __name__ == "__main__":
    organizador = elegir_organizador()
    menu(organizador)
    conn.close()
