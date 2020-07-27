# Model begins here
from model.disease_progression import BariatricDiseaseProgression, OCADiseaseProgression
from model.final_calculations import OutputFinalCalculations


def run_model():
    bariatric_results = OutputFinalCalculations(BariatricDiseaseProgression,
                                                'outputs/bariatric_final_calculations.csv').final_calculations

    oca_results = OutputFinalCalculations(OCADiseaseProgression,
                                          'outputs/oca_final_calculations.csv').final_calculations

    return bariatric_results, oca_results


if __name__ == '__main__':
    run_model()
