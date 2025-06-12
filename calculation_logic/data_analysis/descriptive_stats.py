import pandas as pd
import numpy as np

def create_descriptive_stats(df):
    # Sluit kolommen uit die met 'year' of 'Year' beginnen
    to_drop = [col for col in df.columns if col.lower().startswith('year')]
    data_cols = df.columns.drop(to_drop)

    # Statistieken opvragen
    stats = df[data_cols].describe().T
    stats['missing_pct'] = df[data_cols].isna().mean() * 100

    # Startjaar bepalen
    start_years = {}
    year_col = next((c for c in df.columns if c.lower().startswith('year')), None)
    for col in data_cols:
        first_valid_idx = df[col].first_valid_index()
        if first_valid_idx is not None and year_col is not None:
            start_year = df.loc[first_valid_idx, year_col].year
        else:
            start_year = np.nan
        start_years[col] = start_year

    stats['Start Year'] = pd.Series(start_years)

    # Zet kolomnamen (zoals 'daily_01') in een kolom om maturity te extraheren
    stats['Column Name'] = stats.index

    # Extract maturity-nummer uit kolomnaam
    stats['Maturity'] = stats['Column Name'].str.extract(r'(\d+)$')[0].astype(int)

    stats = stats.rename(columns={
        'count': 'Count',
        'mean': 'Mean',
        '50%': 'Median',
        'std': 'Std',
        'min': 'Min',
        'max': 'Max',
        'missing_pct': 'Missing %'
    })

    stats = stats[['Maturity', 'Count', 'Mean', 'Median', 'Std', 'Min', 'Max', 'Missing %', 'Start Year']]
    stats = stats.sort_values('Maturity').reset_index(drop=True)
    stats.index = stats.index + 1
    stats = stats.round(2)

    return stats