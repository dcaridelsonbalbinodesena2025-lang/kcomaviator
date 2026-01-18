import os
import requests
from flask import Flask, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- CONFIGURAÇÕES ---
TOKEN = "8044840096:AAEayqE2x4V8CD8Fgrdf97Me8nkw0RSWvcg"
CHAT_ID = "5692126478"

# Página Visual (O Painel que você via no GitHub agora dentro do Render)
HTML_PAINEL = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculadora Integrada - KcomAviator</title>
    <style>
        body { background: #0b0b0b; color: white; font-family: sans-serif; display: flex; flex-direction: column; align-items: center; padding: 20px; }
        .visor { width: 100%; max-width: 400px; background: #151515; border-radius: 15px; padding: 20px; text-align: center; border: 2px solid #333; margin-bottom: 20px; }
        .grade { display: grid; grid-template-columns: repeat(7, 1fr); gap: 8px; width: 100%; max-width: 400px; }
        .vela { background: #222; height: 45px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 0.9rem; border: 1px solid #444; }
        .v-azul { border: 2px solid #005f87; color: #00d2ff; }
        .v-roxo { border: 2px solid #6441a5; color: #d59fff; }
        .v-rosa { border: 2px solid #bf279b; color: #ff9de2; }
    </style>
</head>
<body onload="atualizar()">
    <div class="visor">
        <h2 id="status">CONECTANDO...</h2>
    </div>
    <div class="grade" id="grade"></div>

    <script>
        let ultimaVela = 0;
        let historico = [];

        async function atualizar() {
            try {
                const res = await fetch('/ultimo');
                const data = await res.json();
                
                if (data.valor !== ultimaVela) {
                    ultimaVela = data.valor;
                    let cor = data.valor < 2 ? 'v-azul' : (data.valor < 10 ? 'v-roxo' : 'v-rosa');
                    historico.unshift({v: data.valor.toFixed(2), c: cor});
                    if(historico.length > 21) historico.pop();
                    desenhar();
                    document.getElementById('status').innerText = "Vela: " + data.valor + "x";
                }
            } catch(e) {}
            setTimeout(atualizar, 3000);
        }

        function desenhar() {
            const g = document.getElementById('grade');
            g.innerHTML = '';
            for(let i=0; i<21; i++) {
                const v = historico[i];
                g.innerHTML += `<div class="vela ${v ? v.c : ''}">${v ? v.v : ''}</div>`;
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAINEL)

@app.route('/ultimo')
def ultimo():
    try:
        # Busca real na API do TipMiner
        response = requests.get("https://api.tipminer.com/api/v1/games/aviator/history", timeout=5)
        dados = response.json()
        valor = float(dados['data'][0]['result'])
        return jsonify({"valor": valor})
    except:
        return jsonify({"valor": 0})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
