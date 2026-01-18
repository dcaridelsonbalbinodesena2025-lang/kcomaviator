import os
import requests
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Variável para controlar a última vela e não repetir na grade
ultima_vela_conhecida = 0.0

@app.route('/ultimo')
def ultimo():
    global ultima_vela_conhecida
    try:
        # Busca os dados reais do TipMiner (API leve)
        response = requests.get("https://api.tipminer.com/api/v1/games/aviator/history", timeout=5)
        if response.status_code == 200:
            dados = response.json()
            # Pega o resultado da última rodada que saiu no site
            vela_atual = float(dados['data'][0]['result'])
            return jsonify({"valor": vela_atual})
    except Exception as e:
        print(f"Erro na busca: {e}")
    
    # Se der erro ou não houver vela nova, ele mantém o que já tinha
    return jsonify({"valor": ultima_vela_conhecida})

@app.route('/')
def home():
    return "Robo KcomAviator Online"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
