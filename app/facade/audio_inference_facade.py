import logging
import subprocess
import sys
from pathlib import Path
from typing import Dict, List

from app.config.settings import settings

MODEL_CONFIG_MAP = {
    "vocals": {
        "yaml": "artifacts/melbandroformers/vocals/voc_gabox.yaml",
        "ckpt": "artifacts/melbandroformers/vocals/voc_fv5.ckpt",
    },
    "4stems": {
        "yaml": "artifacts/melbandroformers/4stems/4stems.yaml",
        "ckpt": "artifacts/melbandroformers/4stems/4stems.ckpt",
    },
    "noise_reduction": {
        "yaml": "artifacts/melbandroformers/test2/voc_gabox.yaml",
        "ckpt": "artifacts/melbandroformers/test2/voc_fv5.ckpt",
    },
    "instrumental": {
        "yaml": "artifacts/melbandroformers/instrumental/inst_gabox.yaml",
        "ckpt": "artifacts/melbandroformers/instrumental/Inst_GaboxFv8.ckpt"
    }
    # Add more models as needed
}

class AudioInference:
    @staticmethod
    def pipeline_inference(audio_path: str, model_key: str) -> List[Dict[str, str]]:
        logging.debug(f"audio_path = {audio_path}")
        logging.debug(f"model_key = {model_key}")

        config = MODEL_CONFIG_MAP.get(model_key)
        if not config:
            raise ValueError(f"Unsupported model in pipeline: {model_key}")

        args = [
            sys.executable,
            f"{settings.AUDIO_EXTRACTOR_REPO_DIR}/inference.py",
            "--config_path",
            config["yaml"],
            "--start_check_point",
            config["ckpt"],
            "--input_folder",
            audio_path,
            "--store_dir",
            audio_path,
            "--model_type",
            "mel_band_roformer",
        ]

        subprocess.run(args, check=True)

        output_files = []

        input_folder = Path(audio_path)
        for file in input_folder.iterdir():
            if not file.is_file():
                continue
            output_folder_name = file.stem
            output_folder_path = input_folder / output_folder_name
            if not output_folder_path.exists() or not output_folder_path.is_dir():
                continue
            for generated_file in output_folder_path.iterdir():
                output_files.append({
                    "name": generated_file.name,
                    "path": str(generated_file.resolve()),
                })
        return output_files
