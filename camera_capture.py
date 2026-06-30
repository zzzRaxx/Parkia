import cv2
import config

class CameraCapture:
    def __init__(self):
        self.cap = cv2.VideoCapture(config.CAMERA_INDEX)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,  config.FRAME_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)
        self.cap.set(cv2.CAP_PROP_FPS,          config.FPS_TARGET)

        if not self.cap.isOpened():
            raise RuntimeError("No se pudo abrir la cámara.")
        print("[CAM] Cámara iniciada.")

    def read_frame(self):
        """Retorna (ok, frame). ok=False si falla."""
        return self.cap.read()

    def release(self):
        self.cap.release()
        print("[CAM] Cámara liberada.")
