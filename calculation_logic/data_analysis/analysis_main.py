#IMPORT LIABARIES
import pandas as pd
import glob
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from statsmodels.tsa.stattools import adfuller
import os
from sklearn.decomposition import PCA


# Daily data laden
daily_df = load_term_structures(find_path('/data/daily/'), 'daily-term-structure-spot-interest-rate-R*XX.csv', 'daily')

# Monthly data laden
monthly_df = load_term_structures(find_path('/data/monthly/'), 'monthly-term-structure-spot-interest-rate-R*XX.csv', 'monthly')

print("Daily data sample:")
print(daily_df.head() if daily_df is not None else "No daily data loaded")

print("\nMonthly data sample:")
print(monthly_df.head() if monthly_df is not None else "No monthly data loaded")