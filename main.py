import os
import requests
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

ultima_vela = 0.0

@app.route('/ultimo')
def ultimo():
    global ultima_vela
    try:
        # Busca real no TipMiner (Substitua pela sua URL de API se tiver)
        # Se a API falhar, este código evita que o Render caia
        response = requests.get("https://api.tipminer.com/api/v1/games/aviator/history", timeout=5)
        if response.status_code == 200:
            dados = response.json()
            ultima_vela = float(dados['data'][0]['result'])
    except:
        pass # Mantém o valor antigo se houver erro de conexão
        
    return jsonify({"valor": ultima_vela})

@app.route('/')
def home():
    return "Robo Conectado"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
