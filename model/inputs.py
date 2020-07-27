import pandas as pd
import os


class ModelInputs:
    def __init__(self, input_file='model_inputs.xlsx'):
        self.raw_input = pd.read_excel(input_file, sheet_name=None)

        self.NAFLD_inputs = self.raw_input['Cohort and NAFLD Prevalence'].set_index('Cohorts')

        self.other_disease_inputs = self.raw_input['Other Disease State Prevalences'].set_index('Disease States')

        self.background_mortality = self.raw_input['Age-specific Probabilities'].set_index('Age Cohorts')[
            'Background mortality annual probability']

        self.NAFLD_annual_probabilities = self.raw_input['Age-specific Probabilities'].set_index('Age Cohorts')[
            'NAFLD annual probability']

        self.age_specific_rr = self.raw_input['Age-specific Relative Risks'].set_index('Age Cohorts')

        self.transition_probabilities = self.raw_input['Transition Probabilities'].set_index('Base Transition Matrix')

        self.mortality_risk = self.raw_input['Disease-specific Mortality Risk'].set_index('Disease States')

        self.scoring_and_costing = self.raw_input['Health Scoring and Costing'].set_index('Disease States').fillna(0)

        self.bariatric_substitutions = self.raw_input['Treatment Effects'].set_index('Treatment Year')

        self.oca_substitutions = self.raw_input['OCA Effects'].set_index('Treatment Year')

        self.cohorts = self.NAFLD_inputs.index.tolist()

        self.disease_states = self.transition_probabilities.index


# Load inputs to be accessed globally.
if os.environ['TESTING']:
    inputs = ModelInputs(input_file='test_model_inputs.xlsx')
else:
    inputs = ModelInputs()


def round_4(num):
    """ Rounds to four decimal points for test result precision. """
    return round(num, 4)
