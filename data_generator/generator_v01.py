import json
import time
import random
from datetime import datetime
import urllib.request
import urllib.error

# ==============================================================================
# CONFIGURAÇÃO DIRETA (Insira os seus dados do Databricks aqui)
# ==============================================================================
DATABRICKS_HOST = "https://databricks.com"
DATABRICKS_TOKEN = "8c72518723123bdcf5ea3d765b845237d19194aaa87c84c3f51f5fce01c32a4a" 
# ==============================================================================

def generate_sensor_data():
    """Gera os dados sintéticos em formato de dicionário simulando sensores IoT urbanos."""
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
    url = f"{DATABRICKS_HOST}/api/2.0/dbfs/put"
    
    # Prepara o corpo da requisição multipart exigido pela API do Databricks
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    parts = []
    
    parts.append(f"--{boundary}")
    parts.append('Content-Disposition: form-data; name="path"')
    parts.append('')
    parts.append(f"/mnt/pulsecity/stage/{file_name}")
    
    parts.append(f"--{boundary}")
    parts.append('Content-Disposition: form-data; name="contents"')
    parts.append('')
    parts.append(json.dumps(payload))
    
    parts.append(f"--{boundary}")
    parts.append('Content-Disposition: form-data; name="overwrite"')
    parts.append('')
    parts.append("true")
    parts.append(f"--{boundary}--")
    parts.append('')
    
    body = "\r\n".join(parts).encode('utf-8')
    
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

if __name__ == "__main__":
    print("="*60)
    print(" LANÇANDO SIMULADOR DE STREAMING: PULSECITY-URBAN ")
    print(" Enviando ficheiros JSON a cada 3 segundos... (Pressione Ctrl+C para parar)")
    print("="*60)
    
    try:
        while True:
            data = generate_sensor_data()
            file_name = f"traffic_{int(time.time() * 1000)}.json"
            
            upload_to_databricks(file_name, data)
            time.sleep(3)
            
    except KeyboardInterrupt:
        print("\n Simulador interrompido com sucesso pelo utilizador.")
