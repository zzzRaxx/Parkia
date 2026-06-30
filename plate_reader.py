import easyocr
import cv2
import config

class PlateReader:
    def __init__(self):
        self.reader = easyocr.Reader(config.OCR_LANGUAGES, gpu=False)
        print("[OCR] EasyOCR iniciado.")

    def read_plate(self, frame, bbox):
        """
        Intenta leer la placa dentro del bbox del auto.
        Retorna el texto o 'N/A'.
        """
        x1, y1, x2, y2 = bbox
        crop = frame[y1:y2, x1:x2]

        if crop.size == 0:
            return "N/A"

        # Enfocar la parte inferior donde suele estar la placa
        h = crop.shape[0]
        plate_zone = crop[int(h * 0.6):, :]

        gray = cv2.cvtColor(plate_zone, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, None, fx=2, fy=2)  # zoom para mejor OCR

        results = self.reader.readtext(gray)

        for (_, text, conf) in results:
            clean = text.upper().replace(" ", "").replace("-", "")
            # Filtrar resultados que parecen placa (4-8 chars alfanuméricos)
            if conf >= config.PLATE_MIN_CONF and 4 <= len(clean) <= 8:
                return clean

        return "N/A"
