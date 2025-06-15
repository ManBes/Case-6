from data_preparation import prep_main as pr
from data_analysis import analysis_main as am
from data_adjustment import adjust 
from model_fit import model_fit_main as mf

# #vanuit hier functies aanroepen in volgorde:
# data_prep: Laden van daily en monthly data
daily_df = pr.load_term_structures(pr.find_path('/data/daily/'), 'daily-term-structure-spot-interest-rate-R*XX.csv', 'daily')
monthly_df = pr.load_term_structures(pr.find_path('/data/monthly/'), 'monthly-term-structure-spot-interest-rate-R*XX.csv', 'monthly')

# data_analysis: uitvoeren data analyse. Opslaan van output in data/output_analysis. Het is mogelijk om script te draaien zonder analyse opnieuw uit te voeren
# am.perform_data_analysis(daily_df, monthly_df, pr.find_path('/data/output_analysis'))

# data_adjustment: filter out NAs, make data objects ready for model calibration
daily_df_adj, maturities, dates, yields = adjust.adjust_df(daily_df)

# - parameter_fitting
mf.activate_model_calibration(daily_df, maturities, dates, yields)
# - scenario_generation (dit vermoedelijk verder opknippen)
# - scenario_analysis