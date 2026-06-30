# ─── Cámara ───────────────────────────────────────────────
CAMERA_INDEX = 0          # 0 = cámara por defecto
FRAME_WIDTH  = 1280
FRAME_HEIGHT = 720
FPS_TARGET   = 30

# ─── YOLO ─────────────────────────────────────────────────
YOLO_MODEL        = "yolov8n.pt"   # nano = más rápido
YOLO_CONFIDENCE   = 0.50           # confianza mínima (0-1)
CAR_CLASS_IDS     = [2, 5, 7]      # COCO: car, bus, truck

# ─── Clasificador de marca/modelo ─────────────────────────
CLASSIFIER_MODEL  = "models/car_classifier.pt"
CLASSIFIER_LABELS = "models/labels.txt"

# ─── OCR de placa ─────────────────────────────────────────
OCR_LANGUAGES     = ["es", "en"]
PLATE_MIN_CONF    = 0.40

# ─── Base de datos PostgreSQL ──────────────────────────────
# ─── Parqueo ──────────────────────────────────────────────
TARIFA_POR_HORA   = 10.0   # Bolivianos por hora
MONEDA            = "Bs"
DB_HOST     = "localhost"
DB_PORT     = 5432
DB_NAME     = "car_detector"
DB_USER     = "postgres"
DB_PASSWORD = "12345678"   # <-- cambia esto
