import subprocess
import os

def click(x, y, device_id):
    """
    Executa um clique automático na posição (x, y) no dispositivo especificado usando o comando adb.

    :param x: Coordenada x para o clique.
    :param y: Coordenada y para o clique.
    :param device_id: ID do dispositivo ADB para realizar o clique.
    """
    # Comando adb para simular o clique
    command = f'adb -s {device_id} shell input tap {x} {y}'
    
    # Executa o comando
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o comando: {e}")