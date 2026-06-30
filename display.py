import cv2

def draw_detection(frame, bbox, info):
    x1, y1, x2, y2 = bbox
    color_box = (0, 200, 100)
    cv2.rectangle(frame, (x1, y1), (x2, y2), color_box, 2)
    lines = [
        f"{info['tipo']} | {info['marca']} {info['modelo']}",
        f"Color: {info['color']}   Placa: {info['placa']}",
        f"Confianza: {info['confianza']:.0%}",
    ]
    line_h = 22
    pad = 6
    panel_h = len(lines) * line_h + pad * 2
    panel_y = max(y1 - panel_h, 0)
    cv2.rectangle(frame, (x1, panel_y), (x2, y1), (20, 20, 20), -1)
    for i, line in enumerate(lines):
        cv2.putText(frame, line,
                    (x1 + pad, panel_y + pad + (i + 1) * line_h - 4),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1, cv2.LINE_AA)
    return frame

def draw_fps(frame, fps):
    cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    return frame

def draw_overlay_parqueo(frame, modo, ultimo_msg=""):
    h, w = frame.shape[:2]
    cv2.rectangle(frame, (0, h - 60), (w, h), (20, 20, 20), -1)
    cv2.putText(frame, "[ MODO AUTOMATICO ]  Q=salir", (10, h - 35),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 200, 150), 2)
    if ultimo_msg:
        color_msg = (0, 255, 100) if "ENTRADA" in ultimo_msg else (0, 180, 255)
        cv2.putText(frame, ultimo_msg, (10, h - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, color_msg, 1)
    return frame