import json
import time
import random
from datetime import datetime, timezone
import os

# --- DEFINIÇÃO DO CAMINHO DO VOLUME DO UNITY CATALOG ---
STAGE_PATH = "/Volumes/pulsecity/bronze/stage_volume"

# Cria uma subpasta 'json_stream' dentro do volume para manter a organização
STREAM_DIR = os.path.join(STAGE_PATH, "json_stream")
os.makedirs(STREAM_DIR, exist_ok=True)
# --------------------------------------------------------

def generate_sensor_data():
    """Simula a geração de dados de telemetria de sensores IoT urbanos."""
    sensors = ["SENSOR_AVEIRO_01", "SENSOR_PORTO_02", "SENSOR_LISBOA_03", "SENSOR_COIMBRA_04"]
    now_utc = datetime.now(timezone.utc)
    
    return {
        "sensor_id": random.choice(sensors),
        "timestamp": now_utc.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
        "vehicle_count": random.randint(5, 60),
        "average_speed_kmh": round(random.uniform(15.0, 85.0), 1),
        "co2_level_ppm": random.randint(320, 580)
    }

if __name__ == "__main__":
    print("="*60, flush=True)
    print(" INICIANDO SIMULADOR DE STREAMING NO DATABRICKS: PULSECITY-URBAN ", flush=True)
    print(f" Destino (Unity Catalog Volume): {STREAM_DIR}", flush=True)
    print("="*60, flush=True)
    
    execucoes = 0
    max_execucoes = 100  
    
    try:
        while execucoes < max_execucoes:
            data = generate_sensor_data()
            
            file_name = f"traffic_{int(time.time() * 1000)}.json"
            full_path = os.path.join(STREAM_DIR, file_name)
            
            # Gravação nativa usando POSIX do Python diretamente no Volume
            with open(full_path, "w", encoding="utf-8") as f:
                json.dump(data, f)
                
            print(f" [OK] -> Arquivo gravado no Volume: {file_name}", flush=True)
            
            execucoes += 1
            time.sleep(3)  
            
    except KeyboardInterrupt:
        print("\n[AVISO] Simulador interrompido manualmente.", flush=True)
        
    print(f"\n[FIM] Carga simulada finalizada com {execucoes} arquivos.", flush=True)
