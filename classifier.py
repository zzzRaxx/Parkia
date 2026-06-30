# Por ahora retorna valores placeholder hasta tener el modelo entrenado.
# En la siguiente fase conectamos un modelo real de marca/modelo.

VEHICLE_TYPES = {2: "Auto", 5: "Bus", 7: "Camioneta"}

class CarClassifier:
    def __init__(self):
        print("[CLASSIFIER] Clasificador iniciado (modo básico).")

    def classify(self, frame, bbox, class_id=2):
        """
        Retorna marca, modelo y tipo.
        Por ahora usa YOLO class_id para el tipo.
        """
        tipo  = VEHICLE_TYPES.get(class_id, "Vehículo")
        marca  = "Desconocida"
        modelo = "Desconocido"

        # ── Aquí conectarás tu modelo de clasificación ──
        # crop = frame[y1:y2, x1:x2]
        # resultado = tu_modelo(crop)
        # marca, modelo = resultado

        return marca, modelo, tipo
