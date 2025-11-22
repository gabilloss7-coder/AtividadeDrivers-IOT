
#TESTE BÁSICO MODBUS TCP pymodbus
#Lê e escreve um registrador simples para testar a comunicação.


from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException

IP = "192.168.0.10"  # altere para o IP do inversor / PC do professor
PORT = 502
SLAVE = 2            # endereço Modbus

def main():
    print("👌 Testando Modbus TCP pymodbus...")

    try:
        # Cria cliente
        client = ModbusTcpClient(IP, port=PORT, timeout=2)

        # Tenta conectar
        if not client.connect():
            print("Não conectou ao servidor Modbus.")
            return

        print("✔ Conectado!")

        # Escreve valor 1 no registrador 1100
        print("➡ Enviando write_register(1100, 1)...")
        resp = client.write_register(address=1100, value=1, slave=SLAVE)

        if resp.isError():
            print("Erro ao escrever registrador.")
        else:
            print("✔ Escrita bem-sucedida!")

        # Lê o registrador
        print("➡ Lendo registrador 1100...")
        resp = client.read_holding_registers(address=1100, count=1, slave=SLAVE)

        if resp.isError():
            print("Erro ao ler registrador.")
        else:
            print("✔ Leitura OK! Valor lido:", resp.registers[0])

        # Finaliza conexão
        client.close()

    except ModbusException as e:
        print("Erro Modbus:", e)
    except Exception as e:
        print("Erro inesperado:", e)


if __name__ == "__main__":
    main()
