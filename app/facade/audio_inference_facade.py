import subprocess
import os
import sys
from pathlib import Path

from app.config.settings import settings


class AudioInference:
    @staticmethod
    def vocal_inference(audio_path: str, extraction_type: str):
        print(f"[DEBUG] audio_path = {audio_path}")
        print(f"[DEBUG] extraction_type = {extraction_type}")

        # Mapear extraction_type para o arquivo de config correto
        config_map = {
            "vocal": "config_vocals_mdx23c.yaml",
            "4stems": "config_musdb18_mdx23c.yaml",
        }

        config_filename = config_map.get(extraction_type)
        if config_filename is None:
            raise ValueError(f"Unsupported extraction type: {extraction_type}")

        config_path = os.path.join(
            settings.AUDIO_EXTRACTOR_REPO_DIR, "configs", config_filename
        )

        args = [
            sys.executable,
            f"{settings.AUDIO_EXTRACTOR_REPO_DIR}/inference.py",
            "--config_path",
            f"{settings.AUDIO_EXTRACTOR_REPO_DIR}/configs/{config_filename}",
            "--input_folder",
            audio_path,
            "--store_dir",
            audio_path,
            "--model_type",
            "mdx23c",
        ]

        subprocess.run(args)

        output_files = []

        input_folder = Path(audio_path)
        for file in input_folder.iterdir():
            if file.is_file():
                output_folder_name = file.stem  # nome sem extensão
                output_folder_path = input_folder / output_folder_name
                if output_folder_path.exists() and output_folder_path.is_dir():
                    for generated_file in output_folder_path.iterdir():
                        output_files.append(
                            {
                                "name": generated_file.name,
                                "path": str(generated_file.resolve()),
                            }
                        )
        return output_files
