# Trabalho PUCPR
# Aluno: Murilo Vinicius Lunardon
import dht
import machine
import time
import urequests
from wifi_lib import conecta

# Atribui a leitura do DHT e do Rele
temperatura = dht.DHT11(machine.Pin(4))
rele = machine.Pin(2, machine.Pin.OUT)
# Iniciar o progama com o Rele desligado
rele.value(0)
# Inicia o monitoramento da Temperatura da umidade
while True:
    # Variavel que chama o DHT
    temperatura.measure()

    # Atribui os valores lidos dentro do Laço
    temp = (temperatura.temperature())
    umid = (temperatura.humidity())

    # Mostra os Valores da temperatura e humidade
    print("Temperatura: {}ºC, Umidade: {}%".format(temp, umid))
    time.sleep(3)
    print('*' * 50)
    # Se a temperatura tiver > 31 graus ou umidade > 70 acende o led
    if temp > 31 or umid > 70:
        rele.value(1)
    # Caso nao chegue no valor, o rele fica desligado
    else:
        rele.value(0)

    # Conceta ao wifi
    station = conecta("TESTE", "TESTE")
    if not station.isconnected():
        print("Não Conectado!...")
    else:
        print("Conectado!!")
        time.sleep(1)
        print('*' * 50)
        print("Acessando o ThingSpeak")
        print('*' * 50)
        resposta = urequests.get("https://api.thingspeak.com/update?api_key=5ZXCZRXDYHG3IDOU&field1={}&field2={}".format(temp, umid))
        print("Pagina Acessada:")
        print('*' * 50)
        print("Dados enviados com sucesso...!")
        print('*' * 50)
        print(resposta.text)
        time.sleep(1)
        station.disconnect()
