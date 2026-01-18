from flask import Flask, jsonify
from flask_cors import CORS # Importante para não dar erro de bloqueio

app = Flask(__name__)
CORS(app) # Isso permite que o GitHub fale com o Render sem bloqueios

ultima_vela = 0.0 # Aqui o seu robô vai guardar a vela do TipMiner

@app.route('/ultimo')
def pegar_vela():
    return jsonify({"valor": ultima_vela})

@app.route('/')
def home():
    return "Robô Ativo! Use /ultimo para ver os dados."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
