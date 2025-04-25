from airflow.decorators import dag, task
from airflow.utils.trigger_rule import TriggerRule
from airflow.models.xcom_arg import XComArg
from typing import List, Union
from datetime import timedelta
import pendulum


@task
def download_zip_file(file_to_download: str, **context) -> str:
    import os
    import logging
    from src.services import Downloader, FileHandler

    logger = logging.getLogger("airflow.task")

    logger.info(f"Iniciando download do arquivo: {file_to_download}")

    execution_date = context["execution_date"]
    data_formatada = execution_date.strftime("%Y%m%d")

    save_dir = os.path.join(os.path.dirname(__file__), "downloads", data_formatada)

    os.makedirs(save_dir, exist_ok=True)
    logger.info(f"Diretório de salvamento criado/verificado: {save_dir}")

    downloader = Downloader(logger=logger)
    downloaded_file = downloader._download_zip_file(file_to_download)
    saved_path = FileHandler._save_file_to_disk(downloaded_file, save_dir, logger=logger)

    logger.info(f"Arquivo ZIP baixado e salvo em: {saved_path}")
    return saved_path


@task
def extract_zip_files(zip_paths: str) -> List[str]:
    import logging
    from pathlib import Path
    from src.services import ZipExtractor

    logger = logging.getLogger("airflow.task")

    logger.info(f"Iniciando extração do arquivo: {zip_paths}")

    zip_path = zip_paths
    zip_name = Path(zip_path).stem
    zip_dir = Path(zip_path).parent
    extract_dir = f"{zip_dir}/extracted_txt/{zip_name}"

    extractor = ZipExtractor(extract_dir)
    result = extractor._extract_zip_file(zip_path, logger=logger)

    logger.info(f"Arquivos extraídos para: {extract_dir} - Arquivos: {result['extracted_files']}")
    return result["extracted_files"]


@task
def serie_diaria(**context) -> List[str]:
    import logging
    logger = logging.getLogger("airflow.task")

    execution_date = context["execution_date"]
    dia_anterior = execution_date - timedelta(days=1)
    nomes_arquivos = [dia_anterior.strftime("COTAHIST_D%d%m%Y.ZIP")]

    logger.info(f"Nome de arquivo diário gerado: {nomes_arquivos}")

    return nomes_arquivos


@task
def series_anuais(**context) -> List[str]:
    import logging
    logger = logging.getLogger("airflow.task")

    from airflow.models import Variable

    execution_date = context["execution_date"]
    ano_execucao = execution_date.year
    try:
        ano_inicial_str = Variable.get("B3_CONFIG_DOWNLOAD_SERIE_ANUAL_DESDE_DE")
        ano_inicial = int(ano_inicial_str)
    except KeyError:
        ano_inicial = ano_execucao

    nomes_arquivos = [f"COTAHIST_A{ano}.ZIP" for ano in range(ano_inicial, ano_execucao + 1)]

    logger.info(f"Nomes de arquivos anuais gerados: {nomes_arquivos}")

    return nomes_arquivos


@task(trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS)
def merge_list(
    lista_diaria: Union[List[str], XComArg, None] = None,
    lista_anual: Union[List[str], XComArg, None] = None,
) -> Union[List[str], XComArg]:
    import logging
    logger = logging.getLogger("airflow.task")

    logger.info(f"Merging listas - Diária: {lista_diaria}, Anual: {lista_anual}")

    return lista_diaria or lista_anual or []


@task
def verifica_disponibilidade(arquivos: Union[List[str], XComArg]) -> List[str]:
    import httpx
    import logging
    logger = logging.getLogger("airflow.task")

    base_url = "https://bvmf.bmfbovespa.com.br/InstDados/SerHist/"
    disponiveis = []

    logger.info(f"Verificando disponibilidade de arquivos: {arquivos}")

    for nome in arquivos:
        url = f"{base_url}{nome}"
        try:
            resp = httpx.head(url, timeout=20, verify=False)
            if resp.status_code == 200:
                disponiveis.append(nome)
        except httpx.HTTPError as e:
            logger.error(f"Erro ao acessar {url}: {e}")
            continue

    logger.info(f"Arquivos disponíveis encontrados: {disponiveis}")

    return disponiveis


@task.branch
def decide_se_continua(lista: Union[List[str], XComArg]) -> str:
    import logging
    logger = logging.getLogger("airflow.task")

    decision = "downloads" if lista else "fim"
    logger.info(f"Decisão da branch: {decision}")

    return decision


@task.branch(task_id="tipo_serie")
def tipo_serie_choice() -> str:
    import logging
    logger = logging.getLogger("airflow.task")

    from airflow.models import Variable
    serie = Variable.get("B3_CONFIG_DOWNLOAD_SERIE", default_var="series_anuais").lower()

    escolha = "if_tipo_serie_then.download_diario" if serie == "serie_diaria" else "if_tipo_serie_then.download_anual"

    logger.info(f"Tipo de série selecionado: {serie} -> Próxima task: {escolha}")

    return escolha


@task
def seta_serie_para_diaria() -> None:
    import logging
    logger = logging.getLogger("airflow.task")

    from airflow.models import Variable
    Variable.set("B3_CONFIG_DOWNLOAD_SERIE", "serie_diaria")

    logger.info("Variável 'B3_CONFIG_DOWNLOAD_SERIE' setada para 'serie_diaria'")


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
    tags=["b3", "etl", "v24"],
)
def b3_etl():
    from airflow.operators.empty import EmptyOperator
    from airflow.utils.task_group import TaskGroup

    inicio = EmptyOperator(task_id="inicio")
    fim = EmptyOperator(
        task_id="fim",
        trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS
    )

    tipo_serie = tipo_serie_choice()

    with TaskGroup(group_id="if_tipo_serie_then") as if_tipo_serie_then:
        arquivos_diarios = serie_diaria.override(task_id="download_diario")()
        arquivos_anuais = series_anuais.override(task_id="download_anual")()

    lista_final = merge_list(
        lista_diaria=arquivos_diarios,
        lista_anual=arquivos_anuais,
    )

    arquivos_existentes = verifica_disponibilidade(lista_final)
    escolha = decide_se_continua(arquivos_existentes)

    downloads = EmptyOperator(task_id="downloads")
    baixa_arquivos = download_zip_file.expand(file_to_download=arquivos_existentes)
    extracoes = extract_zip_files.expand(zip_paths=baixa_arquivos)
    seta_serie = seta_serie_para_diaria()

    # Definindo a sequência
    inicio >> tipo_serie >> if_tipo_serie_then >> lista_final >> arquivos_existentes >> escolha
    escolha >> downloads
    downloads >> baixa_arquivos >> extracoes >> seta_serie
    [seta_serie, escolha] >> fim


dag = b3_etl()

if __name__ == "__main__":
    dag.test()
