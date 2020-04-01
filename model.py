import pandas as pd

from inputs import ModelInputs
from transition_matrices import TransitionMatrices, generate_bariatric_transition_matrices, generate_oca_transition_matrices
from prevalence import StatePrevalence


class DiseaseProgression(TransitionMatrices):
    """ We must multiply each transition matrix by its corresponding disease prevalence array.
    These results are stored in the progression_df dataframe.
    """
    year_interval = range(5)
    disease_prevalence = StatePrevalence().calculate_disease_prevalence_per_age_cohort()

    def __init__(self, initial_cohort):
        super().__init__()
        # Get initial prevalence array for initial cohort.
        self.progression_df = self.disease_prevalence.loc[[initial_cohort]]

        # Get age cohorts specific to the initial cohort selected.
        self.age_cohorts = ModelInputs.cohorts[ModelInputs.cohorts.index(initial_cohort):]

    #     # Get initial prevalence array for initial cohort
    #     initial_prevalence = self.disease_prevalence.loc[[initial_cohort]]
    #
    #     # A copy of this must be made before the 'Year' column is added for matrix multiplication
    #     prevalence_array = initial_prevalence.values
    #
    #     # If progression df has not yet been created, assign it to initial prevalence
    #     self.progression_df = initial_prevalence
    #
    #     # Get age cohorts specific to the initial cohort selected
    #     age_cohorts = ModelInputs.cohorts[ModelInputs.cohorts.index(initial_cohort):]
    #
    #     return prevalence_array, age_cohorts

    def calculate_disease_progression(self):

        year_num = 0
        prevalence_array = self.progression_df.values

        for cohort in self.age_cohorts:

            # Cycle through the year interval for every age cohort.
            for year in self.year_interval:
                # increment current year by 1
                year_num += 1

                # Multiply transition matrix by prevalence array
                transition_matrix = self.generate_transition_matrix(cohort)
                prevalence_array = prevalence_array.dot(transition_matrix)

                self.progression_df = pd.concat([self.progression_df, prevalence_array])

        return self.progression_df


if __name__ == '__main__':
    generate_oca_transition_matrices()
    # for cohort in ModelInputs.cohorts:
    #     DiseaseProgression(cohort).calculate_disease_progression()
