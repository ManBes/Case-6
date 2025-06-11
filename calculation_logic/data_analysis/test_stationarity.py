import pandas as pd
import re
from statsmodels.tsa.stattools import adfuller

def adf_test_all_to_table(df, freq_label, path_to_store_results):
    results = []
    terms = [col for col in df.columns if col.startswith(f'{freq_label}_data_term_')]
    
    for term in sorted(terms):
        series = df[term].dropna()
        result = adfuller(series)
        p_value = result[1]
        is_stationary = 'Yes' if p_value < 0.05 else 'No'

        maturity_num = int(re.search(r'_(\d+)$', term).group(1))

        results.append({
            'Maturity': maturity_num,
            'ADF Statistic': round(result[0], 4),
            'p-value': round(p_value, 4),
            'Stationary': is_stationary
        })
    
    df_results = pd.DataFrame(results)
    df_results = df_results.sort_values('Maturity').reset_index(drop=True)

    df_results.to_excel(f'{path_to_store_results}/{freq_label}_adf_results.xlsx', index=False)
