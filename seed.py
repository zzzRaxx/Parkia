import psycopg2
from datetime import datetime, timedelta
import config

datos = [
    ("Toyota",     "Corolla",   "Auto",      "Blanco",   "1234ABC", 0.92),
    ("Toyota",     "Hilux",     "Camioneta", "Negro",    "9876XYZ", 0.88),
    ("Nissan",     "Sentra",    "Auto",      "Gris",     "4567DEF", 0.91),
    ("Chevrolet",  "Silverado", "Camioneta", "Rojo",     "7890GHI", 0.85),
    ("Honda",      "Civic",     "Auto",      "Azul",     "2345JKL", 0.93),
    ("Ford",       "Ranger",    "Camioneta", "Blanco",   "6789MNO", 0.87),
    ("Hyundai",    "Tucson",    "Auto",      "Gris",     "3456PQR", 0.90),
    ("Kia",        "Sportage",  "Auto",      "Negro",    "8901STU", 0.89),
    ("Mazda",      "CX-5",      "Auto",      "Rojo",     "2345VWX", 0.94),
    ("Suzuki",     "Swift",     "Auto",      "Amarillo", "6789YZA", 0.86),
    ("Mitsubishi", "L200",      "Camioneta", "Blanco",   "1234BCD", 0.91),
    # --- estos 4 siguen adentro ---
    ("BMW",        "320i",      "Auto",      "Negro",    "5678EFG", 0.95),
    ("Mercedes",   "C200",      "Auto",      "Gris",     "9012HIJ", 0.93),
    ("Volkswagen", "Golf",      "Auto",      "Azul",     "3456KLM", 0.88),
    ("Jeep",       "Wrangler",  "Camioneta", "Verde",    "7890NOP", 0.90),
]

SIN_SALIDA = {"5678EFG", "9012HIJ", "3456KLM", "7890NOP"}

def seed():
    # Hora base: hace 8 horas, cada auto llega 30 minutos después del anterior
    hora_base = datetime.now() - timedelta(hours=8)

    with psycopg2.connect(
        host=config.DB_HOST, port=config.DB_PORT,
        dbname=config.DB_NAME, user=config.DB_USER, password=config.DB_PASSWORD
    ) as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM detections;")

            for i, (marca, modelo, tipo, color, placa, conf) in enumerate(datos):
                hora_entrada = hora_base + timedelta(minutes=i * 30)

                if placa in SIN_SALIDA:
                    hora_sal = None
                    minutos  = None
                    costo    = None
                else:
                    # Se fue entre 20 y 90 minutos después de entrar
                    minutos  = 20 + (i * 7)   # progresivo para que no se repita
                    hora_sal = hora_entrada + timedelta(minutes=minutos)
                    costo    = round((minutos / 60) * config.TARIFA_POR_HORA, 2)

                cur.execute("""
                    INSERT INTO detections
                        (hora_entrada, hora_salida, marca, modelo, tipo,
                         color, placa, confianza, tiempo_minutos, costo_total)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, (hora_entrada, hora_sal, marca, modelo, tipo,
                      color, placa, conf,
                      round(minutos, 2) if minutos else None, costo))

        conn.commit()
    print("[SEED] 15 registros ordenados por llegada. 4 todavía en parqueo.")

if __name__ == "__main__":
    seed()