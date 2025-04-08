class FileHandler:
    @staticmethod
    def _save_file_to_disk(file_info: dict, save_dir: str) -> str:
        from pathlib import Path
        import logging

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