from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException

# -------- CONFIGURAÇÕES DO MODBUS --------
IP = "192.168.0.10"   # ALTERAR para o IP do professor
PORT = 502
SLAVE = 2


# -------- FUNÇÃO DE CONEXÃO --------
def conectar():
    client = ModbusTcpClient(IP, port=PORT, timeout=2)
    if not client.connect():
        print("\n❌ ERRO: Não foi possível conectar ao servidor Modbus.")
        return None
    return client


# -------- FUNÇÕES DE OPERAÇÃO --------
def ligar_motor():
    try:
        client = conectar()
        if client is None:
            return
        resposta = client.write_register(address=1100, value=1, slave=SLAVE)
        if resposta.isError():
            print("❌ ERRO: Falha ao enviar comando para ligar o motor.")
        else:
            print("✔ Motor ligado.")
        client.close()
    except ModbusException as e:
        print(f"❌ Erro Modbus: {e}")


def desligar_motor():
    try:
        client = conectar()
        if client is None:
            return
        resposta = client.write_register(address=1100, value=0, slave=SLAVE)
        if resposta.isError():
            print("❌ ERRO: Falha ao enviar comando para desligar o motor.")
        else:
            print("✔ Motor desligado.")
        client.close()
    except ModbusException as e:
        print(f"❌ Erro Modbus: {e}")


def definir_sentido(horario=True):
    try:
        client = conectar()
        if client is None:
            return
        valor = 0 if horario else 1
        resposta = client.write_register(address=1101, value=valor, slave=SLAVE)
        if resposta.isError():
            print("❌ ERRO: Falha ao definir sentido.")
        else:
            print("✔ Sentido definido:", "Horário" if horario else "Anti-horário")
        client.close()
    except ModbusException as e:
        print(f"❌ Erro Modbus: {e}")


def definir_velocidade(freq):
    if freq < 1 or freq > 60:
        print("❌ Erro: a velocidade deve estar entre 1 e 60 Hz.")
        return
    try:
        client = conectar()
        if client is None:
            return
        resposta = client.write_register(address=41400, value=int(freq), slave=SLAVE)
        if resposta.isError():
            print("❌ ERRO: Falha ao definir velocidade.")
        else:
            print(f"✔ Velocidade definida para {freq} Hz.")
        client.close()
    except ModbusException as e:
        print(f"❌ Erro Modbus: {e}")


# -------- FUNÇÃO GENÉRICA DE LEITURA --------
def ler_reg(reg):
    try:
        client = conectar()
        if client is None:
            return None

        resposta = client.read_holding_registers(address=reg, count=1, slave=SLAVE)
        client.close()

        if resposta.isError():
            print(f"❌ ERRO: Falha ao ler registrador {reg}.")
            return None

        return resposta.registers[0]

    except ModbusException as e:
        print(f"❌ Erro Modbus: {e}")
        return None


# -------- FUNÇÕES DE LEITURA ESPECÍFICAS --------
def estado_motor():
    val = ler_reg(100)
    if val is not None:
        print("✔ Estado do motor:", "Girando" if val == 1 else "Parado")


def temperatura():
    val = ler_reg(30403)
    if val is not None:
        print("✔ Temperatura:", val, "°C")


def corrente():
    val = ler_reg(30401)
    if val is not None:
        print("✔ Corrente:", val, "A")


def tensao():
    val = ler_reg(30402)
    if val is not None:
        print("✔ Tensão:", val, "V")


def velocidade_atual():
    val = ler_reg(30400)
    if val is not None:
        print("✔ Velocidade:", val, "Hz")


# -------- CONFIGURAÇÃO PADRÃO --------
def iniciar_padrao():
    definir_velocidade(30)
    definir_sentido(horario=True)
    ligar_motor()


# ----------- MENU PRINCIPAL -----------
def menu():
    while True:
        print("\n===== MENU DO INVERSOR SENAI =====")
        print("1 - Ligar motor")
        print("2 - Desligar motor")
        print("3 - Definir velocidade")
        print("4 - Verificar temperatura")
        print("5 - Verificar corrente")
        print("6 - Verificar tensão")
        print("7 - Definir sentido de giro")
        print("8 - Verificar estado do motor")
        print("9 - Iniciar com configuração padrão")
        print("0 - Sair")
        op = input("Escolha: ")

        if op == "1":
            ligar_motor()
        elif op == "2":
            desligar_motor()
        elif op == "3":
            freq = float(input("Velocidade (1 a 60 Hz): "))
            definir_velocidade(freq)
        elif op == "4":
            temperatura()
        elif op == "5":
            corrente()
        elif op == "6":
            tensao()
        elif op == "7":
            sentido = input("0 = horário | 1 = anti-horário: ")
            definir_sentido(horario=(sentido == "0"))
        elif op == "8":
            estado_motor()
        elif op == "9":
            iniciar_padrao()
        elif op == "0":
            print("Encerrando programa...")
            break
        else:
            print("❌ Opção inválida.")


# INICIAR PROGRAMA
if __name__ == "__main__":
    menu()
