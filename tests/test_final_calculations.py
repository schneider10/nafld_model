from model.disease_progression import BariatricDiseaseProgression, OCADiseaseProgression
from model.final_calculations import FinalCalculations
from model.inputs import inputs
import pandas as pd


class OutputFinalCalculations:
    def __init__(self, disease_progression, outfile):
        self.disease_progression = disease_progression
        self.outputs = []
        self.final_calculations = self.output_final_calculations()
        self.final_calculations.to_csv(outfile)

    def output_final_calculations(self):
        for cohort in inputs.cohorts:
            calculations = FinalCalculations(self.disease_progression, cohort).get_all_final_calculations()
            self.outputs.append(calculations)

        return pd.DataFrame(self.outputs).set_index('Cohort')


def test_final_bariatric_calculations(test_inputs):
    test_case = {'cohort': '45-49', 'sum': 1333716971.2915266}
    calculations = OutputFinalCalculations(BariatricDiseaseProgression,
                                           'outputs/bariatric_final_calculations.csv').final_calculations

    assert calculations.loc[test_case['cohort']].to_numpy().sum() == test_case['sum']


def test_final_oca_calculations(test_inputs):
    test_case = {'cohort': '45-49', 'sum': 1391221028.5460157}
    calculations = OutputFinalCalculations(OCADiseaseProgression,
                                           'outputs/oca_final_calculations.csv').final_calculations

    assert calculations.loc[test_case['cohort']].to_numpy().sum() == test_case['sum']
