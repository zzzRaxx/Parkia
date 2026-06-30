import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import config

def get_connection():
    return psycopg2.connect(
        host     = config.DB_HOST,
        port     = config.DB_PORT,
        dbname   = config.DB_NAME,
        user     = config.DB_USER,
        password = config.DB_PASSWORD
    )

def create_table():
    sql = """
    CREATE TABLE IF NOT EXISTS detections (
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
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()
    print("[DB] Tabla 'detections' lista.")

def registrar_entrada(marca, modelo, tipo, color, placa, confianza, imagen_path=None):
    sql_check = "SELECT id FROM detections WHERE placa = %s AND hora_salida IS NULL;"
    sql_insert = """
        INSERT INTO detections (marca, modelo, tipo, color, placa, confianza, imagen_path)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (placa) DO NOTHING
        RETURNING id;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql_check, (placa,))
            existe = cur.fetchone()
            if existe:
                print(f"[DB] Auto {placa} ya está en el parqueo (ID {existe[0]})")
                return existe[0]
            cur.execute(sql_insert, (marca, modelo, tipo, color, placa, confianza, imagen_path))
            row = cur.fetchone()
            new_id = row[0] if row else None
        conn.commit()
    if new_id:
        print(f"[DB] Entrada registrada → Placa: {placa} | ID: {new_id}")
    return new_id

def registrar_salida(placa):
    sql_buscar = """
        SELECT id, hora_entrada FROM detections
        WHERE placa = %s AND hora_salida IS NULL
        ORDER BY hora_entrada DESC LIMIT 1;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql_buscar, (placa,))
            row = cur.fetchone()
            if not row:
                print(f"[DB] No se encontró entrada activa para placa: {placa}")
                return None
            det_id, hora_entrada = row
            hora_salida    = datetime.now()
            minutos        = (hora_salida - hora_entrada).total_seconds() / 60
            costo          = round((minutos / 60) * config.TARIFA_POR_HORA, 2)
            cur.execute("""
                UPDATE detections
                SET hora_salida = %s, tiempo_minutos = %s, costo_total = %s
                WHERE id = %s;
            """, (hora_salida, round(minutos, 2), costo, det_id))
        conn.commit()
    resultado = {
        "id": det_id, "placa": placa,
        "hora_entrada": hora_entrada.strftime("%H:%M:%S"),
        "hora_salida":  hora_salida.strftime("%H:%M:%S"),
        "minutos": round(minutos, 1), "costo": costo
    }
    print(f"[DB] Salida → Placa: {placa} | {round(minutos,1)} min | Bs {costo}")
    return resultado

def get_autos_en_parqueo():
    sql = "SELECT id, hora_entrada, marca, modelo, color, placa FROM detections WHERE hora_salida IS NULL ORDER BY hora_entrada DESC;"
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql)
            return cur.fetchall()

def get_historial(limit=20):
    sql = "SELECT id, hora_entrada, hora_salida, placa, color, tiempo_minutos, costo_total FROM detections WHERE hora_salida IS NOT NULL ORDER BY hora_salida DESC LIMIT %s;"
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, (limit,))
            return cur.fetchall()