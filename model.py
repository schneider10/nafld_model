from copy import copy
import pandas as pd

from inputs import ModelInputs
from transition_matrices import TransitionMatrices
from prevalence import StatePrevalence


class DiseaseProgression(TransitionMatrices):
    """ We must multiply each transition matrix by its corresponding disease prevalence array.
    These results are stored in the progression_df dataframe.
    """
    year_interval = range(5)

    disease_prevalence = StatePrevalence().calculate_disease_prevalence_per_age_cohort()

    def __init__(self):
        super().__init__()
        self.progression_df = None
        self.current_year = 0

    def initialize_progression_df(self, initial_cohort):

        # Get initial prevalence array for initial cohort
        initial_prevalence = self.disease_prevalence.loc[[initial_cohort]]

        # A copy of this must be made before the 'Year' column is added for matrix multiplication
        prevalence_array = copy(initial_prevalence)
        initial_prevalence['Year'] = self.current_year

        if self.progression_df is None:
            # If progression dataframe has not yet been created, assign it to initial prevalence
            self.progression_df = initial_prevalence

        else:
            # If dataframe has been created, concatenate initial prevalence to main dataframe
            self.progression_df = pd.concat([self.progression_df, initial_prevalence])

        # Get age cohorts specific to the initial cohort selected
        age_cohorts = ModelInputs.cohorts[ModelInputs.cohorts.index(initial_cohort):]

        return prevalence_array, age_cohorts

    def calculate_disease_progression(self):

        for initial_cohort in ModelInputs.cohorts:

            self.current_year = 0
            prevalence_array, age_cohorts = self.initialize_progression_df(initial_cohort)

            for age_cohort in age_cohorts:

                # Cycle through the year interval for every age cohort.
                for year in self.year_interval:
                    # increment current year by 1
                    self.current_year += 1

                    # Multiply transition matrix by prevalence array
                    prevalence_array = prevalence_array.dot(self.generate_transition_matrix(age_cohort))

                    # A copy of this array must be made so adding the 'Year' column to this row
                    # doesn't affect the multiplied array

                    new_progression_row = copy(prevalence_array)
                    new_progression_row['Year'] = self.current_year

                    self.progression_df = pd.concat([self.progression_df, new_progression_row])

        # Add "year" to index to make a multi-index
        return self.progression_df.set_index('Year', append=True)


if __name__ == '__main__':
    DiseaseProgression().calculate_disease_progression()
