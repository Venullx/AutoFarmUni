# verificado
import subprocess

def list_adb_devices():
    """Executa o comando 'adb devices' e retorna os dispositivos encontrados como uma string."""
    try:
        # Executa o comando adb devices
        result = subprocess.run(["adb", "devices"], capture_output=True, text=True, check=True)
        
        # Captura a saída do comando
        output = result.stdout.strip()
        
        # Se a saída estiver em branco, exibe uma mensagem apropriada
        if not output:
            return ""

        # Divide a saída em linhas
        lines = output.split('\n')
        
        # Remove a primeira linha (cabeçalho)
        device_lines = lines[1:]
        
        # Verifica se há dispositivos conectados
        if not device_lines or device_lines[0].strip() == "":
            return ""
        else:
            return "\n".join(device_lines)
            
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o comando adb: {e}")
        return ""
