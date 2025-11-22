"""
TESTE BÁSICO MODBUS TCP usando uModBus
Lê e escreve um registrador simples para testar comunicação.
"""

import socket
from umodbus import conf
from umodbus.client.tcp import write_single_register, read_holding_registers

IP = "192.168.0.10"  # altere para o IP do inversor / PC do professor
PORT = 502
SLAVE = 2            # endereço Modbus

# uModBus usa valores SEM sinal por padrão
conf.SIGNED_VALUES = False

def main():
    print("🔌 Testando Modbus TCP com uModBus...")

    try:
        # abre socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)

        try:
            sock.connect((IP, PORT))
            print("✔ Conectado!")
        except:
            print("❌ Falha ao conectar ao servidor Modbus.")
            return

        # 1) Escreve valor no registrador 1100
        print("➡ Enviando write_single_register(1100, 1)...")
        req = write_single_register(slave_id=SLAVE, address=1100, value=1)
        sock.send(req)

        # 2) Lê o registrador 1100
        print("➡ Lendo registrador 1100...")
        req = read_holding_registers(slave_id=SLAVE, starting_address=1100, quantity=1)
        sock.send(req)

        response = sock.recv(1024)  # recebe pacote Modbus

        if len(response) < 9:
            print("❌ Erro na resposta do servidor.")
        else:
            # O valor lido vem nos bytes finais
            value_high = response[-2]
            value_low = response[-1]
            value = value_high * 256 + value_low

            print("✔ Valor lido:", value)

        sock.close()

    except Exception as e:
        print("❌ Erro:", e)


if __name__ == "__main__":
    main()
