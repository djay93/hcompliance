import pandas as pd
import logging
from time import time

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def vlookup_from_json(config):
    start_time = time()
    logger.info("Starting vlookup_from_json function")

    # Load the input file
    logger.info(f"Loading input file: {config['input_file']}")
    input_df = pd.read_excel(config['input_file'])
    logger.info(f"Input file loaded. Shape: {input_df.shape}")

    # Pre-load all lookup files
    lookup_dfs = {}
    for lookup_key, lookup_config in config.items():
        if lookup_key.startswith('lookup_'):
            logger.info(f"Loading lookup file: {lookup_config['lookup_file']}")
            lookup_dfs[lookup_key] = pd.read_excel(lookup_config['lookup_file'])
            logger.info(f"Lookup file {lookup_key} loaded. Shape: {lookup_dfs[lookup_key].shape}")

    # Optimize lookup function
    def perform_lookup(input_values, lookup_config, lookup_df):
        result_column = lookup_config['result_value'].split("column:")[1] if lookup_config['result_value'].startswith("column:") else None
        
        if result_column:
            # Create a dictionary for faster lookups
            lookup_dict = dict(zip(lookup_df[lookup_config['lookup_column']], lookup_df[result_column]))
            
            # Vectorized lookup
            results = input_values.map(lookup_dict)
            
            # Fill NaN values with na_value
            results = results.fillna(lookup_config['na_value'])
        else:
            # If result_value is static, return it for all rows
            results = pd.Series([lookup_config['result_value']] * len(input_values))
        
        return results

    # Apply lookups
    for lookup_key, lookup_config in config.items():
        if lookup_key.startswith('lookup_'):
            logger.info(f"Performing lookup: {lookup_key}")
            start_lookup = time()
            
            # Apply the lookup for all rows at once
            input_df[lookup_key] = perform_lookup(
                input_df[config['input_lookup_column']],
                lookup_config,
                lookup_dfs[lookup_key]
            )
            
            logger.info(f"Lookup {lookup_key} completed in {time() - start_lookup:.2f} seconds")

    # Save the updated dataframe back to the file
    output_file = "updated_" + config['input_file']
    logger.info(f"Saving updated file to: {output_file}")
    input_df.to_excel(output_file, index=False)
    logger.info(f"Updated file saved. Shape: {input_df.shape}")

    total_time = time() - start_time
    logger.info(f"vlookup_from_json completed in {total_time:.2f} seconds")

# Example config from the JSON-like structure
config = {
    "input_file": "input_data.xlsx",
    "input_lookup_column": "C",
    "lookup_1": {
        "lookup_file": "lookup1.xlsx",
        "lookup_column": "A",
        "result_value": "column:B",  # Refers to a column in the lookup file
        "na_value": "empty"
    },
}

if __name__ == "__main__":
    # Call the function with the provided config
    vlookup_from_json(config)
