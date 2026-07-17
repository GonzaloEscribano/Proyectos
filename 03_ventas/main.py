import sqlite3
import datetime as dt
import matplotlib.pyplot as plt

def guardar_componente_elegido(conn, id_venta, id_producto, unidades):
    consulta = '''INSERT INTO Detalle_Ventas (id_venta, id_producto, cantidad_producto) VALUES (?, ?, ?)'''
    conn.execute(consulta, (id_venta, id_producto, unidades))
    conn.commit()

def buscar_producto(conn):
    consulta = '''SELECT id_producto, nombre, info_extra, precio FROM Productos
                WHERE nombre LIKE ?'''
    
    nombre_producto = input("\nIngrese el producto a buscar: ")
    
    datos = conn.execute(consulta, (f"%{nombre_producto}%",))
    productos = datos.fetchall()
    
    if not productos:
        print("No se encontraron productos.")
        return None
    
    for id_producto, nombre, info, precio in productos:
        print(f"ID: {id_producto} | Nombre: {nombre} | Info: {info} | Precio: ${precio}")
        
    try:
        id_producto_elegido = int(input("Ingrese el ID del producto que quiera elegir: "))
        return id_producto_elegido
    except ValueError:
        print("Entrada no válida.")
        return None

def calcular_total_venta(conn, id_venta):
    # CORRECCIÓN: Cambiado Venta_Detalle por Detalle_Ventas
    consulta = '''SELECT SUM(p.precio * vd.cantidad_producto) FROM Productos AS p
                  JOIN Detalle_Ventas AS vd 
                  ON p.id_producto = vd.id_producto
                  WHERE vd.id_venta = ?'''
    dato = conn.execute(consulta, (id_venta,))
    resultado = dato.fetchone()[0]
    
    total_acumulado = resultado if resultado is not None else 0
    
    consulta2 = '''UPDATE Ventas
                SET monto_total = ?
                WHERE id_venta = ?'''
    conn.execute(consulta2, (total_acumulado, id_venta))
    conn.commit()
    
    print(f"\n✅ ¡El pedido fue guardado con éxito! El precio total es: ${total_acumulado}")

def elegir_producto(conn, id_venta):
    opcion = "1"
    while True:
        if opcion == "1":
            id_producto_elegido = buscar_producto(conn)
            if id_producto_elegido is not None:
                unidades = int(input("Cantidad de unidades: ")) 
                guardar_componente_elegido(conn, id_venta, id_producto_elegido, unidades)
                print("Producto agregado al pedido.\n")    
        elif opcion == "2":
            calcular_total_venta(conn, id_venta)
            break
        else:
            print("Opción no válida\n")
        opcion = input('''¿Desea agregar otro producto? (1.Seguir | 2.Finalizar)
                       ''')

def armar_pedido(conn):
    consulta = "INSERT INTO Ventas (nombre_cliente, monto_total, fecha) VALUES (?, 0, ?)"
    nombre_cliente = input("\nInserte el nombre del cliente: ")
    fecha = dt.date.today().isoformat()
    
    cursor = conn.execute(consulta, (nombre_cliente, fecha))
    id_venta = cursor.lastrowid
    
    elegir_producto(conn, id_venta)

def buscar_pedido(conn):
    consulta = ('''SELECT * FROM Ventas
                 WHERE id_venta >= ? AND id_venta <= ?''')
    minimo = int(input("Ingrese el ID desde el cual buscar: "))
    maximo = int(input("Ingrese el ID hasta el cual buscar: "))
    
    datos = conn.execute(consulta, (minimo, maximo))
    pedidos = datos.fetchall()
    
    if not pedidos:
        print("No se encontraron pedidos.")
        return None
    
    for id_venta, cliente, monto, fecha in pedidos:
        print(f"ID: {id_venta} | Nombre: {cliente} | Fecha: {fecha} | Monto: ${monto}")
    
    try:
        id_venta_elegido = int(input("Ingrese el ID de venta: "))
        return id_venta_elegido
    except ValueError:
        print("Entrada no válida.")
        return None
    
def eliminar_pedido(conn):
    id_venta_elegido = buscar_pedido(conn)
    
    # CORRECCIÓN: Si el usuario cancela o no hay ventas, salimos sin error
    if id_venta_elegido is None:
        return
    
    # CORRECCIÓN: Primero borramos el detalle para no romper la relación
    conn.execute('''DELETE FROM Detalle_Ventas WHERE id_venta = ?''', (id_venta_elegido,))
    
    # Luego borramos la venta principal
    consulta = '''DELETE FROM Ventas WHERE id_venta = ?'''
    conn.execute(consulta, (id_venta_elegido,))
    conn.commit()
    
    print("✅ Pedido y sus detalles eliminados correctamente.")

def grafico_productos_mas_vendidos(conn):
    consulta = '''SELECT p.nombre, SUM(vd.cantidad_producto) AS total
                  FROM Productos AS p
                  JOIN Detalle_Ventas AS vd ON p.id_producto = vd.id_producto
                  GROUP BY p.id_producto
                  ORDER BY total DESC LIMIT 5'''
    
    resultados = conn.execute(consulta).fetchall()
    if not resultados or resultados[0][0] is None:
        print("❌ No hay datos suficientes para generar este gráfico.")
        return

    nombres = [fila[0] for fila in resultados]
    cantidades = [fila[1] for fila in resultados]

    plt.figure(figsize=(8, 5))
    plt.bar(nombres, cantidades, color='skyblue', edgecolor='black')
    plt.title("Top 5 - Productos Más Vendidos (Unidades)")
    plt.ylabel("Unidades")
    plt.tight_layout()
    plt.show()

