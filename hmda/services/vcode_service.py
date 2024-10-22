import json
import pandas as pd
from typing import List, Dict
from hmda.utils.logger import get_logger

logger = get_logger(__name__)

class VCodeService:
    @staticmethod
    def replace_vcode(excel_file: str, vcode_data: Dict[str, str]):
        logger.info(f"Starting file replacement process for {excel_file}")
        logger.info(f"Vcode data: {vcode_data}")

         # Read the Excel file
        df = pd.read_excel(excel_file)

        replaced_count = 0
        # Apply vcode-mapping to all columns
        for column in df.columns:
            df[column] = df[column].map(lambda x: vcode_data.get(str(x), x))
            replaced_count += df[column].map(lambda x: x in vcode_data.values()).sum()

        # Save the changes back to the same file
        df.to_excel(excel_file, index=False)

        logger.info(f"Vcode replacement process completed. Replaced {replaced_count} values.")
        logger.info(f"Updated data saved to {excel_file}")

    @staticmethod
    def load_vcode(mapping_file: str) -> Dict[str, str]:
        with open(mapping_file, 'r') as f:
            return json.load(f)
