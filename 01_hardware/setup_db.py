import sqlite3

def crear_categorias_base(conn):
    conn.executescript('''
    INSERT OR IGNORE INTO Categorias (nombre) VALUES ('Procesador'), ('Placa Madre'), ('Placa de Video'), ('Fuente'), ('Memoria RAM'), ('Almacenamiento')
''')

def insertar_componentes(conn):
    conn.executescript('''
    INSERT OR IGNORE INTO Componentes (nombre, precio, especificacion_clave, id_categoria) VALUES 
    ('Intel Core Ultra 5 225F 4.9Ghz Turbo', 266000, 'LGA1851', 1),
    ('ASUS Prime B860M-K', 189300, 'LGA1851 DDR5', 2),
    ('Corsair 16GB 6000Mhz Vengeance', 386550, 'DDR5', 5),
    ('MSI GeForce RTX 5060 8GB', 620410, 'OC', 3),
    ('Corsair RM750e', 175000, 'Cybenetics Platinum Full Modular', 4),
    ('AMD Ryzen 7 5700 4.6Ghz Turbo', 226700, 'AM4', 1),
    ('Gigabyte A520M-K V2', 84300, 'DDR4 AM4', 2),
    ('Patriot Viper 8GB 3200Mhz Steel', 119550, 'DDR4', 5);
''')

def rellenar_tablas(conn):
    crear_categorias_base(conn)
    insertar_componentes(conn)

def crear_tablas():
    # creamos las tablas
    with sqlite3.connect("hardware.db") as conn:
        conn.executescript('''
        CREATE TABLE IF NOT EXISTS Categorias (
        id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE
    );
        CREATE TABLE IF NOT EXISTS Componentes(
        id_componente INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE,
        precio REAL,
        especificacion_clave TEXT NOT NULL,
        id_categoria INTEGER,
        FOREIGN KEY (id_categoria) REFERENCES Categorias (id_categoria)
    );
        CREATE TABLE IF NOT EXISTS Presupuestos(
        id_presupuesto INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo_armado TEXT NOT NULL UNIQUE,
        fecha TEXT NOT NULL,
        precio_total REAL
    );
        CREATE TABLE IF NOT EXISTS Presupuesto_Detalle(
        id_presupuesto_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
        id_presupuesto INTEGER,
        id_componente INTEGER,
        FOREIGN KEY (id_presupuesto) REFERENCES Presupuestos (id_presupuesto),
        FOREIGN KEY (id_componente) REFERENCES Componentes (id_componente)
    );''')
        rellenar_tablas(conn)

if __name__ == "__main__":
    crear_tablas()