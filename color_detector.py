import cv2
import numpy as np

# Rangos HSV para cada color
COLOR_RANGES = {
    "Rojo":    [((0,  70, 50), (10, 255,255)), ((170,70,50),(180,255,255))],
    "Naranja": [((11, 70, 50), (25, 255,255))],
    "Amarillo":[((26, 70, 50), (34, 255,255))],
    "Verde":   [((35, 40, 40), (85, 255,255))],
    "Azul":    [((86, 50, 50), (128,255,255))],
    "Morado":  [((129,50, 50), (155,255,255))],
    "Blanco":  [((0,  0, 200), (180, 30,255))],
    "Negro":   [((0,  0,  0),  (180, 255, 50))],
    "Gris":    [((0,  0, 51),  (180, 30, 199))],
}

def detect_color(frame, bbox):
    """Detecta el color predominante del auto recortado."""
    x1, y1, x2, y2 = bbox
    crop = frame[y1:y2, x1:x2]

    if crop.size == 0:
        return "Desconocido"

    # Zona central para evitar bordes y fondo
    h, w = crop.shape[:2]
    center = crop[h//4: 3*h//4, w//4: 3*w//4]
    hsv = cv2.cvtColor(center, cv2.COLOR_BGR2HSV)

    best_color = "Desconocido"
    best_count = 0

    for color_name, ranges in COLOR_RANGES.items():
        mask = np.zeros(hsv.shape[:2], dtype=np.uint8)
        for (lo, hi) in ranges:
            mask |= cv2.inRange(hsv, np.array(lo), np.array(hi))
        count = cv2.countNonZero(mask)
        if count > best_count:
            best_count = count
            best_color = color_name

    return best_color
