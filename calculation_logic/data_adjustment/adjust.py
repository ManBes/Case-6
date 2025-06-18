import pandas as pd
import numpy as np

#Select rows that contain no NA values, 
#Return the adjusted object, an array of maturities (n), an array of dates (m), and an array of yields (nxm) 
def adjust_df(df):
    # Step 1: Drop rows with any NaN values
    df_new = df.dropna()

    # Step 2: Filter only numeric term columns
    term_cols = [col for col in df_new.columns if col.startswith('monthly_data_term_')]

    # Step 3: Drop values before 2025
    df_new = df_new[df_new['years'].str[:4] <= '2024']

    # Step 4: Extract outputs
    maturities = np.array([int(col.split('_')[-1]) for col in term_cols])  # array([1, 2, ..., 30])
    dates = pd.to_datetime(df_new['years'].values)  # convert to datetime
    yields = df_new[term_cols].values  # shape (n_dates, n_terms)

    return df_new, maturities, dates, yields