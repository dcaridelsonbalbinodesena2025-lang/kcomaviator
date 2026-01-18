import os
import requests
import time
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# CONFIGURAÇÃO DO SEU TELEGRAM
TOKEN = "8044840096:AAEayqE2x4V8CD8Fgrdf97Me8nkw0RSWvcg"
CHAT_ID = "5692126478"

# Variável para armazenar a última vela capturada
ultima_vela_detectada = 0.0

def enviar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={mensagem}"
    try:
        requests.get(url)
    except:
        pass

@app.route('/ultimo')
def ultimo():
    global ultima_vela_detectada
    
    try:
        # Aqui o robô tenta ler a API do TipMiner ou EstrelaBet
        # Como o Playwright trava no seu Render, usamos este método leve:
        response = requests.get("https://api.tipminer.com/api/v1/games/aviator/history", timeout=5)
        dados = response.json()
        
        # Pega a vela mais recente da lista
        vela_atual = float(dados['data'][0]['result'])
        
        if vela_atual != ultima_vela_detectada:
            ultima_vela_detectada = vela_atual
            # Opcional: Avisar no Telegram que capturou uma nova
            # enviar_telegram(f"Vela detectada: {vela_atual}x")
            
        return jsonify({"valor": ultima_vela_detectada})
    except:
        # Se a API falhar, ele retorna o último valor conhecido
        return jsonify({"valor": ultima_vela_detectada})

@app.route('/')
def home():
    return "Robo Ativo e Monitorando TipMiner!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
