import json
from typing import List, Dict
from hmda.utils.logger import get_logger

logger = get_logger(__name__)

class FileReplacer:
    @staticmethod
    def replace_files(excel_data: List[Dict[str, str]], vcode_data: Dict[str, Dict[str, str]]):
        logger.info("Starting file replacement process")
        for row in excel_data:
            # source = os.path.join(config["source_dir"], row["source"])
            # destination = os.path.join(config["destination_dir"], row["destination"])
            # replacement = os.path.join(config["replacement_dir"], row["replacement"])

            # Apply vcode-mapping to column A and column B
            for column in ["A", "B"]:
                if column in vcode_data and row[f"column{column}"] in vcode_data[column]:
                    row[f"column{column}"] = vcode_data[column][row[f"column{column}"]]

            # if not os.path.exists(source):
            #     logger.warning(f"Source file not found: {source}")
            #     continue

            # if not os.path.exists(replacement):
            #     logger.warning(f"Replacement file not found: {replacement}")
            #     continue

            # os.makedirs(os.path.dirname(destination), exist_ok=True)
            # shutil.copy2(replacement, destination)
            # logger.info(f"Replaced {source} with {replacement} at {destination}")

        logger.info("File replacement process completed")

    @staticmethod
    def load_vcode(mapping_file: str) -> Dict[str, Dict[str, str]]:
        with open(mapping_file, 'r') as f:
            return json.load(f)
