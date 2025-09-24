from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
import os

app = Flask(__name__)

# Carpeta temporal en Render
CARPETA_EXCEL = "/tmp/archivos_excel"
os.makedirs(CARPETA_EXCEL, exist_ok=True)
EXCEL_FILE = os.path.join(CARPETA_EXCEL, "registros_internacional.xlsx")

# Ruta para servir el index.html
@app.route("/")
def home():
    return send_from_directory(os.getcwd(), "index.html")

# Ruta para guardar en Excel
@app.route("/guardar", methods=["POST"])
def guardar():
    try:
        data = request.json
        if not data:
            return jsonify({"status": "error", "message": "No llegaron datos"}), 400

        # Crear o actualizar Excel
        if not os.path.exists(EXCEL_FILE):
            df = pd.DataFrame([data])
            df.to_excel(EXCEL_FILE, index=False)
        else:
            df = pd.read_excel(EXCEL_FILE)
            df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
            df.to_excel(EXCEL_FILE, index=False)

        return jsonify({"status": "success", "message": "Datos guardados en Excel"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Ruta para descargar el Excel
@app.route("/descargar", methods=["GET"])
def descargar():
    if os.path.exists(EXCEL_FILE):
        return send_from_directory(CARPETA_EXCEL, "registros_internacional.xlsx", as_attachment=True)
    return jsonify({"status": "error", "message": "No existe el archivo"}), 404

if __name__ == "__main__":
    # Render ignora esto y usa gunicorn, pero sirve en local
    app.run(debug=True, host="0.0.0.0", port=5000)
