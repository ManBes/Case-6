import pandas as pd
import glob
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from statsmodels.tsa.stattools import adfuller
import shutil
import os
from sklearn.decomposition import PCA
from IPython.display import display

def create_term_structure_plot(df, path_to_store_results, tag, file_identifier):
    df['years'] = pd.to_datetime(df['years'], errors='coerce')

    plt.figure(figsize=(12, 8))

    monthly_cols = sorted([col for col in df.columns if col.startswith(file_identifier)])

    for col in monthly_cols:
        label = col.replace(f'{tag}_data_term_', '')  # Alleen het jaarnummer
        plt.plot(df['years'], df[col], label=label, alpha=0.7)

    plt.title(f'{tag} interest rates for different maturities')
    plt.xlabel('Date')
    plt.ylabel('Interest Rate')

    # Stel de x-as formatter en locator in voor datums
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.YearLocator(base=5))  # elke 5 jaar een tick
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    plt.legend(loc='upper right', fontsize='small', ncol=2)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'{path_to_store_results}/term_structure_of_{file_identifier}.png')
    plt.close()

def create_correlation_heatmap_annotated(df, path_to_store_results, title, tag):
    term_cols = sorted([col for col in df.columns if 'data_term_' in col])
    corr = df[term_cols].corr()

    plt.figure(figsize=(18,16))
    ax = sns.heatmap(
        corr,
        cmap='vlag',
        center=0.9,
        vmin=0.8,
        vmax=1.0,
        square=True,
        annot=True,
        fmt=".2f",
        annot_kws={"size":7},
        linewidths=0.3,
        cbar_kws={"shrink": 0.6}
    )
    plt.title(title, fontsize=20)

    # Vervang de xticks en yticks labels door alleen het nummer (bijv. '1' in plaats van 'daily_data_term_01')
    new_labels = [col.split('_')[-1] for col in term_cols]  # pakt '01', '02', etc.
    new_labels = [str(int(label)) for label in new_labels]  # converteert '01' -> '1' als string

    ax.set_xticklabels(new_labels, rotation=90, fontsize=8)
    ax.set_yticklabels(new_labels, fontsize=8)
    
    plt.tight_layout()
    plt.savefig(f'{path_to_store_results}/correlation_heatmap_of_{tag}.png')
    plt.close()

    return corr

# Plot en sla de correlatiematrices op
daily_corr = create_correlation_heatmap_annotated(daily_df, path_to_store_results, 'Correlation Heatmap for different maturities - Daily Data', 'daily')
monthly_corr = create_correlation_heatmap_annotated(monthly_df, path_to_store_results, 'Correlation Heatmap for different maturities - Monthly Data', 'monthly')

# Toon de correlatiematrices als tabel
print("Correlation matrix - Daily Data:")
print(daily_corr.round(3))

print("\nCorrelation matrix - Monthly Data:")
print(monthly_corr.round(3))