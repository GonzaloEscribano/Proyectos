Análisis de rendimiento de defensores centrales (FM24)

Pipeline en Python para limpiar un dataset de estadísticas de defensores centrales exportado de Football Manager 2024, guardarlo en SQLite y rankearlos según un puntaje de rendimiento y una relación calidad/sueldo.

El problema

Los datos exportados del juego vienen con formatos mezclados: unidades pegadas al número ("12,3 km", "85%"), separadores de miles y decimales con coma, columnas con texto extra y vacíos. Así no se pueden comparar jugadores ni calcular nada.

Qué hace
Limpieza (limpieza_fm.py, Pandas): lee la tabla HTML exportada, corrige nombres de columnas con errores de codificación, elimina columnas innecesarias, quita unidades y símbolos, convierte tipos (int/float) y trata vacíos. Crea una métrica nueva, Faltas/90, evitando división por cero.
Almacenamiento: guarda el resultado en una base SQLite (scouting_fm24.db, tabla Centrales: 88 jugadores × 26 columnas).
Análisis (analisis_fm.py, SQL): define una función de puntaje que se registra dentro de SQLite y la usa en una consulta. El puntaje premia pases, robos, distancia recorrida, juego aéreo y lectura de juego, y penaliza faltas y errores que terminan en gol. Después calcula un índice de rentabilidad = puntaje / sueldo y devuelve el top 10.
Resultado

Un ranking de los 10 centrales con mejor relación rendimiento/sueldo, listo para usar en una decisión de fichaje.

Captura del resultado: [agregar imagen del top 10 en consola]

Cómo correrlo
bash
cd 02_estadisticas_fm24
pip install pandas numpy
python analisis_fm.py    # usa la base scouting_fm24.db incluida en el repo

limpieza_fm.py regenera la base desde el archivo HTML exportado del juego.

Limitaciones
Los pesos del puntaje (por ejemplo, robos ×2, errores ×5) son criterio propio, no están validados estadísticamente.
El análisis cubre una sola posición (centrales) y una muestra de 88 jugadores.
Próximo paso: comparar contra la media de la liga y visualizar el ranking.
Qué aprendí

Limpieza de datos reales con Pandas (expresiones regulares, conversión de tipos), creación de métricas derivadas y uso de funciones propias dentro de consultas SQL.
