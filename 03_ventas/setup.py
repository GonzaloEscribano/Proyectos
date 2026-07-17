import sqlite3

def crear_tablas(conn):
    # creamos, si no existen, las tablas Productos, Ventas y Detalle_Ventas
    conn.executescript('''CREATE TABLE IF NOT EXISTS Productos(
        id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        costo REAL,
        precio REAL,
        ganancia REAL,
        info_extra TEXT
        );
        CREATE TABLE IF NOT EXISTS Ventas(
        id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_cliente TEXT NOT NULL,
        monto_total REAL NOT NULL,
        fecha TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS Detalle_Ventas(
        id_detalle_venta INTEGER PRIMARY KEY AUTOINCREMENT,
        id_producto INTEGER,
        cantidad_producto INTEGER NOT NULL,
        id_venta INTEGER,
        FOREIGN KEY (id_producto) REFERENCES Productos(id_producto),
        FOREIGN KEY (id_venta) REFERENCES Ventas(id_venta)
        )''')   
    
def añadir_producto(conn):
    try:    
        consulta = '''INSERT OR IGNORE INTO Productos (nombre, costo, precio, ganancia, info_extra) VALUES (?, ?, ?, ?, ?)'''
        
        nombre = input("Nombre del producto: ")
        costo = float(input("Ingrese el costo: "))
        precio = float(input("Ingrese el precio de venta: "))
        ganancia = precio - costo
        info = input("Ingrese información sobre el producto: ")
        
        # ejecutamos la consulta
        conn.execute(consulta, (nombre, costo, precio, ganancia, info))
        
        # guardamos los datos
        conn.commit()
        print(f"Producto {nombre} agregado con éxito.")
    
    except ValueError:
        print("ERROR: agregar números válidos para precio y costo")
    
    except Exception as e:
        print(f"Ocurrió un error con la base de datos: {e}")

def recorrer_productos(conn):
    consulta = '''SELECT id_producto, nombre, info_extra FROM Productos
                WHERE nombre LIKE ?'''            
    nombre = input("Ingrese el nombre del producto: ")
    
    datos = conn.execute(consulta, (f"%{nombre}%",))
    productos = datos.fetchall()
    print("Productos relacionados a la búsqueda:")
    for id_producto, nombre, info in productos:
        print(f"ID: {id_producto} | Nombre: {nombre} | Info: {info}")
        
    id_producto_elegido = int(input("Ingrese el ID del producto: "))
    
    return id_producto_elegido
    
def modificar_precio(conn):
    id_producto_elegido = recorrer_productos(conn)
    
    consulta2 = '''UPDATE Productos
                    SET costo = ?, precio = ?, ganancia = ?
                    WHERE id_producto = ?'''
    costo_nuevo = float(input("Ingrese el nuevo costo: "))
    precio_nuevo =  float(input("Ingrese el nuevo precio de venta: "))
    nueva_ganancia = precio_nuevo - costo_nuevo
    
    conn.execute(consulta2, (costo_nuevo, precio_nuevo, nueva_ganancia, id_producto_elegido))
    conn.commit()
    print("Precios actualizados.")
    
def eliminar_producto(conn):
    id_producto_elegido = recorrer_productos(conn)
    
    consulta = '''DELETE FROM Productos
                WHERE id_producto = ?'''
    
    conn.execute(consulta, (id_producto_elegido,))
    conn.commit()
    
    print("Producto eliminado.")

with sqlite3.connect("base_de_datos.db") as conn:
    # Activamos claves foráneas por buena práctica
    conn.execute("PRAGMA foreign_keys = ON")
    
    print("------------- BIENVENIDO AL SETUP -------------")
    while True:
        print()
        print('''OPCIONES:\n1. Crear Tablas\n2. Añadir Producto\n3. Modificar Precio\n4. Eliminar Producto\n5. Salir''')
        opcion = input("Elija una opción (1-5): ")
        print()
        if opcion == "1":
            crear_tablas(conn)
            print("Tablas creadas con éxito.")
        elif opcion == "2":
            añadir_producto(conn)
        elif opcion == "3":
            modificar_precio(conn)
        elif opcion == "4":
            eliminar_producto(conn)
        elif opcion == "5":
            break
        else:
            print("Entrada no válida")