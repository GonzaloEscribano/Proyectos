Sistema de ventas a pedido

Aplicación de consola para registrar pedidos por encargo y analizar las ventas con gráficos, sobre una base relacional SQLite.

El problema

Una venta a pedido genera muchos datos sueltos (qué cliente, qué productos, cuántas unidades, a qué costo). Llevarlo a mano dificulta saber cuáles son los productos más rentables, quiénes compran más y si el negocio gana plata.

Qué hace
Carga de pedidos: busca productos por nombre, arma el pedido con cantidades y calcula el total con SQL (JOIN + SUM).
Gestión de productos (setup.py): alta, modificación de precio/costo (recalcula la ganancia) y baja.
Eliminación de pedidos respetando la relación entre tablas.
5 gráficos de análisis con Matplotlib:
Top 5 productos más vendidos
Top 5 clientes con más pedidos
Evolución de ingresos por día
Top 5 productos más rentables (ganancia acumulada)
Ingresos vs. costos de la mercadería vendida

Capturas de los gráficos: [agregar imágenes]

Modelo de datos (SQLite, 3 tablas)
Productos: nombre, costo, precio, ganancia e información extra.
Ventas: cliente, monto total y fecha.
Detalle_Ventas: relación entre cada venta y sus productos, con la cantidad (claves foráneas).
Cómo correrlo
bash
cd 03_ventas
pip install matplotlib
python setup.py   # opción 1: crear tablas; opción 2: cargar productos
python main.py    # opción 1: nuevo pedido · 3: gráficos
Limitaciones y próximos pasos
La interfaz es de consola; el siguiente paso sería una app web para ver los gráficos sin menús.
No hay datos de ejemplo incluidos: hay que cargar productos con setup.py.
Qué aprendí

Diseño de un modelo relacional con claves foráneas, consultas con JOIN y GROUP BY, y visualización de resultados de SQL con Matplotlib.
