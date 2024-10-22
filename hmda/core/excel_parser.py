from typing import List, Dict
import pandas as pd
from hmda.utils.logger import get_logger

logger = get_logger(__name__)

class ExcelParser:
    @staticmethod
    def parse(file_path: str) -> List[Dict[str, str]]:
        logger.info(f"Parsing Excel file: {file_path}")
        
        # Read the Excel file
        df = pd.read_excel(file_path, engine='openpyxl')
        
        # Remove any completely empty rows
        df = df.dropna(how='all')
        
        # Ensure the required columns are present
        required_columns = ['A', 'B']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Excel file must contain columns: {', '.join(required_columns)}")
        
        # Convert DataFrame to list of dictionaries
        data = df[required_columns].to_dict('records')
        
        logger.info(f"Parsed {len(data)} rows from Excel file")
        return data

    @staticmethod
    def save_to_excel(data: List[Dict[str, str]], output_file: str):
        df = pd.DataFrame(data)
        df.to_excel(output_file, index=False)
        logger.info(f"Updated data saved to {output_file}")