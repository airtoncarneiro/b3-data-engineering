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

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

# Configuração de Header e Trailing no logging
def log_banner(mensagem: str, tipo: str = "info"):
    borda = "=" * 80
    msg = f"\n{borda}\n📢 {mensagem}\n{borda}\n"
    getattr(logging, tipo)(msg)

# 🚀 Wrappers com @task para o Airflow
@task
def download_zip_file() -> Dict[str, Any]:
    downloader = Downloader()
    zip_data = downloader._download_zip_file()
    return zip_data

@task
def save_file_to_disk(file_info: Dict[str, Any]) -> str:
    saved_path = FileHandler._save_file_to_disk(file_info, save_dir)
    return saved_path

@task
def extract_zip_file(zip_path: str) -> Dict[str, Any]:
    zip_name = Path(zip_path).stem
    zip_dir = Path(zip_path).parent
    extract_dir = f"{zip_dir}/extracted_txt/{zip_name}"
    
    extractor = ZipExtractor(extract_dir)  # Agora é um diretório válido
    result = extractor._extract_zip_file(zip_path)
    return result

# 📅 DAG do Airflow
dag_name = "b3_etl"
@dag(
    dag_id=dag_name,
    default_args=default_args,
    schedule=None,
    start_date=days_ago(1),
    catchup=False,
    tags=["download", "zip", "httpx", "hibrido"],
    description="Pipeline híbrido testável como DAG ou script"
)
def final_download_and_extract_zip():
    downloaded = download_zip_file.function()
    saved = save_file_to_disk.function(downloaded) # type: ignore
    extracted = extract_zip_file.function(saved) # type: ignore
    return extracted



log_banner(f"INICIANDO DAG: {dag_name}")
dag = final_download_and_extract_zip()
log_banner(f"FINALIZOU DAG: {dag_name}")
