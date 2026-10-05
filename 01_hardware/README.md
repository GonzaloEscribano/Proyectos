Armador de PC con validación de compatibilidad

Programa de consola que guía el armado de una PC paso a paso y evita elegir componentes incompatibles. Los datos viven en una base relacional SQLite.

El problema

Al armar una PC, elegir mal un componente (por ejemplo, una placa madre que no es compatible con el procesador) obliga a devolver la compra. Este programa filtra las opciones en cada paso para que solo se pueda elegir lo compatible.

Cómo funciona

El armado sigue una cadena donde cada elección limita la siguiente:

Procesador: se elige de la lista completa. El programa guarda su socket (por ejemplo, AM4 o LGA1851).
Placa madre: solo se muestran las que coinciden con ese socket.
Memoria RAM: según la placa madre elegida (DDR4 o DDR5), solo se muestra la RAM del tipo correcto.
Placa de video y fuente: se eligen de su categoría.
Se guarda el presupuesto con el precio total calculado con SQL (SUM + JOIN).

Reglas de compatibilidad validadas: socket procesador ↔ placa madre y tipo de RAM ↔ placa madre.

Modelo de datos (SQLite, 4 tablas)
Categorias: tipos de componente.
Componentes: nombre, precio, especificación clave y categoría (clave foránea).
Presupuestos: cada armado guardado, con fecha y precio total.
Presupuesto_Detalle: relación entre un presupuesto y sus componentes.

El catálogo de ejemplo tiene 8 componentes en dos plataformas (AMD AM4 + DDR4 e Intel LGA1851 + DDR5).

Cómo correrlo
bash
cd 01_hardware
python setup_db.py   # crea hardware.db y carga el catálogo
python main.py       # abre el menú

Menú: 1 ver catálogo completo · 2 armar presupuesto · 3 salir. Solo usa la biblioteca estándar de Python (no hay que instalar nada).

Limitaciones y próximos pasos
No valida compatibilidad de fuente ni placa de video (hoy solo se eligen de la lista).
El catálogo es chico y se carga a mano en setup_db.py.
Próximo paso: leer los precios desde un CSV y sumar más plataformas.
Qué aprendí

Modelar relaciones entre tablas (claves foráneas), consultas parametrizadas con ? para evitar inyección SQL y encadenar filtros condicionales.
