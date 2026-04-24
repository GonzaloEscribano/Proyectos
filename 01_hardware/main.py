import sqlite3
import datetime as dt

def calcular_monto(conn, id_presupuesto_actual):
    consulta = '''SELECT SUM(Componentes.precio) FROM Componentes
                JOIN Presupuesto_Detalle
                ON Presupuesto_Detalle.id_componente = Componentes.id_componente
                WHERE Presupuesto_Detalle.id_presupuesto = ?'''
    dato = conn.execute(consulta, (id_presupuesto_actual,))
    total_acumulado = dato.fetchone()[0]
    
    consulta = '''UPDATE Presupuestos 
                SET precio_total = ?
                WHERE id_presupuesto = ?'''
    conn.execute(consulta, (total_acumulado, id_presupuesto_actual))
    print(f"\n¡El armado fue guardado con éxito! El precio total es: ${total_acumulado}")

def guardar_componente_elegido(conn, id_presupuesto_actual, id_componente):
    consulta = '''INSERT INTO Presupuesto_Detalle (id_presupuesto, id_componente) VALUES (?, ?)'''
    conn.execute(consulta, (id_presupuesto_actual, id_componente))

def elegir_componente(componentes):
    datos = componentes.fetchall()
    for id_componente, nombre, precio in datos:
        print(f"ID: {id_componente} | Nombre: {nombre} | Precio: {precio}")
    print()
    return int(input("Ingrese el ID del componente que elija: "))

def recorrer_rams(conn, tipo_ram, id_presupuesto_actual):
    consulta = '''SELECT id_componente, nombre, precio FROM Componentes
                WHERE id_categoria = 5 AND especificacion_clave LIKE ?'''
    componentes = conn.execute(consulta, (f"%{tipo_ram}%",))
    
    id_ram_elegida = elegir_componente(componentes)
    
    guardar_componente_elegido(conn, id_presupuesto_actual, id_ram_elegida)
    calcular_monto(conn, id_presupuesto_actual)

def recorrer_mothers(conn, socket_procesador, id_presupuesto_actual):
    consulta = '''SELECT id_componente, nombre, precio FROM Componentes 
                WHERE id_categoria = 2 AND especificacion_clave LIKE ?'''
    componentes = conn.execute(consulta, (f"%{socket_procesador}%",))    # % para que busque esa variable aunque tenga algo delante o atrás
    
    id_mother_elegida = elegir_componente(componentes)
    
    consulta_ddr = '''SELECT especificacion_clave FROM Componentes WHERE id_componente = ?'''
    datos_mother = conn.execute(consulta_ddr, (id_mother_elegida,))
    resultado_ddr = datos_mother.fetchone()
    ddr_mother = resultado_ddr[0]
    
    if "DDR5" in ddr_mother:
        tipo_ram = "DDR5"
    else:
        tipo_ram = "DDR4"
        
    guardar_componente_elegido(conn, id_presupuesto_actual, id_mother_elegida)
    recorrer_rams(conn, tipo_ram, id_presupuesto_actual)

def recorrer_procesadores(conn, id_presupuesto_actual):
    consulta = '''SELECT id_componente, nombre, precio FROM Componentes
                WHERE id_categoria = 1'''
    componentes = conn.execute(consulta)
    
    id_procesador_elegido = elegir_componente(componentes)
    
    consulta_socket = '''SELECT especificacion_clave FROM Componentes WHERE id_componente = ?'''
    datos_procesador = conn.execute(consulta_socket, (id_procesador_elegido,))
    resultado_socket = datos_procesador.fetchone()
    socket_procesador = resultado_socket[0]
    
    guardar_componente_elegido(conn, id_presupuesto_actual, id_procesador_elegido)
    recorrer_mothers(conn, socket_procesador, id_presupuesto_actual)

def armar_presupuesto(conn):
    nombre_presupuesto = input("Ingrese el nombre para su presupuesto: ")
    fecha = dt.date.today().isoformat()
    # Usamos ? como comodines
    consulta = '''INSERT INTO Presupuestos (titulo_armado, fecha, precio_total) VALUES (?, ?, 0)'''
    # Ejecutamos pasando la consulta y luego las variables en orden
    cursor = conn.execute(consulta, (nombre_presupuesto, fecha))
    id_presupuesto_actual = cursor.lastrowid
    recorrer_procesadores(conn, id_presupuesto_actual)
    
def menu():
    with sqlite3.connect("hardware.db") as conn:
        print(f"------------ BIENVENIDO AL MENÚ ------------")
        while True:
            eleccion = int(input("Seleccione una opción (1.Ver Catálogo Completo / 2.Armar Presupuesto / 3.Salir): "))
            if eleccion == 1:
                cursor = conn.execute('''
                SELECT Componentes.nombre, Componentes.precio, Categorias.nombre 
                FROM Componentes 
                JOIN Categorias ON Componentes.id_categoria = Categorias.id_categoria
                ''')
                datos = cursor.fetchall()
                for nombre, precio, categoria in datos:
                        print(f"[{categoria}] {nombre} - Precio: ${precio}")
                print()
            elif eleccion == 2:
                armar_presupuesto(conn)
                print()
            elif eleccion == 3:
                break
            else:
                print("Opción no válida")
                print()

if __name__ == "__main__":
    menu()