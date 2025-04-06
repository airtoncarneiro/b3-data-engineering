from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from datetime import timedelta
import httpx
import zipfile
import logging
from pathlib import Path
from typing import Dict, Any

# Configuração do logging
logging.getLogger("airflow.task").setLevel(logging.INFO)
logging.getLogger("httpx").setLevel(logging.INFO)
logging.getLogger("zipfile").setLevel(logging.INFO)

# Configurações globais
DEFAULT_URL = "https://example.com/arquivo.zip"
DEFAULT_SAVE_PATH = "/tmp"
DEFAULT_EXTRACT_DIR = "/tmp/extracted_files"
DEFAULT_TIMEOUT = 60.0

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

@dag(
    dag_id="final_download_and_extract_zip",
    default_args=default_args,
    schedule=None,
    start_date=days_ago(1),
    catchup=False,
    tags=["download", "zip", "httpx", "final"],
    description="Pipeline final combinando as melhores práticas das versões analisadas"
)
def final_download_and_extract_zip():

    @task(retries=3)
    def download_zip_file(url: str = DEFAULT_URL, timeout: float = DEFAULT_TIMEOUT) -> Dict[str, Any]:
        """
        Faz o download do arquivo com httpx (streaming) e retorna metadados e conteúdo.
        """
        logging.info(f"Iniciando download de: {url}")
        try:
            with httpx.stream("GET", url, timeout=timeout) as response:
                response.raise_for_status()
                content = b''.join(response.iter_bytes())

                return {
                    "content": content,
                    "filename": url.split("/")[-1],
                    "content_type": response.headers.get("content-type", ""),
                    "content_length": len(content),
                    "status_code": response.status_code,
                }

        except httpx.HTTPError as e:
            logging.error(f"Erro HTTP: {e}")
            raise
        except Exception as e:
            logging.error(f"Erro inesperado no download: {e}")
            raise

    @task
    def save_file_to_disk(file_info: Dict[str, Any], save_dir: str = DEFAULT_SAVE_PATH) -> str:
        """
        Salva o conteúdo do arquivo em disco e retorna o caminho salvo.
        """
        Path(save_dir).mkdir(parents=True, exist_ok=True)
        file_path = Path(save_dir) / file_info["filename"]

        try:
            with open(file_path, "wb") as f:
                f.write(file_info["content"])
            logging.info(f"Arquivo salvo em: {file_path} ({file_info['content_length']} bytes)")
            return str(file_path)
        except Exception as e:
            logging.error(f"Erro ao salvar arquivo: {e}")
            raise

    @task
    def extract_zip_file(zip_path: str, extract_dir: str = DEFAULT_EXTRACT_DIR) -> Dict[str, Any]:
        """
        Descompacta o arquivo ZIP e retorna informações da extração.
        """
        Path(extract_dir).mkdir(parents=True, exist_ok=True)

        try:
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                # Verifica se o ZIP está corrompido
                if zip_ref.testzip() is not None:
                    raise zipfile.BadZipFile("Arquivo ZIP corrompido.")

                zip_ref.extractall(extract_dir)
                extracted_files = zip_ref.namelist()

            logging.info(f"{len(extracted_files)} arquivos extraídos para: {extract_dir}")
            return {
                "extract_path": extract_dir,
                "extracted_files": extracted_files,
                "total_files": len(extracted_files)
            }

        except zipfile.BadZipFile as e:
            logging.error(f"Arquivo inválido: {e}")
            raise
        except Exception as e:
            logging.error(f"Erro na extração: {e}")
            raise

    # Pipeline
    file_info = download_zip_file()
    file_path = save_file_to_disk(file_info)
    extract_info = extract_zip_file(file_path)

# Instancia a DAG
final_dag_instance = final_download_and_extract_zip()
# Configuração do logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
