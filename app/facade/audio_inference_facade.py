import subprocess
import os
from pathlib import Path

from app.config.settings import settings

class AudioInference:
    @staticmethod
    def vocal_inference(audio_path: str):
        audio_path = audio_path
        print(f"[DEBUG] audio_path = {audio_path}")
        output_path = os.path.join(audio_path, "separated")


        args = [
            "python3", f"{settings.AUDIO_EXTRACTOR_REPO_DIR}/inference.py",
            "--config_path", f"{settings.AUDIO_EXTRACTOR_REPO_DIR}/configs/config_vocals_mdx23c.yaml",
            "--input_folder", audio_path,
            "--store_dir", audio_path,
            "--model_type", "mdx23c"
        ]

        subprocess.run(args)

        # Get base name (without extension)
        ##input_folder = Path(audio_path)
        #for file in input_folder.iterdir():
        #    if file.is_file():
        #        output_folder_name = file.stem  # name without extension
         #       output_folder_path = input_folder / output_folder_name
         #       if output_folder_path.exists() and output_folder_path.is_dir():
         #           print(f"Contents of {output_folder_path}:")
          #          for generated_file in output_folder_path.iterdir():
          #              print(generated_file)  # or do something with each file


        
        
        
