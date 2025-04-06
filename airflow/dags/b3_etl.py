from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from datetime import timedelta
import logging
from typing import Dict, Any
from libs.b3_utils import download_zip_file as _download_zip_file
from libs.b3_utils import save_file_to_disk as _save_file_to_disk
from libs.b3_utils import extract_zip_file as _extract_zip_file

# Configuração do logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

# 🚀 Wrappers com @task para o Airflow
@task
def download_zip_file() -> Dict[str, Any]:
    return _download_zip_file()

@task
def save_file_to_disk(file_info: Dict[str, Any]) -> str:
    return _save_file_to_disk(file_info)

@task
def extract_zip_file(zip_path: str) -> Dict[str, Any]:
    return _extract_zip_file(zip_path)

# 📅 DAG do Airflow
@dag(
    dag_id="b3_etl",
    default_args=default_args,
    schedule=None,
    start_date=days_ago(1),
    catchup=False,
    tags=["download", "zip", "httpx", "hibrido"],
    description="Pipeline híbrido testável como DAG ou script"
)
def final_download_and_extract_zip():
    file_info = download_zip_file()
    file_path = save_file_to_disk(file_info) # type: ignore
    extract_info = extract_zip_file(file_path) # type: ignore

if __name__ != "__main__":
    # 🎯 Execução direta no Airflow
    logging.info("Executando DAG pelo Airflow.")
    dag = final_download_and_extract_zip()
else:
    # 🎯 Execução direta no Python
    logging.info("Executando como script Python puro...")
    file_info = _download_zip_file()
    file_path = _save_file_to_disk(file_info)
    extract_info = _extract_zip_file(file_path)
    print(f"✅ Extração concluída: {extract_info['total_files']} arquivos extraídos.")
    print(f"📦 Arquivo ZIP: {file_info['filename']}")
    print(f"📂 Arquivos extraídos:")
    for arq in extract_info['extracted_files']:
        print(f" - {arq}")
    print(f"📁 Diretório de extração: {extract_info['extract_path']}")
