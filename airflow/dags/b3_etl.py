from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator
from airflow.utils.task_group import TaskGroup
from airflow.utils.trigger_rule import TriggerRule
from airflow.models import Variable
from datetime import timedelta
import pendulum
from typing import List, Optional
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
def extract_zip_files(zip_paths: str) -> List[str]:
    from src.services import ZipExtractor
    logger = logging.getLogger("airflow.task")
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
    return [f"COTAHIST_A{ano}.ZIP" for ano in range(ano_inicial, ano_execucao + 1)]


@task(trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS)
def merge_list(
    lista_diaria: Optional[List[str]] = None,
    lista_anual: Optional[List[str]] = None,
) -> List[str]:
    return lista_diaria or lista_anual or []


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
    start_date=pendulum.today("UTC").add(days=-1),
    catchup=False,
    description=(
        "DAG para download de séries da B3.\n"
        "Variáveis esperadas:\n"
        "- B3_CONFIG_DOWNLOAD_SERIE: tipo de série a ser baixada (padrão: series_anuais)\n"
        "- B3_CONFIG_DOWNLOAD_SERIE_ANUAL_DESDE_DE: ano inicial para séries anuais\n"
    ),
    tags=["b3", "etl", "v3"],
)
def b3_etl():
    @task.branch(task_id="tipo_serie")
    def tipo_serie_choice() -> str:
        cfg = Variable.get("B3_CONFIG_DOWNLOAD_SERIE", default_var="series_anuais").lower()
        return "grupo_diario.download_diario" if cfg == "serie_diaria" else "grupo_anual.download_anual"

    inicio = EmptyOperator(task_id="inicio")
    fim = EmptyOperator(task_id="fim")
    tipo_serie = tipo_serie_choice()

    with TaskGroup(group_id="grupo_diario") as grupo_diario:
        arquivos_diarios = serie_diaria.override(task_id="download_diario")()

    with TaskGroup(group_id="grupo_anual") as grupo_anual:
        arquivos_anuais = series_anuais.override(task_id="download_anual")()
    
    lista_final = merge_list(arquivos_diarios, arquivos_anuais) # type: ignore
    downloads = download_zip_file.expand(file_to_download=lista_final)
    extracoes = extract_zip_files.expand(zip_paths=downloads)

    inicio >> tipo_serie # type: ignore
    tipo_serie >> grupo_diario # type: ignore
    tipo_serie >> grupo_anual # type: ignore
    lista_final >> downloads >> extracoes >> fim # type: ignore


dag = b3_etl()

if __name__ == "__main__":
    dag.test()
