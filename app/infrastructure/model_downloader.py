from typing import Literal
from huggingface_hub import hf_hub_download

class ModelDownloader:
    def __init__(self) -> None:
        self.repo_id = "GaboxR67/MelBandRoformers" # Not sure if keep harcoded
        self.extraction_mapping = {
            "vocals": { "ckpt": "voc_fv5.ckpt", "yaml": "voc_gabox.yaml" },
            "instrumental": { "ckpt": "Inst_GaboxFv8.ckpt", "yaml": "inst_gabox.yaml" },
        }

    def download_model(
        self,
        extraction_type: Literal["vocals", "instrumental", "4stems"],
    ) -> None:
        remote_ckpt = f"melbandroformers/{extraction_type}/{self.extraction_mapping[extraction_type]['ckpt']}"
        remote_yaml = f"melbandroformers/{extraction_type}/{self.extraction_mapping[extraction_type]['yaml']}"

        hf_hub_download(
            repo_id=self.repo_id,
            filename=remote_ckpt,
            local_dir=f"artifacts/",
            cache_dir="extractions",
            force_download=False,
        )

        hf_hub_download(
            repo_id=self.repo_id,
            filename=remote_yaml,
            local_dir=f"artifacts/",
            cache_dir="extractions",
            force_download=False,
        )
