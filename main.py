import os
import requests
from flask import Flask, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- CONFIGURAÇÕES DO TELEGRAM ---
TOKEN = "8044840096:AAEayqE2x4V8CD8Fgrdf97Me8nkw0RSWvcg"
CHAT_ID = "5692126478"

# --- HTML COMPLETO (PAINEL VISUAL) ---
HTML_PAINEL = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculadora Pro - KcomAviator</title>
    <style>
        :root { --azul: #3498db; --verde: #2ecc71; --roxo: #9b59b6; --rosa: #e91e63; }
        body { background: #0b0b0b; color: white; font-family: sans-serif; display: flex; flex-direction: column; align-items: center; padding: 15px; }
        .visor { width: 100%; max-width: 450px; background: #151515; border: 2px solid #333; border-radius: 15px; padding: 20px; text-align: center; margin-bottom: 20px; }
        .status-msg { font-size: 1.2rem; font-weight: bold; color: var(--verde); }
        .grade { display: grid; grid-template-columns: repeat(7, 1fr); gap: 6px; width: 100%; max-width: 450px; margin-bottom: 20px; }
        .vela { background: #222; height: 40px; border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 0.85rem; font-weight: bold; border: 1px solid #444; }
        .v-azul { border: 2px solid #005f87; color: #00d2ff; }
        .v-roxo { border: 2px solid #6441a5; color: #d59fff; }
        .v-rosa { border: 2px solid #bf279b; color: #ff9de2; }
        .cadastro { width: 100%; max-width: 450px; background: #1c1c1c; border-radius: 12px; padding: 15px; border: 1px solid #444; }
        input { width: 60%; padding: 10px; border-radius: 5px; border: 1px solid #555; background: #000; color: white; }
        button { padding: 10px 15px; background: var(--azul); border: none; border-radius: 5px; color: white; cursor: pointer; }
    </style>
</head>
<body onload="iniciar()">
    <div class="visor">
        <div id="status" class="status-msg">AGUARDANDO DADOS...</div>
    </div>
    <div class="grade" id="grade"></div>
    <div class="cadastro">
        <h4 style="margin-bottom:10px;">ESTRATÉGIAS (EX: PPG):</h4>
        <input type="text" id="padraoInput" placeholder="PPG">
        <button onclick="salvarPadrao()">SALVAR</button>
        <div id="listaPadroes" style="margin-top:10px; color: var(--azul); font-size: 0.8rem;"></div>
    </div>

    <script>
        let ultimaVela = 0;
        let historico = [];
        let meusPadroes = [];

        async function buscar() {
            try {
                const res = await fetch('/ultimo');
                const data = await res.json();
                
                if (data.valor > 0 && data.valor !== ultimaVela) {
                    ultimaVela = data.valor;
                    processar(data.valor);
                }
            } catch(e) {}
        }

        function processar(v) {
            let cor = v < 2 ? 'v-azul' : (v < 10 ? 'v-roxo' : 'v-rosa');
            let tipo = v >= 2 ? 'G' : 'P';
            
            historico.unshift({v: v.toFixed(2), c: cor, t: tipo});
            if(historico.length > 21) historico.pop();
            
            document.getElementById('status').innerText = "VELA: " + v.toFixed(2) + "x";
            desenhar();
            verificarSinal();
        }

        function salvarPadrao() {
            let p = document.getElementById('padraoInput').value.toUpperCase();
            if(p) { meusPadroes.push(p); document.getElementById('listaPadroes').innerText = "ATIVOS: " + meusPadroes.join(" | "); }
        }

        function verificarSinal() {
            let seq = historico.map(x => x.t).join('');
            meusPadroes.forEach(p => {
                if(seq.startsWith(p)) {
                    document.getElementById('status').innerText = "🚨 SINAL CONFIRMADO!";
                    fetch(`/sinal?msg=Sinal Confirmado: Padrao ${p}`);
                }
            });
        }

        function desenhar() {
            const g = document.getElementById('grade');
            g.innerHTML = '';
            for(let i=0; i<21; i++) {
                const v = historico[i];
                g.innerHTML += `<div class="vela ${v ? v.c : ''}">${v ? v.v : ''}</div>`;
            }
        }

        function iniciar() { desenhar(); setInterval(buscar, 3000); }
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
        # Busca direta na API para evitar travamentos
        response = requests.get("https://api.tipminer.com/api/v1/games/aviator/history", timeout=5)
        dados = response.json()
        return jsonify({"valor": float(dados['data'][0]['result'])})
    except:
        return jsonify({"valor": 0})

@app.route('/sinal')
def sinal():
    msg = requests.args.get('msg')
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}")
    return "OK"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
