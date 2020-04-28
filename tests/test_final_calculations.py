from model.disease_progression import BariatricDiseaseProgression, OCADiseaseProgression
from model.final_calculations import FinalCalculations
from model.inputs import inputs

if __name__ == '__main__':
    treatments = [BariatricDiseaseProgression, OCADiseaseProgression]

    for treatment in treatments:
        for age_cohort in inputs.cohorts:
            t = FinalCalculations(treatment, age_cohort).get_icer()
            print(t)