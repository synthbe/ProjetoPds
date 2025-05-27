import logging
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Literal

from app.config.settings import settings

class AudioInference:
    @staticmethod
    def vocal_inference(
        audio_path: str,
        extraction_type: Literal["vocals", "instrumental", "4stems"]
    ) -> List[Dict[str, str]]:
        logging.debug(f"audio_path = {audio_path}")
        logging.debug(f"extraction_type = {extraction_type}")

        # Mapear extraction_type para o arquivo de config correto
        # Colocar mapeamento em um lugar mais adequado
        config_map = {
            "vocals": { "yaml": "artifacts/melbandroformers/vocals/voc_gabox.yaml", "ckpt": "artifacts/melbandroformers/vocals/voc_fv5.ckpt" },
            "4stems": {}, # Define
            "instrumental": { "yaml": "artifacts/melbandroformers/instrumental/inst_gabox.yaml", "ckpt": "artifacts/melbandroformers/instrumental/Inst_GaboxFv8.ckpt"}
        }

        # ALERT! SERVER RETURNS 200 IF FILES ABOVE NOT FOUND

        config_filename = config_map[extraction_type].get("yaml")
        if config_filename is None:
            raise ValueError(f"Unsupported extraction type: {extraction_type}")

        args = [
            sys.executable,
            f"{settings.AUDIO_EXTRACTOR_REPO_DIR}/inference.py",
            "--config_path",
            f"{config_map[extraction_type]['yaml']}",
            "--start_check_point",
            f"{config_map[extraction_type]['ckpt']}",
            "--input_folder",
            audio_path,
            "--store_dir",
            audio_path,
            "--model_type",
            "mel_band_roformer",
        ]

        subprocess.run(args)

        output_files = []

        input_folder = Path(audio_path)
        for file in input_folder.iterdir():
            if not file.is_file():
                continue
            output_folder_name = file.stem  # nome sem extensão
            output_folder_path = input_folder / output_folder_name
            if not output_folder_path.exists() or not output_folder_path.is_dir():
                continue
            for generated_file in output_folder_path.iterdir():
                output_files.append(
                    {
                        "name": generated_file.name,
                        "path": str(generated_file.resolve()),
                    }
                )
        return output_files
