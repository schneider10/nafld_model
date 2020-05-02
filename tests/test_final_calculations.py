from model.disease_progression import BariatricDiseaseProgression, OCADiseaseProgression
from model.final_calculations import FinalCalculations
from model.inputs import inputs
import pandas as pd


def test_final_bariatric_calculations(test_inputs):
    output_file = 'outputs/bariatric_final_calculations.csv'

    for ind, cohort in enumerate(inputs.cohorts):
        calculations = FinalCalculations(BariatricDiseaseProgression, cohort).get_all_final_calculations()

        # Output cohort name.
        if ind == 0:
            pd.DataFrame({'Cohort': [cohort]}).to_csv(output_file)
        else:
            pd.DataFrame({'Cohort': [cohort]}).to_csv(output_file, mode='a')

        calculations.to_csv(output_file, mode='a')

        test_case = {'cohort': '45-49', 'sum': 1333716971.2915266}

        if cohort == test_case['cohort']:
            assert calculations.to_numpy().sum() == test_case['sum']


def test_final_oca_calculations(test_inputs):
    output_file = 'outputs/oca_final_calculations.csv'

    for ind, cohort in enumerate(inputs.cohorts):
        calculations = FinalCalculations(OCADiseaseProgression, cohort).get_all_final_calculations()

        # Output cohort name.
        if ind == 0:
            pd.DataFrame({'Cohort': [cohort]}).to_csv(output_file)
        else:
            pd.DataFrame({'Cohort': [cohort]}).to_csv(output_file, mode='a')

        calculations.to_csv(output_file, mode='a')

        test_case = {'cohort': '45-49', 'sum': 1391221028.5460157}

        if cohort == test_case['cohort']:
            assert calculations.to_numpy().sum() == test_case['sum']
