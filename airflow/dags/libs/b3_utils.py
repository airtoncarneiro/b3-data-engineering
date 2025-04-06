import httpx
import zipfile
import logging
from pathlib import Path
from typing import Dict, Any

# Configuração do logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Configurações globais
DEFAULT_URL = "https://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_D01042025.ZIP"
DEFAULT_SAVE_PATH = "/tmp"
DEFAULT_EXTRACT_DIR = "/tmp/extracted_files"
DEFAULT_TIMEOUT = 60.0

def download_zip_file(url: str = DEFAULT_URL, timeout: float = DEFAULT_TIMEOUT) -> Dict[str, Any]:
    logging.info(f"Iniciando download de: {url}")
    try:
        logging.warning("⚠️ Verificação SSL desativada para a URL: %s", url)

        with httpx.stream("GET", url, timeout=timeout, verify=False) as response:
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

def save_file_to_disk(file_info: Dict[str, Any], save_dir: str = DEFAULT_SAVE_PATH) -> str:
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

def extract_zip_file(zip_path: str, extract_dir: str = DEFAULT_EXTRACT_DIR) -> Dict[str, Any]:
    Path(extract_dir).mkdir(parents=True, exist_ok=True)
    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
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

if __name__ == "__main__":
    # Exemplo de uso direto do módulo
    file_info = download_zip_file()
    file_path = save_file_to_disk(file_info)
    extract_info = extract_zip_file(file_path)
    print(f"✅ Extração concluída: {extract_info['total_files']} arquivos extraídos.")
    print(f"📦 Arquivo ZIP: {file_info['filename']}")
    print(f"📂 Arquivos extraídos:")
    for arq in extract_info['extracted_files']:
        print(f" - {arq}")
    print(f"📁 Diretório de extração: {extract_info['extract_path']}")