from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

EXCEL_FILE = "registros_guardados.xlsx"

@app.route("/")
def home():
    return send_from_directory(os.getcwd(), "index.html")

@app.route("/guardar", methods=["POST"])
def guardar():
    try:
        data = request.json  # Recibe JSON del formulario
        if not data:
            return jsonify({"status": "error", "message": "No se recibieron datos"}), 400

        # Si no existe el archivo, lo crea
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

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
