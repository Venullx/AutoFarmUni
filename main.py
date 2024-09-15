import tkinter as tk
from tkinter import messagebox
import threading
import subprocess
import os
import time
import sys
from src.finddevice import list_adb_devices
from src.printscreen import ScreenshotManager

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoFarm - Your Hero")
        self.root.geometry("300x300")

        # Controle de threads em execução
        self.screenshot_done = False
        self.monitoring_thread = None

        # Tela inicial com o botão "Start"
        self.start_button = tk.Button(self.root, text="Start", command=self.start_app)
        self.start_button.pack(pady=50)

    def start_app(self):
        # Limpa a tela
        for widget in self.root.winfo_children():
            widget.destroy()

        # Botão "Find devices"
        self.find_button = tk.Button(self.root, text="Find devices", command=self.show_devices)
        self.find_button.pack(pady=50)

    def show_devices(self):
        # Limpa a tela novamente
        for widget in self.root.winfo_children():
            widget.destroy()

        # Exibe os dispositivos encontrados em uma lista
        devices = self.get_adb_devices()
        
        if not devices:
            messagebox.showerror("Erro", "Nenhum dispositivo encontrado.")
            return

        self.device_listbox = tk.Listbox(self.root, height=10, width=40)
        self.device_listbox.pack(pady=20)
        for device in devices.splitlines():
            self.device_listbox.insert(tk.END, device)

        self.device_listbox.bind('<Double-1>', self.select_device)

    def get_adb_devices(self):
        # Captura a saída do comando "adb devices" e retorna uma lista de dispositivos
        devices = list_adb_devices()
        if devices:
            return devices
        else:
            return []

    def select_device(self, event):
        # Captura o dispositivo selecionado
        widget = event.widget
        selected_index = widget.curselection()
        if selected_index:
            device_info = widget.get(selected_index[0])
            device_id = device_info.split()[0]  # Obtém apenas o ID do dispositivo

            # Armazena o ID do dispositivo em um arquivo para uso futuro
            with open("device_selected.txt", "w") as file:
                file.write(device_id)

            # Limpa a tela e exibe os botões "Start" e "Exit"
            self.device_selected_screen(device_id)

    def device_selected_screen(self, device):
        # Limpa a tela
        for widget in self.root.winfo_children():
            widget.destroy()

        # Exibe o dispositivo selecionado
        device_label = tk.Label(self.root, text=f"Dispositivo: {device}")
        device_label.pack(pady=20)

        # Botão "Start"
        start_button = tk.Button(self.root, text="Start", command=lambda: self.start_screenshot_manager(device))
        start_button.pack(pady=10)

        # Botão "Exit"
        exit_button = tk.Button(self.root, text="Exit", command=self.exit_app)
        exit_button.pack(pady=10)

    def start_screenshot_manager(self, device):
        # Inicia a captura de screenshots em uma thread separada
        screenshot_limit = 10  #limite de screenshots

        # Cria um arquivo para sinalizar a conclusão da captura
        self.screenshot_done = False

        # Define uma função para monitorar a captura
        def monitor_capture():
            while not self.screenshot_done:
                time.sleep(1)  # Espera um segundo

        # Inicia o monitoramento
        self.monitoring_thread = threading.Thread(target=monitor_capture)
        self.monitoring_thread.start()

        # Inicia a captura de screenshots
        manager = ScreenshotManager(adb_device=device, screenshot_limit=screenshot_limit)
        threading.Thread(target=self.run_screenshot_manager, args=(manager,)).start()

        # Espera até a captura de screenshots e processa continuamente as novas capturas
        self.root.after(1000, self.process_screenshots)

    def run_screenshot_manager(self, manager):
        # Executa o ScreenshotManager e sinaliza quando terminar
        manager.start()
        self.screenshot_done = True

    def process_screenshots(self):
        # Chama o script de corte de imagem após a captura das screenshots
        try:
            screenshots_dir = os.path.join(os.getcwd(), 'images', 'screenshots')
            latest_screenshot = max(
                (os.path.join(screenshots_dir, f) for f in os.listdir(screenshots_dir)),
                key=os.path.getctime
            )

            # Atualiza o caminho da imagem mais recente no cut.py
            subprocess.run(["python", "src/cut.py"], check=True, input=latest_screenshot, text=True)
        except subprocess.CalledProcessError as e:
            print(f"Erro ao executar o script cut.py: {e}")
            messagebox.showerror("Erro", "Erro ao processar as imagens cortadas.")
            return
        
        # Chama o script de comparação de imagem após o corte
        self.root.after(1000, self.compare_images)

    def compare_images(self):
        # Executa o actions.py para comparar a imagem base com as imagens cortadas
        try:
            subprocess.run(["python", "src/actions.py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Erro ao executar o script actions.py: {e}")
            messagebox.showerror("Erro", "Erro ao comparar as imagens.")
            return

        # Espera para processar novos screenshots ou realizar outras tarefas
        self.root.after(5000, self.process_screenshots)

    def exit_app(self):
        # Interrompe o loop e encerra o aplicativo completamente
        self.screenshot_done = True
        if self.monitoring_thread and self.monitoring_thread.is_alive():
            self.monitoring_thread.join()
        self.root.quit()
        os._exit(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
