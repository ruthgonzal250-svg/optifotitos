from flask import Flask, render_template, request, redirect, url_for
import os
import cv2
import numpy as np
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Carpeta donde se guardan imágenes subidas y procesadas
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Función de optimización ligera con OpenCV
def optimizar_imagen(ruta_entrada, ruta_salida):
    img = cv2.imread(ruta_entrada)

    # Ajuste de brillo y contraste automático
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    l = clahe.apply(l)
    lab = cv2.merge((l, a, b))
    img_clahe = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    # Suavizado ligero para evitar pixelado
    img_suave = cv2.GaussianBlur(img_clahe, (3,3), 0)

    cv2.imwrite(ruta_salida, img_suave)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/subir', methods=['POST'])
def subir():
    if 'imagen' not in request.files:
        return redirect(url_for('index'))

    file = request.files['imagen']
    if file.filename == '':
        return redirect(url_for('index'))

    filename = secure_filename(file.filename)
    ruta_entrada = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(ruta_entrada)

    # Crear nombre para la imagen procesada
    nombre_salida = "mejorada_" + filename
    ruta_salida = os.path.join(app.config['UPLOAD_FOLDER'], nombre_salida)

    # Optimizar la imagen
    optimizar_imagen(ruta_entrada, ruta_salida)

    return render_template('resultado.html', antes=os.path.join('uploads', filename), despues=os.path.join('uploads', nombre_salida))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
