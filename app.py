from flask import Flask, render_template, request
import os
import cv2
import uuid
import numpy as np

app = Flask(__name__)
app.static_folder = 'static'
UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/subir", methods=["POST"])
def subir():
    if "imagen" not in request.files:
        return "No se envió ninguna imagen.", 400

    imagen = request.files["imagen"]
    if imagen.filename == "":
        return "Archivo vacío.", 400

    nombre_id = str(uuid.uuid4())
    nombre_original = f"{nombre_id}_original.png"
    nombre_optimizada = f"{nombre_id}_optimizada.png"

    ruta_original = os.path.join(UPLOAD_FOLDER, nombre_original)
    imagen.save(ruta_original)

    try:
        img = cv2.imread(ruta_original)
        if img is None:
            return "Error al leer la imagen.", 400

        alpha = 1.02
        beta = 3
        img_contrast = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

        img_enhanced = cv2.detailEnhance(img_contrast, sigma_s=5, sigma_r=0.05)

        img_hsv = cv2.cvtColor(img_enhanced, cv2.COLOR_BGR2HSV)
        factor_saturacion = 0.75
        img_hsv[:, :, 1] = (img_hsv[:, :, 1] * factor_saturacion).astype(np.uint8)
        img_final = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)

        kernel = np.array([[0, -0.2, 0],
                           [-0.2, 1.8, -0.2],
                           [0, -0.2, 0]])
        img_final = cv2.filter2D(img_final, -1, kernel)

        ruta_optimizada = os.path.join(UPLOAD_FOLDER, nombre_optimizada)
        cv2.imwrite(ruta_optimizada, img_final)

    except Exception as e:
        print("❌ Error al optimizar:", e)
        return "Error interno al procesar la imagen.", 500

    antes_url = f"/{ruta_original.replace(os.sep, '/')}"
    despues_url = f"/{ruta_optimizada.replace(os.sep, '/')}"

    return render_template("resultado.html", antes=antes_url, despues=despues_url)

if __name__ == "__main__":
    app.run(debug=True)
