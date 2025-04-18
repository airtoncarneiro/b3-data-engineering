from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator
from airflow.utils.task_group import TaskGroup
from airflow.utils.dates import days_ago
from airflow.utils.trigger_rule import TriggerRule
from airflow.models import Variable
from datetime import timedelta
import pendulum
from typing import List
from pathlib import Path
import os
import logging


@task
def download_zip_file(file_to_download: str) -> str:
    from src.services import Downloader, FileHandler
    logger = logging.getLogger("airflow.task")
    save_dir = os.path.join(os.path.dirname(__file__), "downloads")
    downloader = Downloader(logger=logger)
    downloaded_file = downloader._download_zip_file(file_to_download)
    saved_path = FileHandler._save_file_to_disk(downloaded_file, save_dir, logger=logger)
    logger.info(f"Arquivo ZIP baixado e salvo em: {saved_path}")
    return saved_path

@task
def extract_zip_files(zip_paths: str) -> None:
# def extract_zip_files(zip_paths: List[str]) -> None:
    from src.services import ZipExtractor
    logger = logging.getLogger("airflow.task")
    # for zip_path in zip_paths:
    #     zip_name = Path(zip_path).stem
    #     zip_dir = Path(zip_path).parent
    #     extract_dir = f"{zip_dir}/extracted_txt/{zip_name}"
    #     extractor = ZipExtractor(extract_dir)
    #     result = extractor._extract_zip_file(zip_path, logger=logger)
    #     logger.info(f"Arquivo ZIP extraído: {result['extracted_files']}")
    zip_path = zip_paths
    zip_name = Path(zip_path).stem
    zip_dir = Path(zip_path).parent
    extract_dir = f"{zip_dir}/extracted_txt/{zip_name}"
    extractor = ZipExtractor(extract_dir)
    result = extractor._extract_zip_file(zip_path, logger=logger)
    logger.info(f"Arquivo ZIP extraído: {result['extracted_files']}")
    return result["extracted_files"]

@task
def serie_diaria(**context) -> List[str]:
    execution_date = context["execution_date"]
    dia_anterior = execution_date - timedelta(days=1)
    nome_arquivo = dia_anterior.strftime("COTAHIST_D%d%m%Y.ZIP")
    return [nome_arquivo]

@task
def series_anuais(**context) -> List[str]:
    execution_date = context["execution_date"]
    ano_execucao = execution_date.year

    try:
        ano_inicial_str = Variable.get("B3_CONFIG_DOWNLOAD_SERIE_ANUAL_DESDE_DE")
        ano_inicial = int(ano_inicial_str)
    except KeyError:
        ano_inicial = ano_execucao

    arquivos = [f"COTAHIST_A{ano}.ZIP" for ano in range(ano_inicial, ano_execucao + 1)]
    return arquivos

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=1),
}
@dag(
    dag_id="b3_etl",
    default_args=default_args,
    schedule=None,
    start_date=pendulum.today('UTC').add(days=-1),
    catchup=False,
    description=(
        "DAG para download de séries da B3.\n"
        "Variáveis esperadas:\n"
        "- B3_CONFIG_DOWNLOAD_SERIE: tipo de série a ser baixada (padrão: series_anuais)\n"
        "                            após a primeira execução, o valor será serie_diaria\n"
        "- B3_SERIE_ANUAL_DESDE_DE: ano inicial para as séries anuais\n"
        "\n"
        "Exemplo: Se B3_SERIE_ANUAL_DESDE_DE for '2023' e a DAG executar em 2025, "
        "os arquivos COTAHIST_A2023.ZIP, COTAHIST_A2024.ZIP e COTAHIST_A2025.ZIP serão processados."
    ),
    tags=["b3", "etl", "v 1"],
)
def b3_etl():
    @task.branch(task_id="tipo_serie")
    def tipo_serie_choice():
        B3_CONFIG_DOWNLOAD_SERIE = Variable.get("B3_CONFIG_DOWNLOAD_SERIE", default_var="series_anuais").lower()     
        return "grupo_serie_diaria.download_diario" if B3_CONFIG_DOWNLOAD_SERIE == "serie_diaria" else "grupo_series_anuais.download_anual"

    # Tasks de controle
    inicio = EmptyOperator(task_id="inicio")
    fim = EmptyOperator(task_id="fim")
    tipo_serie = tipo_serie_choice()

    # Grupo para série diária
    with TaskGroup(group_id="grupo_serie_diaria") as grupo_diario:
        arquivos_diarios = serie_diaria.override(task_id="download_diario")()
        downloads_dia = download_zip_file.expand(file_to_download=arquivos_diarios)
        extrair_dia = extract_zip_files.expand(zip_paths=downloads_dia)
        arquivos_diarios >> downloads_dia >> extrair_dia # type: ignore

    # Grupo para séries anuais
    with TaskGroup(group_id="grupo_series_anuais") as grupo_anual:
        arquivos_anuais = series_anuais.override(task_id="download_anual")()
        downloads_ano = download_zip_file.expand(file_to_download=arquivos_anuais)
        extrair_ano = extract_zip_files.expand(zip_paths=downloads_ano)
        arquivos_anuais >> downloads_ano >> extrair_ano # type: ignore

    # Operador necessario pois quando o Airflow ignora um branch, ele não executa o fim
    # Com este merge informando o trigger_rule, o Airflow executa o fim
    merge = EmptyOperator(
        task_id="merge_paths",
        trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS,
    )
    inicio >> tipo_serie # type: ignore
    tipo_serie >> grupo_diario >> merge # type: ignore
    tipo_serie >> grupo_anual >> merge # type: ignore
    merge >> fim # type: ignore


dag = b3_etl()

if __name__ == "__main__":
    dag.test()
