from datetime import datetime, timedelta
import random
import json

def generar_dato():
    dato = {
        "key": '7803f9b4f94ab605f48087da2c2a1627',
        "nivel_colesterol": round(random.uniform(1.0, 3.0), 2),
        "presion_arterial": round(random.uniform(0.6, 1.8), 2),
        "azucar": round(random.uniform(0.5, 2.0), 2),
        "edad": random.randint(0, 99),
        "sobrepeso": random.choice([0, 1]),
        "tabaquismo": random.choice([0, 1]),
        "resultado": round(random.uniform(0.0, 1.0), 4),
        "riesgo_cardiaco": random.choice(["BAJO","ALTO"]),
        "tiempo_procesamiento": round(random.uniform(0.0, 0.2), 4),
        "fecha": str(generar_fecha_aleatoria())
    }
    return dato

def generar_fecha_aleatoria():
    # Establecer un rango de fechas (puedes ajustar según tus necesidades)
    fecha_inicio = datetime(2023, 10, 1)
    fecha_fin = datetime(2024, 1, 12)

    # Calcular un intervalo de tiempo aleatorio entre las fechas
    diferencia = fecha_fin - fecha_inicio
    tiempo_aleatorio = random.uniform(0, diferencia.total_seconds())

    # Crear una fecha aleatoria dentro del rango
    fecha_aleatoria = fecha_inicio + timedelta(seconds=tiempo_aleatorio)

    return fecha_aleatoria


# Generar 100 datos distintos
datos_generados = [generar_dato() for _ in range(100)]

# Guardar en un archivo JSON
with open("datos_generados_log.json", "w") as archivo:
    json.dump(datos_generados, archivo, indent=2)

print("Datos generados y guardados en datos_generados.json.")
