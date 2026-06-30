import psycopg2
import config

def migrate():
    with psycopg2.connect(
        host=config.DB_HOST, port=config.DB_PORT,
        dbname=config.DB_NAME, user=config.DB_USER, password=config.DB_PASSWORD
    ) as conn:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS detections;")
            cur.execute("""
                CREATE TABLE detections (
                    id             SERIAL PRIMARY KEY,
                    hora_entrada   TIMESTAMP DEFAULT NOW(),
                    hora_salida    TIMESTAMP,
                    marca          TEXT,
                    modelo         TEXT,
                    tipo           TEXT,
                    color          TEXT,
                    placa          TEXT UNIQUE,
                    confianza      FLOAT,
                    imagen_path    TEXT,
                    tiempo_minutos FLOAT,
                    costo_total    FLOAT
                );
            """)
        conn.commit()
    print("[MIGRATE] Tabla recreada correctamente.")

if __name__ == "__main__":
    migrate()