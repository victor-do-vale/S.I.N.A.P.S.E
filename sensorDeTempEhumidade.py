from machine import I2C, Pin
from time import sleep
from dht import DHT22
from pico_i2c_lcd import I2cLcd

# ====== CONFIGURAÇÃO DO LED ======
led_alerta = Pin(14, Pin.OUT)   # LED no pino GP14 (altere se necessário)

# ====== LIMITES DE SEGURANÇA ======
TEMP_MAX = 28       # Temperatura máxima permitida
UMID_MAX = 80       # Umidade máxima permitida

# ====== CONFIGURAÇÃO DO SENSOR DHT22 ======
sensor = DHT22(Pin(15))

# ====== CONFIGURAÇÃO DO LCD ======
i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=400000)
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

# Mensagem inicial
lcd.putstr("Iniciando sensor...")
sleep(2)
lcd.clear()

# ====== LOOP PRINCIPAL ======
while True:
    sensor.measure()
    temp = sensor.temperature()
    umid = sensor.humidity()

    # ==== LÓGICA DO LED ====
    if temp > TEMP_MAX or umid > UMID_MAX:
        led_alerta.value(1)  # Liga LED (alerta)
    else:
        led_alerta.value(0)  # Desliga LED

    # ==== MOSTRA NO LCD ====
    lcd.clear()
    lcd.putstr(f"Temp: {temp:.2f} C")
    lcd.move_to(0, 1)
    lcd.putstr(f"Umid: {umid:.1f}%")

    sleep(2) 
