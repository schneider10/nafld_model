import numpy as np
import pandas as pd

from model.inputs import inputs


# Prevalence Calculations
class StatePrevalence:

    def __init__(self):
        self.disease_prevalence_per_age_cohort = self.calculate_disease_prevalence_per_age_cohort()

    def calculate_disease_prevalence_per_age_cohort(self):
        """ """
        zeros_column = np.zeros(len(inputs.NAFLD_inputs.index))
        fibrosis_states_per_age_cohort = {fibrosis_state: self.calculate_fibrosis_per_age_cohort(fibrosis_state)
                                          for fibrosis_state in ['F1', 'F2', 'F3', 'F4']}

        # Assign calculation results to columns
        disease_prevalence_data = \
            {'No NAFLD': self.calculate_no_NAFLD_per_age_cohort(),
             'NAFLD Y1': zeros_column,
             'NAFLD Y2-beyond': self.calculate_NAFLD_per_age_cohort(),
             **fibrosis_states_per_age_cohort,
             'DCC': self.calculate_total_cirrhosis_per_age_cohort(),
             'HCC Y1': zeros_column,
             'HCC Y2-beyond': self.calculate_NASH_HCC_per_age_cohort(fibrosis_states_per_age_cohort),
             'LT Y1': zeros_column,
             'LT Y2-beyond': self.calculate_cirrhosis_LT_per_age_cohort(),
             'death': zeros_column}

        # Return a dataframe from this dictionary with the same index as NAFLD input
        return pd.DataFrame(disease_prevalence_data, index=inputs.NAFLD_inputs.index)

    def calculate_NAFLD_per_age_cohort(self):
        # Multiply NAFLD prevalence by age by sample per age cohort
        return inputs.NAFLD_inputs['NAFLD prevalence by age'] * inputs.NAFLD_inputs['Sample per cohort']

    def calculate_no_NAFLD_per_age_cohort(self):
        # Subtract NAFLD prevalence from sample per age cohort to calculate no NAFLD prevalence per age cohort
        return inputs.NAFLD_inputs['Sample per cohort'] - self.calculate_NAFLD_per_age_cohort()

    def calculate_fibrosis_per_age_cohort(self, disease_state):
        # Multipy Disease Prevalence Adjustment by F1, F2, F3, F4 non-age specific prevalence by NAFLD prevalence
        return inputs.NAFLD_inputs['Disease Prevalence Adjustment'] \
               * inputs.other_disease_inputs.loc[disease_state]['Non-age specific prevalence'] \
               * self.calculate_NAFLD_per_age_cohort()

    def calculate_total_cirrhosis_per_age_cohort(self):
        # Multiply Disease Prevalence Adjustment by cirrhohsis non-age specific prevalence by sample per cohort
        return inputs.NAFLD_inputs['Disease Prevalence Adjustment'] \
               * inputs.other_disease_inputs.loc['DCC']['Non-age specific prevalence'] \
               * inputs.NAFLD_inputs['Sample per cohort']

    def calculate_NASH_HCC_per_age_cohort(self, fibrosis_states_per_age_cohort):
        """ Multiple Disease Prevalence Adjustment by NASH HCC non-age specific prevalence
        by the total NASH patients in each age cohort """
        return inputs.NAFLD_inputs['Disease Prevalence Adjustment'] \
               * inputs.other_disease_inputs.loc['HCC']['Non-age specific prevalence'] \
               * sum(fibrosis_states_per_age_cohort.values())

    def calculate_cirrhosis_LT_per_age_cohort(self):
        """ Multiply Disease Prevalence Adjustment by LT non-age specific prevalence
        by the total cirrhosis patients in each age cohort """
        return inputs.NAFLD_inputs['Disease Prevalence Adjustment'] \
               * self.calculate_total_cirrhosis_per_age_cohort() \
               * inputs.other_disease_inputs.loc['LT']['Non-age specific prevalence']
