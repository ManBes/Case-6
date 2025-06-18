from data_preparation import prep_main as pr
from data_analysis import analysis_main as am
from data_adjustment import adjust 
from model_fit import model_fit_main as mf
from model_fit import assess_fit as af

if __name__ == '__main__':
    # #vanuit hier functies aanroepen in volgorde:
    # data_prep: Laden van daily en monthly data
    daily_df = pr.load_term_structures(pr.find_path('/data/daily/'), 'daily-term-structure-spot-interest-rate-R*XX.csv', 'daily')
    monthly_df = pr.load_term_structures(pr.find_path('/data/monthly/'), 'monthly-term-structure-spot-interest-rate-R*XX.csv', 'monthly')

    # data_analysis: uitvoeren data analyse. Opslaan van output in data/output_analysis. Het is mogelijk om script te draaien zonder analyse opnieuw uit te voeren
    # am.perform_data_analysis(daily_df, monthly_df, pr.find_path('/data/output_analysis'))

    # # data_adjustment: filter out NAs, make data objects ready for model calibration
    monthly_df_adj, maturities, dates, yields = adjust.adjust_df(monthly_df)

    # - parameter_fitting
    output_grid, output_flex  = mf.activate_model_calibration(maturities, dates, yields)

    # assess flex
    af.assess_flexible_tau(output_flex, pr.find_path('/data/output_analysis'))

    # assess grid and choose tau based on lowest total sum of squared residual
    af.assess_fixed_tau(output_grid, pr.find_path('/data/output_analysis'))


