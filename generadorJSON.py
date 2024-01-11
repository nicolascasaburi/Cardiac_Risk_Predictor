import random
import json

def generar_dato():
    dato = {
        "nivel_colesterol": round(random.uniform(1.0, 3.0), 2),
        "presion_arterial": round(random.uniform(0.6, 1.8), 2),
        "azucar": round(random.uniform(0.5, 2.0), 2),
        "edad": random.randint(0, 99),
        "sobrepeso": random.choice([0, 1]),
        "tabaquismo": random.choice([0, 1])
    }
    return dato

# Generar 100 datos distintos
datos_generados = [generar_dato() for _ in range(100)]

# Guardar en un archivo JSON
with open("datos_generados.json", "w") as archivo:
    json.dump(datos_generados, archivo, indent=2)

print("Datos generados y guardados en datos_generados.json.")
