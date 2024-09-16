from PIL import Image
import numpy as np
import os

def matchimage(path_img1, path_img2):
    """
    Compara duas imagens para verificar se são iguais.

    :param path_img1: Caminho para a primeira imagem.
    :param path_img2: Caminho para a segunda imagem.
    :return: Retorna True se as imagens forem iguais, False caso contrário.
    """
    if not (os.path.exists(path_img1) and os.path.exists(path_img2)):
        print(f"Uma ou ambas as imagens não existem:\n{path_img1}\n{path_img2}")
        return False

    try:
        img1 = Image.open(path_img1)
        img2 = Image.open(path_img2)
    except (IOError, SyntaxError) as e:
        print(f"Erro ao abrir as imagens: {e}")
        return False

    img1 = img1.convert('RGB')
    img2 = img2.convert('RGB')

    if img1.size != img2.size:
        print("Imagens não possuem as mesmas dimensões.")
        return False

    arr1 = np.array(img1)
    arr2 = np.array(img2)

    if np.array_equal(arr1, arr2):
        return True
    else:
        return False

def compare_images(base_image_path, cropped_images_dir):
    """
    Compara a imagem base com todas as imagens cortadas no diretório especificado.

    :param base_image_path: Caminho para a imagem base.
    :param cropped_images_dir: Diretório contendo as imagens cortadas.
    """
    if not os.path.exists(base_image_path):
        print(f"A imagem base não existe: {base_image_path}")
        return

    if not os.path.exists(cropped_images_dir):
        return

    for file_name in os.listdir(cropped_images_dir):
        if file_name.endswith(".png"):
            cropped_image_path = os.path.join(cropped_images_dir, file_name)
            print(f"Comparando com {file_name}...")
            matchimage(base_image_path, cropped_image_path)

if __name__ == "__main__":
    current_directory = os.getcwd()
    base_image_path = os.path.join(current_directory, 'images', 'base', 'base_image.png')  # Caminho da imagem base
    cropped_images_dir = os.path.join(current_directory, 'images', 'cropped')  # Diretório das imagens cortadas

    compare_images(base_image_path, cropped_images_dir)
