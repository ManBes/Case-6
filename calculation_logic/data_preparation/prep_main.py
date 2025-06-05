#IMPORT LIABARIES
import pandas as pd
import re
import numpy as np
import os

#LOADING IN DATA:
def load_term_structures(source, pattern, prefix):
    """
    Laad CSV bestanden volgens het glob pattern,
    voeg prefix toe aan kolomnamen (bijv. 'daily' of 'monthly')
    """
    files = os.listdir(source)
    dataframes = []

    print(f"Loading files with pattern '{pattern}'")
    for file in files:
        match = re.search(r'R(\d{2})XX', file)
        if not match:
            print(f"Term length not found in filename: {file}, skipping")
            continue
        term_length = match.group(1)

        df = pd.read_csv(source + file, skiprows=9, header=None, usecols=[0, 1])
        df.columns = ['years', f'{prefix}_data_term_{term_length}']
        dataframes.append(df)

    if not dataframes:
        print(f"No files loaded for pattern {pattern}")
        return None

    merged_df = dataframes[0]
    for df in dataframes[1:]:
        merged_df = pd.merge(merged_df, df, on='years', how='outer')

    merged_df = merged_df.sort_values(by='years').reset_index(drop=True)

    # Vervang '.' door NaN en converteer naar numeriek
    term_cols = [col for col in merged_df.columns if col.startswith(f'{prefix}_data_term_')]
    for col in term_cols:
        merged_df[col] = merged_df[col].replace('.', np.nan)
        merged_df[col] = pd.to_numeric(merged_df[col], errors='coerce')

    return merged_df

def find_path(add_to_dir):
    current_path = os.getcwd()

    return current_path + add_to_dir