def grafico_clientes_frecuentes(conn):
    consulta = '''SELECT nombre_cliente, COUNT(id_venta) AS compras
                  FROM Ventas
                  GROUP BY nombre_cliente
                  ORDER BY compras DESC LIMIT 5'''
    
    resultados = conn.execute(consulta).fetchall()
    if not resultados:
        print("❌ No hay datos suficientes para generar este gráfico.")
        return

    clientes = [fila[0] for fila in resultados]
    compras = [fila[1] for fila in resultados]

    plt.figure(figsize=(8, 5))
    plt.bar(clientes, compras, color='lightgreen', edgecolor='black')
    plt.title("Top 5 - Clientes Frecuentes")
    plt.ylabel("Cantidad de Pedidos")
    plt.tight_layout()
    plt.show()

def grafico_ingresos_tiempo(conn):
    consulta = '''SELECT fecha, SUM(monto_total) 
                  FROM Ventas 
                  GROUP BY fecha 
                  ORDER BY fecha'''
    
    resultados = conn.execute(consulta).fetchall()
    if not resultados:
        print("❌ No hay datos suficientes para generar este gráfico.")
        return

    fechas = [fila[0] for fila in resultados]
    ingresos = [fila[1] for fila in resultados]

    plt.figure(figsize=(9, 5))
    plt.plot(fechas, ingresos, marker='o', linestyle='-', color='purple', linewidth=2) 
    plt.title("Evolución de Ingresos por Día")
    plt.ylabel("Dinero Ingresado ($)")
    plt.grid(True, linestyle='--', alpha=0.6) 
    plt.xticks(rotation=45) # Rotamos las fechas un poco para que no se superpongan
    plt.tight_layout()
    plt.show()

def grafico_productos_rentables(conn):
    consulta = '''SELECT p.nombre, SUM(p.ganancia * vd.cantidad_producto) AS rentabilidad
                  FROM Productos AS p
                  JOIN Detalle_Ventas AS vd ON p.id_producto = vd.id_producto
                  GROUP BY p.id_producto
                  ORDER BY rentabilidad DESC LIMIT 5'''
    
    resultados = conn.execute(consulta).fetchall()
    if not resultados or resultados[0][0] is None:
        print("❌ No hay datos suficientes para generar este gráfico.")
        return

    nombres = [fila[0] for fila in resultados]
    rentabilidad = [fila[1] for fila in resultados]

    plt.figure(figsize=(9, 5))
    plt.barh(nombres, rentabilidad, color='coral', edgecolor='black')
    plt.title("Top 5 - Productos Más Rentables (Ganancia Neta)")
    plt.xlabel("Ganancia Acumulada ($)")
    plt.gca().invert_yaxis() 
    plt.tight_layout()
    plt.show()

def grafico_ingresos_vs_costos(conn):
    # Sumamos el precio total (ingreso) y el costo total (gasto) de todos los productos vendidos
    consulta = '''SELECT SUM(p.precio * vd.cantidad_producto) AS ingresos,
                         SUM(p.costo * vd.cantidad_producto) AS costos
                  FROM Productos AS p
                  JOIN Detalle_Ventas AS vd ON p.id_producto = vd.id_producto'''
    
    resultado = conn.execute(consulta).fetchone()
    
    # Validamos que no esté vacío (si no hay ventas, SUM devuelve None)
    if not resultado or resultado[0] is None:
        print("❌ No hay datos de ventas para comparar ingresos y costos.")
        return

    ingresos = resultado[0]
    costos = resultado[1]

    categorias = ['Ingresos Brutos', 'Costos de Mercadería']
    valores = [ingresos, costos]

    plt.figure(figsize=(7, 5))
    barras = plt.bar(categorias, valores, color=['#4caf50', '#f44336'], edgecolor='black', width=0.6)
    plt.title("Comparativa Global: Ingresos vs. Costos")
    plt.ylabel("Dinero ($)")

    # Agregamos el número exacto arriba de cada barra para mayor claridad
    for barra in barras:
        altura = barra.get_height()
        plt.text(barra.get_x() + barra.get_width()/2, altura + (altura * 0.01), 
                 f'${altura:.2f}', ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()
    plt.show()

def menu_graficos(conn):
    while True:
        print('''\n------------- GRÁFICOS -------------
            1. Productos más vendidos
            2. Clientes con más pedidos
            3. Ingresos a lo largo del tiempo (días/meses)
            4. Productos más rentables
            5. Ingresos vs. Costos de la mercadería vendida
            6. Salir''')
        
        opcion = input("Elija una opción (1-6): ")
        
        if opcion == "1":
            grafico_productos_mas_vendidos(conn)
        elif opcion == "2":
            grafico_clientes_frecuentes(conn)
        elif opcion == "3":
            grafico_ingresos_tiempo(conn)
        elif opcion == "4":
            grafico_productos_rentables(conn)
        elif opcion == "5":
            grafico_ingresos_vs_costos(conn)
        elif opcion == "6":
            print("Saliendo del menú de gráficos...")
            break
        else:
            print("❌ Entrada no válida. Ingrese un número del 1 al 6.")
    
with sqlite3.connect("base_de_datos.db") as conn:
    # Activamos claves foráneas por buena práctica
    conn.execute("PRAGMA foreign_keys = ON")
    print("------------- BIENVENIDO AL MENÚ -------------\n")
    while True:
        print('''OPCIONES:\n1. Nuevo Pedido\n2. Eliminar Pedido\n3. Mostrar Gráficos\n4. Salir''')
        opcion = input("Elija una opción (1-4): ")
        if opcion == "1":
            armar_pedido(conn)
        elif opcion == "2":
            eliminar_pedido(conn)
        elif opcion == "3":
            menu_graficos(conn)
        elif opcion == "4":
            break
        else:
            print("Entrada no válida\n")