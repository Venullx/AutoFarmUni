import os
import time
from matchimage import matchimage  # Certifique-se de que esta função está no mesmo diretório ou ajuste o caminho
from click import click  # Certifique-se de que a função click está no mesmo diretório ou ajuste o caminho

def read_device_id(file_path):
    """Lê o ID do dispositivo do arquivo de texto."""
    try:
        with open(file_path, 'r') as file:
            device_id = file.readline().strip()
        return device_id
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {file_path}")
        return None

def perform_actions(base_path, screen_path, device_id):
    """Executa uma série de ações com base na comparação de imagens."""
    
    # Obtém o caminho completo das imagens de base e de tela
    base_path = os.path.abspath(base_path)  # Converte para um caminho absoluto
    screen_path = os.path.abspath(screen_path)  # Converte para um caminho absoluto
    
    # Define os pares de imagens e as ações correspondentes (com tempos de espera)
    actions = [
        
        {
            "base": os.path.join(base_path, "base2.png"),
            "screen": os.path.join(screen_path, "cropped", "slice_2.png"),
            "clicks": [(45, 582, 1), (323, 462, 1), (236, 527, 1), (399, 677, 1), (306, 510, 1), (308, 257, 1), (395, 614, 0)] # AP quest
        },
        {
            "base": os.path.join(base_path, "base3.png"),
            "screen": os.path.join(screen_path, "cropped", "slice_3.png"),
            "clicks": [(399, 677, 1), (306, 510, 1), (308, 257, 1), (395, 614, 0)] # Again
        },
        {
            "base": os.path.join(base_path, "base4.png"),
            "screen": os.path.join(screen_path, "cropped", "slice_4.png"),
            "clicks": [(240, 760, 1), (423, 697, 1), (334, 671, 1), (236, 662, 1), (142, 674, 1), (240, 760, 1), (51, 699, 1), (42, 601, 1)] # skills
        },
        {
            "base": os.path.join(base_path, "base5.png"),
            "screen": os.path.join(screen_path, "cropped", "slice_5.png"),
            "clicks": [(178, 792, 3), (178, 792, 0), (178, 792, 5), (178, 792, 1), (238, 740, 3), (164, 499, 1), (241, 421, 1), (237, 505, 1), (109, 798, 2), (108,690,2),(103,808,2)] # OK
        },
        {
            "base": os.path.join(base_path, "base6.png"),
            "screen": os.path.join(screen_path, "cropped", "slice_6.png"),
            "clicks": [(238, 488, 1)] # JMV
        },
        {
            "base": os.path.join(base_path, "base7.png"),
            "screen": os.path.join(screen_path, "cropped", "slice_7.png"),
            "clicks": [(333, 499, 2), (310, 511, 2), (232, 490, 2), (394, 612, 2)] # Recovery AP
        },
        {
            "base": os.path.join(base_path, "base1.png"),
            "screen": os.path.join(screen_path, "cropped", "slice_1.png"),
            "clicks": [(106, 798, 0)]  # symbol quest
        },
    ]

    for action in actions:
        base_image = action["base"]
        screen_image = action["screen"]
        
        # Verifica se as imagens existem
        if not os.path.isfile(base_image):
            print(f"Imagem base não encontrada: {base_image}")
            continue
        if not os.path.isfile(screen_image):
            print(f"Imagem de tela não encontrada: {screen_image}")
            continue
        
        # Compara as imagens
        if matchimage(base_image, screen_image):

            for x, y, wait_time in action["clicks"]:
                click(x, y, device_id)  # Executa o clique
                time.sleep(wait_time)  # Aguarda o tempo especificado
    
        else:
            pass

if __name__ == "__main__":

    base_image_dir = os.path.join(os.getcwd(), "images", "base")
    screen_image_dir = os.path.join(os.getcwd(), "images", "screenshots") 

    # Caminho para o arquivo device_selected.txt
    device_id_file = os.path.join(os.getcwd(), "device_selected.txt")
    device_id = read_device_id(device_id_file)

    if device_id:
        perform_actions(base_image_dir, screen_image_dir, device_id)
    else:
        print("Não foi possível ler o device_id. Verifique o arquivo device_selected.txt.")
