from ultralytics import YOLO
import config

class CarDetector:
    def __init__(self):
        self.model = YOLO(config.YOLO_MODEL)
        print("[YOLO] Modelo cargado.")

    def detect(self, frame):
        """
        Retorna lista de autos detectados.
        Cada item: {'bbox': (x1,y1,x2,y2), 'confidence': float}
        """
        results = self.model(frame, verbose=False)[0]
        detections = []

        for box in results.boxes:
            class_id = int(box.cls[0])
            conf      = float(box.conf[0])

            if class_id in config.CAR_CLASS_IDS and conf >= config.YOLO_CONFIDENCE:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                detections.append({
                    "bbox":       (x1, y1, x2, y2),
                    "confidence": round(conf, 2)
                })

        return detections
