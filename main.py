import time
import requests
from flask import Flask, jsonify
from threading import Thread
from playwright.sync_api import sync_playwright

app = Flask(__name__)
# Armazena o último resultado capturado para sua calculadora ler
dados_aviator = {"valor": 0.0}

# --- SUAS INFORMAÇÕES CONFIGURADAS ---
TOKEN = "8044840096:AAEayqE2x4V8CD8Fgrdf97Me8nkw0RSWvcg"
CHAT_ID = "5692126478" 
URL_ALVO = "https://www.tipminer.com/br/historico/estrelabet/aviator"

def enviar_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}"
        requests.get(url)
    except Exception as e:
        print(f"Erro Telegram: {e}")

def monitorar_tipminer():
    global dados_aviator
    with sync_playwright() as p:
        # Abre o navegador em modo invisível
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
        page = context.new_page()
        
        print(f"🔗 Conectando ao TipMiner...")
        page.goto(URL_ALVO)
        
        while True:
            try:
                # Seletor atualizado para pegar o primeiro resultado da grade do TipMiner
                elemento = page.query_selector(".result-value") 
                
                if elemento:
                    valor_texto = elemento.inner_text().replace('x', '').strip()
                    valor_float = float(valor_texto)

                    # Se sair um número novo
                    if valor_float != dados_aviator["valor"]:
                        dados_aviator["valor"] = valor_float
                        print(f"🎰 Novo Resultado: {valor_float}x")
                        
                        # Exemplo: Se quiser alerta de Vela Rosa no Telegram
                        if valor_float >= 10.0:
                            enviar_telegram(f"🔥 VELA ROSA DETECTADA: {valor_float}x")
                
                time.sleep(2) # Verifica a cada 2 segundos
            except Exception as e:
                print(f"Aguardando atualização do site... {e}")
                time.sleep(5)

# Rota que sua calculadora vai acessar
@app.route('/ultimo')
def obter_ultimo():
    return jsonify(dados_aviator)

if __name__ == "__main__":
    # Inicia a captura em segundo plano
    t = Thread(target=monitorar_tipminer)
    t.start()
    # Inicia o servidor na porta padrão do Render
    app.run(host='0.0.0.0', port=10000)
