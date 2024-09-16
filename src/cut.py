from PIL import Image
import os
from concurrent.futures import ThreadPoolExecutor

def cut_image(image_path, output_path, coordinates):
    """Corta uma imagem com base nas coordenadas fornecidas e salva o resultado."""
    try:
        if not os.path.exists(image_path):
            print(f"Arquivo não encontrado: {image_path}")
            return

        img = Image.open(image_path)
        left, upper, width, height = coordinates
        right = left + width
        lower = upper + height

        cropped_img = img.crop((left, upper, right, lower))
        cropped_img.save(output_path)

    except Exception as e:
        print(f"Erro ao cortar a imagem {image_path}: {e}")

def process_images_parallel(image_path, output_folder, coordinates_list):
    """Processa múltiplos cortes de imagem em paralelo."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with ThreadPoolExecutor() as executor:
        futures = []
        for i, coords in enumerate(coordinates_list):
            output_path = os.path.join(output_folder, f"slice_{i+1}.png")
            futures.append(executor.submit(cut_image, image_path, output_path, coords))
        for future in futures:
            future.result()  # Espera que todos os cortes sejam concluídos

# Defina o caminho base como o diretório principal (AutoFarm)
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Construa os caminhos dinâmicos corretos
image_path = os.path.join(base_dir, 'images', 'screenshots', 'screen.png')
output_folder = os.path.join(base_dir, 'images', 'screenshots', 'cropped')

# Lista de coordenadas para cortar a imagem
coordinates_list = [
    (82, 782, 20, 20), # symbol quest
    (31, 582, 20, 10), # AP quest
    (375, 655, 20, 20), # Again
    (432, 771, 20, 20), # skills
    (222, 781, 20, 20), # OK
    (177, 469, 20, 20), # JMV
    (368, 465, 20, 20) # Recovery AP
]

# Processar as imagens
process_images_parallel(image_path, output_folder, coordinates_list)
