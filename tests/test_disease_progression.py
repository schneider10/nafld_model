import pandas as pd

from model.disease_progression import DiseaseProgression, BariatricDiseaseProgression, OCADiseaseProgression
from model.inputs import inputs


class OutputProgression:
    def __init__(self):
        self.output_file = None

    def output_disease_progression(self, disease_progression):
        pd.DataFrame().to_csv(self.output_file)

        for ind, cohort in enumerate(inputs.cohorts):
            df = disease_progression(cohort).calculate_progression()

            # Output cohort name.
            pd.DataFrame({'Cohort': [cohort]}).to_csv(self.output_file, mode='a')
            df.to_csv(self.output_file, mode='a')

            yield {f'{cohort}': df}

    def output_control_disease_progression(self):
        self.output_file = 'outputs/disease_progression/control_disease_progression.csv'
        return self.output_disease_progression(DiseaseProgression)

    def output_bariatric_disease_progression(self):
        self.output_file = 'outputs/disease_progression/bariatric_disease_progression.csv'
        return self.output_disease_progression(BariatricDiseaseProgression)

    def output_oca_disease_progression(self):
        self.output_file = 'outputs/disease_progression/oca_disease_progression.csv'
        return self.output_disease_progression(OCADiseaseProgression)


def test_control_disease_progression_generation(test_inputs):
    progression = OutputProgression().output_control_disease_progression()
    for p in progression:
        test_case = {'cohort': '45-49', 'sum': 373897}

        if test_case['cohort'] in p:
            assert int(p[test_case['cohort']].to_numpy().sum()) == test_case['sum']


def test_bariatric_disease_progression_generation(test_inputs):
    progression = OutputProgression().output_bariatric_disease_progression()
    for p in progression:
        test_case = {'cohort': '45-49', 'sum': 373897}

        if test_case['cohort'] in p:
            assert int(p[test_case['cohort']].to_numpy().sum()) == test_case['sum']


def test_oca_disease_progression_generation(test_inputs):
    progression = OutputProgression().output_oca_disease_progression()
    for p in progression:
        test_case = {'cohort': '45-49', 'sum': 373896}

        if test_case['cohort'] in p:
            assert int(p[test_case['cohort']].to_numpy().sum()) == test_case['sum']
