import os
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Valor de teste para ver se aparece na sua calculadora
ultima_vela = 2.50 

@app.route('/')
def home():
    return "Robo Online - Use /ultimo para dados"

@app.route('/ultimo')
def get_ultimo():
    return jsonify({"valor": ultima_vela})

if __name__ == "__main__":
    # O Render exige que usemos a porta fornecida por eles
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
