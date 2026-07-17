# importamos las librerías
import pandas as pd
import sqlite3
import numpy as np

# guardamos el archivo
archivo = pd.read_html("centrales_arg1_gemini.html", encoding='utf8', decimal=',', thousands='.')       # utf8 para que se lean bien los nombres

# nos quedamos solamente con la tabla de los jugadores
df_jugadores = archivo[0]

# imprimimos nombres de columnas
print(df_jugadores.columns.to_list())

# eliminamos columnas que no nos sirven
df_jugadores = df_jugadores.drop("Inf", axis=1)

# renombramos las columnas que están mal
df_jugadores = df_jugadores.rename(columns= {"PosiciÃ³n":"Posicion"})

# ajustamos los registros que contengan info de más
# 1. Agarro la columna original
# 2. Le aplico .str.split(' - ') para cortarla por el guion
# 3. Le aplico .str[0] para quedarme solo con la primera parte de ese corte
# 4. Sobrescribo la columna original con este resultado limpio
df_jugadores['Nombre'] = df_jugadores['Nombre'].str.split(' - ').str[0]
df_jugadores["Club"] = df_jugadores["Club"].str.split(" - ").str[0]

df_jugadores["Dist/90"] = df_jugadores["Dist/90"].str.replace(" km", "")
df_jugadores["Dist/90"] = df_jugadores["Dist/90"].str.replace(",", ".")
df_jugadores["Dist/90"] = df_jugadores["Dist/90"].astype(float)         # lo convertimos en float

df_jugadores["% Pase"] = df_jugadores["% Pase"].str.replace("%", "")
df_jugadores["% Pase"] = df_jugadores["% Pase"].astype(int)         # lo convertimos en integer

df_jugadores["Min"] = df_jugadores["Min"].astype(str)          # lo convertimos en string para que nos deje modificar
df_jugadores["Min"] = df_jugadores["Min"].str.replace(".", "")
df_jugadores["Min"] = df_jugadores["Min"].astype(int)         # lo convertimos en integer

df_jugadores["Altura"] = df_jugadores["Altura"].str.replace(" cm", "")
df_jugadores["Altura"] = df_jugadores["Altura"].astype(int)

df_jugadores["Rcg %"] = df_jugadores["Rcg %"].str.replace("%", "")
df_jugadores["Rcg %"] = df_jugadores["Rcg %"].astype(float)

df_jugadores["Pos Gan/90"] = df_jugadores["Pos Gan/90"].astype(str).str.replace(",", ".").astype(float)
df_jugadores["DsR/90"] = df_jugadores["DsR/90"].astype(str).str.replace(",", ".").astype(float)
df_jugadores["Cab Clv/90"] = df_jugadores["Cab Clv/90"].astype(str).str.replace(",", ".").astype(float)

# Nos aseguramos que Errores y Faltas sean números
df_jugadores["FC"] = pd.to_numeric(df_jugadores["FC"], errors='coerce').fillna(0).astype(int)
df_jugadores["Gl Err"] = pd.to_numeric(df_jugadores["Gl Err"], errors='coerce').fillna(0).astype(int)

# --- FEATURE ENGINEERING (Creación de nueva métrica) ---
# Calculamos Faltas por 90 minutos: (Faltas totales / Minutos jugados) * 90
# Usamos un filtro rápido donde Min > 0 para evitar dividir por cero y que explote Python
df_jugadores["Faltas/90"] = np.where(df_jugadores["Min"] > 0, (df_jugadores["FC"] / df_jugadores["Min"]) * 90, 0)
df_jugadores["Faltas/90"] = df_jugadores["Faltas/90"].round(2) # Redondeamos a 2 decimales

# 1. Por las dudas, forzamos a que toda la columna se lea como texto primero
df_jugadores['Sueldo'] = df_jugadores['Sueldo'].astype(str)

# 2. LA BAZUCA: \D significa "cualquier carácter que no sea un dígito". 
# Lo reemplazamos por nada (''). Así sobreviven solo los números.
df_jugadores['Sueldo'] = df_jugadores['Sueldo'].str.replace(r'\D', '', regex=True)

# 3. Ahora sí, convertimos a número. Los que queden vacíos se vuelven NaN automáticamente.
df_jugadores['Sueldo'] = pd.to_numeric(df_jugadores['Sueldo'], errors='coerce')

with sqlite3.connect(r"C:\Users\gonza\OneDrive\Desktop\Estadísticas FM\scouting_fm24.db") as conn:
    df_jugadores.to_sql("Centrales", conn, if_exists="replace", index=False)
    
    # if_exists="replace" es vital: si mañana volvés a correr el script de Python, pisa la tabla vieja en vez de duplicar a todos los jugadores
    # index=False para que no te guarde los numeritos 0, 1, 2, 3 del índice de Pandas como una columna extra inútil en SQL

print(df_jugadores[['Nombre', 'Altura', 'Rcg %', 'Pos Gan/90', 'FC', 'Faltas/90', 'Gl Err', 'Min']].head())
# Filtramos y mostramos a los "Sin Nombre"
print(df_jugadores[df_jugadores['Nombre'] == '- -'][['Nombre', 'Club', 'Edad']].head(10))