import pandas as pd
from model.inputs import inputs, round_4


class Mortality:

    def __init__(self):
        self.mortality_prob = self.create_mortality_probability_dataframe()

    def get_disease_state_mortality_RR(self, disease_state):
        # Inherit Model Inputs
        return inputs.mortality_risk.loc[disease_state]['Relative Risk of Mortality']

    def create_mortality_probability_dataframe(self):
        # Create an empty dataframe with same index as Mortality inputs

        self.mortality_prob = pd.DataFrame(index=inputs.NAFLD_inputs.index)
        self.mortality_prob['Background mortality annual probability'] = inputs.background_mortality
        self.mortality_prob['NAFLD mortality RR'] = inputs.age_specific_rr['NAFLD mortality RR']

        # Calculate mortality probabilities for NAFLD, F1, F2, F3, and F4
        for disease_state in ['NAFLD', 'F1', 'F2', 'F3', 'F4']:
            self.mortality_prob[f'{disease_state} mortality probability'] = \
                round_4(inputs.background_mortality
                        * inputs.age_specific_rr['NAFLD mortality RR']
                        * self.get_disease_state_mortality_RR(disease_state))

        return self.mortality_prob
