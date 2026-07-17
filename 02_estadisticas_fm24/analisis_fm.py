# importamos la librería
import sqlite3

# definimos la función
def evaluar_central(pases, robos, distancia, juego_aereo, lectura, faltas_90, errores_gol):
    # Premiamos pases (0.5), robos (2), distancia (1)
    # Premiamos juego aéreo (Rcg % * 0.5) y lectura (Pos Ganadas * 1.5)
    # PENALIZAMOS faltas (-2 por cada falta promedio) y errores garrafales (-5 por error)
    puntaje = pases*0.5 + robos*2 + distancia + juego_aereo*0.5 + lectura*1.5 - faltas_90*2 - errores_gol*5
    return puntaje

# establecemos la conexión
with sqlite3.connect(r"C:\Users\gonza\OneDrive\Desktop\Estadísticas FM\scouting_fm24.db") as conn:
    
    # le enseñamos la fórmula al sql
    conn.create_function("puntaje_central", 7, evaluar_central)
    
    # creamos el cursor
    cursor = conn.cursor()
    
    cursor.execute('''
                   SELECT Nombre, Club, Edad, Altura, puntaje_central("% Pase", Rob, "Dist/90", "Rcg %", "Pos Gan/90", "Faltas/90", "Gl Err") AS PuntajeFinal, Sueldo, ROUND((puntaje_central("% Pase", Rob, "Dist/90", "Rcg %", "Pos Gan/90", "Faltas/90", "Gl Err") / Sueldo) * 10000, 2) AS IndiceRentabilidad
                   FROM Centrales
                   WHERE Sueldo > 0
                   ORDER BY IndiceRentabilidad DESC
                   LIMIT 10
                   ''')
    
    # Imprimimos los resultados con un formato bien de reporte
    print("=== TOP 10 DEFINITIVO: CENTRALES MÁS RENTABLES (CALIDAD / PRECIO) ===")
    for jugador in cursor.fetchall():
        nombre = jugador[0]
        club = jugador[1]
        edad = jugador[2]
        altura = jugador[3]
        puntaje = jugador[4]
        sueldo = jugador[5]
        rentabilidad = jugador[6]
        
        # Imprimimos todo ordenado y cada cosa en su lugar
        print(f"👤 {nombre} ({edad} años) - {club} | 📏 {altura}cm")
        print(f"   📈 Puntaje: {puntaje:.1f} | 💰 Sueldo: ${sueldo:,.0f} | 💎 Índice Rentabilidad: {rentabilidad:.2f}\n")