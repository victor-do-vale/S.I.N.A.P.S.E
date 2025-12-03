# -------------------------------------------------------------
# Projeto: Fazenda Inteligente
# Módulo: Alerta de Presença (PIR + LED + Buzzer + WhatsApp)
# Autor: Adilson Nascimento dos Santos
# Convertido para: MicroPython com WhatsApp
# -------------------------------------------------------------

from machine import Pin, PWM
import network
import urequests
import time

# --------------------- CONFIGURAÇÃO DE PINOS ---------------------
PIR_PIN = 15
LED_ALERTA = 13
BUZZER_PIN = 14

# ---------------- ESTADO DO SENSOR -----------------
movimento_anterior = False

# ------------------- CONFIG WHATSAPP (CallMeBot API) --------------------
# Seu número no formato internacional: +55219XXXXXXXX (sem espaços)
WHATSAPP_PHONE = "+551124355"
# API Key obtida do CallMeBot
WHATSAPP_API_KEY = "SUA_API_KEY"

# ------------------- CONFIG WI-FI --------------------
#colocar suas config de wifi
WIFI_SSID = "SUA_REDE"
WIFI_PASSWORD = "SENHA"

# ------------------- INICIALIZAÇÃO DOS PINOS ------------------
pir = Pin(PIR_PIN, Pin.IN)
led_alerta = Pin(LED_ALERTA, Pin.OUT)
buzzer = PWM(Pin(BUZZER_PIN))

# ------------------- FUNÇÃO: CODIFICAR URL ------------------
def url_encode(text):
    """
    Codifica texto para formato URL
    """
    encoded = ""
    for char in text:
        if char.isalnum() or char in "-_.~":
            encoded += char
        else:
            encoded += "%{:02x}".format(ord(char))
    return encoded

# ------------------- FUNÇÃO: CONECTAR WI-FI ------------------
def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print("Conectando ao Wi-Fi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        
        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
            print(".", end="")
        
        print()
        
        if wlan.isconnected():
            print("Conectado ao Wi-Fi!")
            print("IP:", wlan.ifconfig()[0])
            return True
        else:
            print("Falha ao conectar ao Wi-Fi.")
            return False
    else:
        print("Já conectado ao Wi-Fi.")
        return True

# ------------------- FUNÇÃO: TOCAR TOM NO BUZZER ------------------
def tocar_tom(frequencia, duracao_ms):
    """
    Toca um tom no buzzer usando PWM
    """
    buzzer.freq(frequencia)
    buzzer.duty_u16(32768)
    time.sleep_ms(duracao_ms)
    buzzer.duty_u16(0)

# ----------------- FUNÇÃO: ENVIAR ALERTA PARA WHATSAPP --------------------
def enviar_mensagem_whatsapp(mensagem):
    """
    Envia mensagem para WhatsApp usando CallMeBot API
    """
    try:
        # Codifica a mensagem para URL
        mensagem_codificada = url_encode(mensagem)
        
        # Monta a URL da API
        url = "https://api.callmebot.com/whatsapp.php?phone={}&text={}&apikey={}".format(
            WHATSAPP_PHONE, mensagem_codificada, WHATSAPP_API_KEY
        )
        
        print("[WhatsApp] Enviando mensagem...")
        resposta = urequests.get(url)
        
        if resposta.status_code == 200:
            print("[WhatsApp] ✓ Mensagem enviada: {}".format(mensagem))
        else:
            print("[WhatsApp] ✗ Erro: {} - {}".format(
                resposta.status_code, resposta.text
            ))
        
        resposta.close()
        
    except Exception as e:
        print("[WhatsApp] ✗ Erro ao enviar: {}".format(e))

# -------------------------- SETUP ---------------------------------
def setup():
    print("=" * 60)
    print("Módulo de presença da Fazenda Inteligente")
    print("Alertas via WhatsApp (CallMeBot)")
    print("=" * 60)
    
    # Conecta ao Wi-Fi
    if not conectar_wifi():
        print("AVISO: Wi-Fi não conectado. WhatsApp não funcionará.")
    
    # Garante que LED e buzzer estão desligados
    led_alerta.value(0)
    buzzer.duty_u16(0)
    
    print("\nSistema iniciado e pronto para detectar movimentos!")
    print("Mensagens serão enviadas para:", WHATSAPP_PHONE)
    print()

# -------------------------- LOOP PRINCIPAL ---------------------------------
def loop():
    global movimento_anterior
    
    while True:
        movimento_atual = pir.value()
        
        # Detecta mudança de estado
        if movimento_atual != movimento_anterior:
            if movimento_atual:
                print("⚠️  Movimento detectado dentro da estufa!")
                
                # Envia alerta para WhatsApp
                enviar_mensagem_whatsapp("🚨 ALERTA: Movimento detectado na área dos animais!")
                
                # Ativa LED e buzzer
                led_alerta.value(1)
                tocar_tom(300, 400)
            else:
                print("✓ Nenhum movimento.")
                led_alerta.value(0)
                buzzer.duty_u16(0)
            
            movimento_anterior = movimento_atual
        
        # Se há movimento constante, mantém LED ligado e buzzer ativo
        if movimento_atual:
            led_alerta.value(1)
            tocar_tom(300, 300)
            time.sleep_ms(500)
        
        time.sleep_ms(100)

# -------------------------- MAIN ---------------------------------
if __name__ == "__main__":
    try:
        setup()
        loop()
    except KeyboardInterrupt:
        print("\n\nPrograma interrompido pelo usuário.")
        led_alerta.value(0)
        buzzer.duty_u16(0)
        print("Sistema finalizado com segurança.")
    except Exception as e:
        print("\n\nErro no sistema: {}".format(e))
        led_alerta.value(0)
        buzzer.duty_u16(0)