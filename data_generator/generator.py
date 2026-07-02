import json
import time
import random
from datetime import datetime
import urllib.request
import urllib.error
import os


def load_env():
    """Lê o ficheiro .env local e carrega as variáveis no ambiente de forma nativa."""
    try:
        # Localiza o arquivo .env na raiz do projeto (um nível acima da pasta data_generator)
        env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
        if os.path.exists(env_path):
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    # Ignora linhas vazias ou comentários
                    if line.strip() and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        os.environ[key] = value.strip()
        else:
            print(" [AVISO] Ficheiro .env não encontrado na raiz do projeto.")
    except Exception as e:
        print(f" [ERRO] Falha ao carregar o ficheiro .env: {e}")

# Inicializa o carregamento das configurações de ambiente
load_env()

# Captura as credenciais diretamente do ambiente do sistema
DATABRICKS_HOST = os.environ.get("DATABRICKS_HOST")
DATABRICKS_TOKEN = os.environ.get("DATABRICKS_TOKEN")


def generate_sensor_data():
    """Gera os dados sintéticos em formato de dicionário simulando sensores IoT urbanos."""
    # Lista de localizações fixas para simular sensores reais
    sensors = ["SENSOR_AVEIRO_01", "SENSOR_PORTO_02", "SENSOR_LISBOA_03", "SENSOR_COIMBRA_04"]
    
    return {
        "sensor_id": random.choice(sensors),
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
        "vehicle_count": random.randint(5, 60),
        "average_speed_kmh": round(random.uniform(15.0, 85.0), 1),
        "co2_level_ppm": random.randint(320, 580)
    }


def upload_to_databricks(file_name, payload):
    """Envia o payload JSON diretamente para o DBFS do Databricks via API REST."""
    # Validação rápida de credenciais antes do envio
    if not DATABRICKS_HOST or not DATABRICKS_TOKEN:
        print(" [ERRO] DATABRICKS_HOST ou DATABRICKS_TOKEN não definidos no arquivo .env.")
        return

    url = f"{DATABRICKS_HOST}/api/2.0/dbfs/put"
    
    # Prepara o corpo da requisição multipart exigido pela API do Databricks
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    parts = []
    
    # Campo 1: Caminho de destino do ficheiro JSON no DBFS do Databricks
    parts.append(f"--{boundary}")
    parts.append('Content-Disposition: form-data; name="path"')
    parts.append('')
    parts.append(f"/mnt/pulsecity/stage/{file_name}")
    
    # Campo 2: O payload real em string JSON
    parts.append(f"--{boundary}")
    parts.append('Content-Disposition: form-data; name="contents"')
    parts.append('')
    parts.append(json.dumps(payload))
    
    # Campo 3: Opção para sobrescrever ficheiros idênticos (obrigatório pela API)
    parts.append(f"--{boundary}")
    parts.append('Content-Disposition: form-data; name="overwrite"')
    parts.append('')
    parts.append("true")
    parts.append(f"--{boundary}--")
    parts.append('')
    
    body = "\r\n".join(parts).encode('utf-8')
    
    # Configura os cabeçalhos HTTP padrões de autenticação do Databricks
    headers = {
        "Authorization": f"Bearer {DATABRICKS_TOKEN}",
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "Content-Length": str(len(body))
    }
    
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                print(f" [OK] {datetime.now().strftime('%H:%M:%S')} -> Enviado: {file_name}")
    except urllib.error.HTTPError as e:
        print(f" [ERRO HTTP] Falha ao enviar {file_name}: {e.code} - {e.read().decode('utf-8')}")
    except Exception as e:
        print(f" [ERRO CONEXÃO] Erro inesperado ao tentar comunicar com a API: {e}")


# Execução principal do loop de simulação
if __name__ == "__main__":
    print("="*60)
    print(" LANÇANDO SIMULADOR DE STREAMING: PULSECITY-URBAN ")
    print(" Enviando ficheiros JSON a cada 3 segundos... (Pressione Ctrl+C para parar)")
    print("="*60)
    
    try:
        while True:
            data = generate_sensor_data()
            # Gera um nome único para o ficheiro baseado em milissegundos epoc
            file_name = f"traffic_{int(time.time() * 1000)}.json"
            
            upload_to_databricks(file_name, data)
            time.sleep(3) # Pausa controlada entre envios
            
    except KeyboardInterrupt:
        print("\n Simulador interrompido com sucesso pelo utilizador.")
