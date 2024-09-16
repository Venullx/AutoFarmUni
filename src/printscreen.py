import subprocess
import time
import os

def run_script(script_name):
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    if os.path.exists(script_path):
        subprocess.run(["python", script_path], check=True)
    else:
        print(f"Arquivo {script_name} não encontrado no caminho {script_path}")

class ScreenshotManager:
    def __init__(self, adb_device, screenshot_limit):
        # Define o caminho dinâmico para salvar as screenshots
        self.save_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images', 'screenshots', 'screen.png')
        self.adb_device = adb_device
        self.screenshot_limit = screenshot_limit
        self.screenshot_count = 0
        self.is_running = True

        # Cria o diretório para salvar as screenshots, se não existir
        os.makedirs(os.path.dirname(self.save_path), exist_ok=True)

    def start(self):
        """Inicia o processo de captura de screenshots."""
        while self.is_running:
            # Captura a screenshot do emulador e salva no diretório
            self.capture_screenshot()

            # Incrementa a contagem de screenshots
            self.screenshot_count += 1

            # Verifica se atingiu o limite de screenshots
            if self.screenshot_count >= self.screenshot_limit:
                self.delete_emulator_screenshots()
                self.screenshot_count = 0

            # Espera 1 segundo antes de capturar a próxima screenshot
            #time.sleep(1)

    def stop(self):
        """Para o processo de captura de screenshots."""
        self.is_running = False
        print("Captura parada.")

    def capture_screenshot(self):
        """Captura a screenshot do emulador e salva localmente."""
        try:
            # Comando para capturar a tela no emulador
            adb_screencap = f"adb -s {self.adb_device} shell screencap -p /sdcard/screen.png"
            subprocess.run(adb_screencap, check=True, shell=True)

            # Comando para puxar a imagem do emulador para o PC
            adb_pull = f"adb -s {self.adb_device} pull /sdcard/screen.png {self.save_path}"
            subprocess.run(adb_pull, check=True, shell=True)

        except subprocess.CalledProcessError as e:
            print(f"Erro ao capturar ou salvar a screenshot: {e}")
        except Exception as e:
            print(f"Erro inesperado ao capturar ou salvar a screenshot: {e}")

    def delete_emulator_screenshots(self):
        """Deleta a screenshot armazenada no emulador após atingir o limite."""  
        try:
            adb_delete = f"adb -s {self.adb_device} shell rm /sdcard/screen.png"
            subprocess.run(adb_delete, check=True, shell=True)
        except subprocess.CalledProcessError as e:
            print(f"Erro ao deletar a screenshot no emulador: {e}")
        except Exception as e:
            print(f"Erro inesperado ao deletar a screenshot no emulador: {e}")