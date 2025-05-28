from typing import Literal
from huggingface_hub import hf_hub_download
from app.facade.audio_inference_facade import MODEL_CONFIG_MAP

class ModelDownloader:
    def __init__(self) -> None:
        self.repo_id = "GaboxR67/MelBandRoformers"  # Keep hardcoded or parametrize if needed

        # Filter out keys that exist in MODEL_CONFIG_MAP and come from huggingface
        self.extraction_mapping = {
            key: {
                "ckpt": value["ckpt"].split("/")[-1],  # just filename for HF path
                "yaml": value["yaml"].split("/")[-1],
            }
            for key, value in MODEL_CONFIG_MAP.items()
            if value["model_type"] == "mel_band_roformer"
        }

    def download_model(
        self,
        extraction_type: Literal["vocals", "instrumental", "4stems"],
    ) -> None:
        if extraction_type not in self.extraction_mapping:
            # Skip if model not recognized or not hosted on huggingface
            return

        remote_ckpt = f"melbandroformers/{extraction_type}/{self.extraction_mapping[extraction_type]['ckpt']}"
        remote_yaml = f"melbandroformers/{extraction_type}/{self.extraction_mapping[extraction_type]['yaml']}"

        hf_hub_download(
            repo_id=self.repo_id,
            filename=remote_ckpt,
            local_dir="artifacts/",
            cache_dir="extractions",
            force_download=False,
        )

        hf_hub_download(
            repo_id=self.repo_id,
            filename=remote_yaml,
            local_dir="artifacts/",
            cache_dir="extractions",
            force_download=False,
        )
