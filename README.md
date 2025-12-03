# S.I.N.A.P.S.E
# Projeto Fazenda Inteligente 
Codigos comentados.
Sistema automatizado para monitoramento ambiental e acionamento de segurança, projetado para proteger animais rurais dentro de estufas ou abrigos de criação. 
 
# Descrição do Projeto 
O sistema realiza automaticamente: 
- Controle de temperatura e umidade 
- Verificação do nível de água 
- Detecção de presença e segurança 
- Alertas visuais e sonoros 
 
Sensores coletam dados em tempo real, e atuadores são acionados com base em regras pré-programadas. Código de alarme de segurança envia uma mensagem pelo whatsapp para o usuário. 
 
# Hardware Utilizado 
COMPONENTE | FUNÇÃO 
Raspberry Pi Pico (ou ESP32) | Microcontrolador principal 
DHT22 | Temperatura e umidade 
PIR HC-SR501 | Detecção de movimento 
HC-SR04 | Medição de nível (reservatório) 
LED | Alerta visual 
Buzzer | Alerta sonoro 
 
# Pinagem 
PIR VCC → 3V3 do Pico 
PIR GND → GND do Pico 
PIR OUT → GP16 
LED (ânodo) → Resistor → GP15 
LED (catodo) → GND 
Buzzer VCC → GP17 
Buzzer GND → GND 

# Como Executar o Projeto 
1. Instale o MicroPython no microcontrolador. 
2. Envie os arquivos. 
3. Mudar linha 23 para seu número de whatsapp. 
4. Na linha 25 mudar chave da api. 
5. Na linha 29 e 30 colocar as configurações do seu próprio wi-fi. 
6. Conecte todos os sensores conforme a tabela de pinagem. 
7. Abra o Thonny ou outra IDE compatível. 
8. Execute os codigos. 
9. Observe no console os valores dos sensores e o acionamento dos atuadores. 
 
# Integração MQTT (Opcional) 
- Pode ser adicionada para permitir dashboards em tempo real. 
- Requer conexão Wi-Fi (ESP32 recomendado). 
 
# Objetivo Final 
Garantir bem-estar animal com automação segura, eficiente e de baixo custo. 
 
