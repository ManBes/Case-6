import os
import shutil

from data_analysis import descriptive_stats, create_plots, test_stationarity

def perform_data_analysis(df_day, df_month, path_to_store_results):
    clear_folder_contents(path_to_store_results)

    #Create graphs
    create_plots.create_term_structure_plot(df_month, path_to_store_results, 'Monthly', 'monthly_data_term_')
    create_plots.create_term_structure_plot(df_day, path_to_store_results, 'Daily', 'daily_data_term_')

    #Create summary statistics
    daily_stats = descriptive_stats.create_descriptive_stats(df_day)
    monthly_stats = descriptive_stats.create_descriptive_stats(df_month)

    print(daily_stats)
    print(monthly_stats)
    
    store_to_excel(daily_stats, path_to_store_results, 'daily')
    store_to_excel(monthly_stats, path_to_store_results, 'monthly')

    #Create correlation plots
    daily_corr = create_plots.create_correlation_heatmap_annotated(df_day, path_to_store_results, 'Correlation Heatmap for different maturities - Daily Data', 'daily')
    monthly_corr = create_plots.create_correlation_heatmap_annotated(df_month, path_to_store_results, 'Correlation Heatmap for different maturities - Monthly Data', 'monthly')

    print(daily_corr.round(3))
    print(monthly_corr.round(3))

    #Test for stationarity
    daily_adf_results = test_stationarity.adf_test_all_to_table(df_day, 'daily', path_to_store_results)
    monthly_adf_results = test_stationarity.adf_test_all_to_table(df_month, 'monthly', path_to_store_results)

    print(daily_adf_results)
    print(monthly_adf_results)

    #Analyse missing data
    create_plots.analyse_missing_data(df_day, df_month, path_to_store_results)

def clear_folder_contents(path_to_store_results):
    shutil.rmtree(path_to_store_results, ignore_errors=True)
    os.makedirs(path_to_store_results)  

def store_to_excel(df, path_to_store_results, tag):
    df.to_excel(f'{path_to_store_results}/{tag}_summary_stats.xlsx')
