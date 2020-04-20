from disease_progression import BariatricDiseaseProgression, OCADiseaseProgression
from final_calculations import FinalCalculations
from inputs import inputs

if __name__ == '__main__':
    treatments = [BariatricDiseaseProgression, OCADiseaseProgression]

    for treatment in treatments:
        for age_cohort in inputs.cohorts:
            t = FinalCalculations(treatment, age_cohort).get_icer()
            print(t)