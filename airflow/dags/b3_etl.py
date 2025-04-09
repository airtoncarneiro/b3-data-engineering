from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from datetime import timedelta
import logging
import src.config.logging_config as log
from typing import Dict, Any
from pathlib import Path
import os

from src.services.downloader import Downloader
from src.services.file_handler import FileHandler
from src.services.zip_extractor import ZipExtractor

# Define save_dir
save_dir = os.path.join(os.path.dirname(__file__), "downloads")
os.makedirs(save_dir, exist_ok=True)

# Configuração do logging
log.logging.basicConfig()


# Configuração de Header e Trailing no logging
def log_banner(mensagem: str, tipo: str = "info"):
    borda = "=" * 80
    msg = f"\n{borda}\n📢 {mensagem}\n{borda}\n"
    getattr(logging, tipo)(msg)


# 🚀 Wrappers com @task para o Airflow
@task
def download_zip_file() -> str:
    downloader = Downloader()
    zip_data = downloader._download_zip_file()
    saved_path = FileHandler._save_file_to_disk(zip_data, save_dir)
    return saved_path

@task
def extract_zip_file(zip_path: str) -> Dict[str, Any]:
    zip_name = Path(zip_path).stem
    zip_dir = Path(zip_path).parent
    extract_dir = f"{zip_dir}/extracted_txt/{zip_name}"
    
    extractor = ZipExtractor(extract_dir)  # Agora é um diretório válido
    result = extractor._extract_zip_file(zip_path)
    return result

# Flag para debug com base na variável de ambiente
DEBUG_MODE = os.environ.get("DEBUG_MODE", "false").lower() == "true"

# 📅 DAG do Airflow
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
}
dag_name = "b3_etl"
@dag(
    dag_id=dag_name,
    default_args=default_args,
    schedule=None,
    start_date=days_ago(1),
    catchup=False,
    tags=["b3", "etl", "v4"],
    description="Pipeline híbrido testável como DAG ou script Python (debugável)"
)
def final_download_and_extract_zip():
    if DEBUG_MODE:
        # Modo debug: executa as funções diretamente para possibilitar o teste
        downloaded = download_zip_file.function()
        extracted = extract_zip_file.function(downloaded) # type: ignore
    else:
        # Modo Airflow: cria as tasks e suas dependências, permitindo a visualização do gráfico
        downloaded = download_zip_file()
        extracted = extract_zip_file(downloaded) # type: ignore
    return extracted

log_banner(f"INICIANDO DAG: {dag_name}")
dag = final_download_and_extract_zip()
log_banner(f"FINALIZOU DAG: {dag_name}")
