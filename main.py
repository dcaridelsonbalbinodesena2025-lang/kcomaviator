import os
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Valor de teste para confirmar que a calculadora recebe dados
ultima_vela = 2.00 

@app.route('/')
def home():
    return "Robo Online"

@app.route('/ultimo')
def get_ultimo():
    return jsonify({"valor": ultima_vela})

if __name__ == "__main__":
    # Importante para o Render não dar erro de porta
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
