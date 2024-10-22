import json
from typing import Dict
from pydantic import BaseModel, Field
from hmda.utils.logger import get_logger

logger = get_logger(__name__)

class Config(BaseModel):
    source_dir: str = Field(..., description="Directory containing source files")
    destination_dir: str = Field(..., description="Directory where files will be replaced")
    replacement_dir: str = Field(..., description="Directory containing replacement files")

class ConfigLoader:
    @staticmethod
    def load(file_path: str) -> Dict[str, str]:
        logger.info(f"Loading configuration from: {file_path}")
        with open(file_path, "r") as f:
            config_data = json.load(f)
        
        config = Config(**config_data)
        logger.info("Configuration loaded successfully")
        return config.dict()
