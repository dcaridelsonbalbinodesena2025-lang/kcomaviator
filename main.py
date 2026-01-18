import time
import requests
from playwright.sync_api import sync_playwright

# CONFIGURAÇÕES
TOKEN = "8044840096:AAEayqE2x4V8CD8Fgrdf97Me8nkw0RSWvcg"
CHAT_ID = "SEU_CHAT_ID" # Use o @userinfobot no Telegram para descobrir o seu ID
URL_TIPMINER = "LINK_DO_TIPMINER_AQUI" 

def enviar_msg(texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={texto}"
    requests.get(url)

def motor_analisador():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL_TIPMINER)
        
        historico = []
        
        while True:
            try:
                # Captura o último valor (precisamos do seletor real do site)
                # Exemplo genérico:
                ultimo_v = page.query_selector(".valor-ultimo").inner_text()
                valor = float(ultimo_v.replace('x', ''))

                if not historico or valor != historico[0]:
                    historico.insert(0, valor)
                    tipo = "G" if valor >= 2.0 else "P"
                    print(f"Novo: {valor}x ({tipo})")

                    # EXEMPLO DE LÓGICA (Seu padrão PPG)
                    if len(historico) >= 3:
                        seq = "".join(["G" if v >= 2.0 else "P" for v in historico[:3]])
                        if seq == "GPP": # Invertido pois o 0 é o mais recente
                            enviar_msg("⚠️ ENTRADA CONFIRMADA: Padrão PPG detectado!")

                time.sleep(3)
            except Exception as e:
                time.sleep(5)

if __name__ == "__main__":
    motor_analisador()
