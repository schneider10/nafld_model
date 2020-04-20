from disease_progression import DiseaseProgression, BariatricDiseaseProgression, OCADiseaseProgression
from inputs import inputs


class OutputToCsv:
    def __init__(self):
        self.output_file = None

    def output_disease_progression(self, disease_progression):
        for age_cohort in inputs.cohorts:
            df = disease_progression(age_cohort).calculate_progression()

            # Output cohort name.
            pd.DataFrame({'Cohort': age_cohort}, index=['Cohort']).to_csv(self.output_file, mode='a')
            df.to_csv(self.output_file, mode='a')

    def output_regular_disease_progression(self):
        self.output_file = 'regular_disease_progression.csv'
        self.output_disease_progression(DiseaseProgression)

    def output_bariatric_disease_progression(self):
        self.output_file = 'bariatric_disease_progression.csv'
        self.output_disease_progression(BariatricDiseaseProgression)

    def output_oca_disease_progression(self):
        self.output_file = 'oca_disease_progression.csv'
        self.output_disease_progression(OCADiseaseProgression)
