import cv2
import time
from camera_capture import CameraCapture
from car_detector    import CarDetector
from classifier      import CarClassifier
from color_detector  import detect_color
from plate_reader    import PlateReader
from display         import draw_detection, draw_fps, draw_overlay_parqueo
from database        import create_table, registrar_entrada, registrar_salida, get_autos_en_parqueo
import config

def main():
    create_table()
    cam        = CameraCapture()
    detector   = CarDetector()
    classifier = CarClassifier()
    plate_rdr  = PlateReader()

    print("\n[MAIN] Sistema automático listo. Q=salir\n")

    prev_time  = time.time()
    ultimo_msg = ""

    while True:
        ok, frame = cam.read_frame()
        if not ok:
            break

        detections = detector.detect(frame)

        for det in detections:
            bbox      = det["bbox"]
            confianza = det["confidence"]

            marca, modelo, tipo = classifier.classify(frame, bbox)
            color = detect_color(frame, bbox)
            placa = plate_rdr.read_plate(frame, bbox)

            if placa != "N/A":
                # Verificar si ya tiene entrada activa (sin salida)
                en_parqueo = get_autos_en_parqueo()
                placas_adentro = [str(a["placa"]) for a in en_parqueo]

                if placa in placas_adentro:
                    # Ya estaba → registrar salida
                    resultado = registrar_salida(placa)
                    if resultado:
                        ultimo_msg = (
                            f"SALIDA  {resultado['placa']} | "
                            f"{resultado['minutos']} min | "
                            f"TOTAL: {config.MONEDA} {resultado['costo']}"
                        )
                else:
                    # No estaba → registrar entrada
                    registrar_entrada(marca, modelo, tipo, color, placa, confianza)
                    ultimo_msg = f"ENTRADA  {placa} | Color: {color}"

            info = {
                "marca": marca, "modelo": modelo, "tipo": tipo,
                "color": color, "placa": placa, "confianza": confianza,
                "modo": "auto"
            }
            frame = draw_detection(frame, bbox, info)

        frame = draw_overlay_parqueo(frame, "auto", ultimo_msg)

        now = time.time()
        fps = 1.0 / (now - prev_time + 1e-9)
        prev_time = now
        frame = draw_fps(frame, fps)

        cv2.imshow("Sistema de Parqueo", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()