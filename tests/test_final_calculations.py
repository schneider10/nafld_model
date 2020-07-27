from model.disease_progression import BariatricDiseaseProgression, OCADiseaseProgression
from model.final_calculations import OutputFinalCalculations


def test_final_bariatric_calculations():
    test_case = {'cohort': '45-49', 'sum': 1414875330.1766636}
    calculations = OutputFinalCalculations(BariatricDiseaseProgression,
                                           'outputs/bariatric_final_calculations.csv').final_calculations

    assert calculations.loc[test_case['cohort']].to_numpy().sum() == test_case['sum']


def test_final_oca_calculations():
    test_case = {'cohort': '45-49', 'sum': 1473521495.6555011}
    calculations = OutputFinalCalculations(OCADiseaseProgression,
                                           'outputs/oca_final_calculations.csv').final_calculations

    assert calculations.loc[test_case['cohort']].to_numpy().sum() == test_case['sum']
