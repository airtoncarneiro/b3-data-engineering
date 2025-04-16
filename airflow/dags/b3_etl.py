from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator
from airflow.utils.task_group import TaskGroup
from airflow.utils.dates import days_ago
from datetime import timedelta
from typing import List
from pathlib import Path
import os
import logging

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=1),
}

@task
def download_zip_file(file_to_download: str) -> str:
    from src.services.downloader import Downloader
    from src.services.file_handler import FileHandler
    logger = logging.getLogger("airflow.task")
    save_dir = os.path.join(os.path.dirname(__file__), "downloads")
    # os.makedirs(save_dir, exist_ok=True)
    downloader = Downloader(logger=logger)
    downloaded_file = downloader._download_zip_file(file_to_download)
    saved_path = FileHandler._save_file_to_disk(downloaded_file, save_dir, logger=logger)
    logger.info(f"Arquivo ZIP baixado e salvo em: {saved_path}")
    return saved_path

@task
def extract_zip_files(zip_paths: List[str]) -> None:
    from src.services.zip_extractor import ZipExtractor
    logger = logging.getLogger("airflow.task")
    for zip_path in zip_paths:
        zip_name = Path(zip_path).stem
        zip_dir = Path(zip_path).parent
        extract_dir = f"{zip_dir}/extracted_txt/{zip_name}"
        extractor = ZipExtractor(extract_dir)
        result = extractor._extract_zip_file(zip_path, logger=logger)
        logger.info(f"Arquivo ZIP extraído: {result['extracted_files']}")

@task
def serie_diaria() -> List[str]:
    return ['COTAHIST_D01042025.ZIP']

@task
def series_anuais() -> List[str]:
    return ['COTAHIST_A2024.ZIP', 'COTAHIST_A2025.ZIP']

@dag(
    dag_id="b3_etl",
    default_args=default_args,
    schedule=None,
    start_date=days_ago(1),
    catchup=False,
    tags=["b3", "etl"],
)
def b3_etl():
    @task.branch(task_id="tipo_serie")
    def tipo_serie_choice():
        from airflow.models import Variable
        b3_download_serie = Variable.get("B3_DOWNLOAD_SERIE", default_var="series_anuais").lower()
        if b3_download_serie == "serie_diaria":
            return "grupo_diario.download_diario"
        else:
            return "grupo_anual.download_anual"

    # Nós de controle
    inicio = EmptyOperator(task_id="inicio")
    fim = EmptyOperator(task_id="fim")

    tipo_serie = tipo_serie_choice()

    # Grupo para série diária
    with TaskGroup(group_id="grupo_diario") as grupo_diario:
        arquivos_diarios = serie_diaria.override(task_id="download_diario")()
        with TaskGroup(group_id="downloads_diarios") as downloads_diarios:
            downloads_dia = download_zip_file.expand(file_to_download=arquivos_diarios)
        extrair_dia = extract_zip_files(downloads_dia)
        arquivos_diarios >> downloads_diarios >> extrair_dia

    # Grupo para séries anuais
    with TaskGroup(group_id="grupo_anual") as grupo_anual:
        arquivos_anuais = series_anuais.override(task_id="download_anual")()
        with TaskGroup(group_id="downloads_anuais") as downloads_anuais:
            downloads_ano = download_zip_file.expand(file_to_download=arquivos_anuais)
        extrair_ano = extract_zip_files(downloads_ano)
        arquivos_anuais >> downloads_anuais >> extrair_ano

    # Conexões
    inicio >> tipo_serie
    tipo_serie >> grupo_diario >> fim
    tipo_serie >> grupo_anual >> fim

dag = b3_etl()

if __name__ == "__main__":
    dag.test()