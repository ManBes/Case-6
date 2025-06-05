from data_preparation import prep_main as pr

# #vanuit hier functies aanroepen in volgorde:
# - data_prep

# Daily data laden
daily_df = pr.load_term_structures(pr.find_path('/data/daily/'), 'daily-term-structure-spot-interest-rate-R*XX.csv', 'daily')

# Monthly data laden
monthly_df = pr.load_term_structures(pr.find_path('/data/monthly/'), 'monthly-term-structure-spot-interest-rate-R*XX.csv', 'monthly')


# - data_analysis
# - parameter_fitting
# - scenario_generation (dit vermoedelijk verder opknippen)
# - scenario_analysis