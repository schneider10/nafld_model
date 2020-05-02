import pandas as pd

from model.disease_progression import DiseaseProgression, BariatricDiseaseProgression, OCADiseaseProgression
from model.inputs import inputs


class OutputProgression:
    def __init__(self):
        self.output_file = None

    def output_disease_progression(self, disease_progression):
        for cohort in inputs.cohorts:
            df = disease_progression(cohort).calculate_progression()

            # Output cohort name.
            pd.DataFrame({'Cohort': cohort}, index=['Cohort']).to_csv(self.output_file, mode='a')
            df.to_csv(self.output_file, mode='a')

            yield {f'{cohort}': df}

    def output_control_disease_progression(self):
        self.output_file = 'outputs/control_disease_progression.csv'
        return self.output_disease_progression(DiseaseProgression)

    def output_bariatric_disease_progression(self):
        self.output_file = 'outputs/bariatric_disease_progression.csv'
        return self.output_disease_progression(BariatricDiseaseProgression)

    def output_oca_disease_progression(self):
        self.output_file = 'outputs/oca_disease_progression.csv'
        return self.output_disease_progression(OCADiseaseProgression)


def test_control_disease_progression_generation(test_inputs):
    progression = OutputProgression().output_control_disease_progression()
    for p in progression:
        test_case = {'cohort': '45-49', 'sum': 373811.2375266784}

        if test_case['cohort'] in p:
            assert p[test_case['cohort']].to_numpy().sum() == test_case['sum']

