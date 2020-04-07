import pandas as pd

from inputs import ModelInputs
from transition_matrices import TransitionMatrices, BariatricTransitionMatrices, OCATransitionMatrices
from prevalence import StatePrevalence


class DiseaseProgression:
    """ We must multiply each transition matrix by its corresponding disease prevalence array.
    These results are stored in the progression_df dataframe.
    """
    year_interval = range(5)
    disease_prevalence = StatePrevalence().calculate_disease_prevalence_per_age_cohort()

    def __init__(self, initial_cohort):
        super().__init__()

        # Get age cohorts specific to the initial cohort selected.
        self.age_cohorts = ModelInputs.cohorts[ModelInputs.cohorts.index(initial_cohort):]

        # Get initial prevalence array for initial cohort.
        self.progression_df = self.disease_prevalence.loc[[initial_cohort]].reset_index(drop=True)
        self.prevalence_array = self.progression_df.to_numpy()[0]

    def calculate_disease_progression(self):
        for cohort in self.age_cohorts:
            # Get transition matrix for current cohort if transition matrices are traditional.
            transition_matrix = TransitionMatrices().generate_df(cohort)

            # Cycle through the year interval for every age cohort
            for year in self.year_interval:
                # Multiply cohorts transition matrix by prevalence array for every year in year interval
                self.prevalence_array = self.prevalence_array.dot(transition_matrix)

                self.progression_df = self.progression_df.append(
                    pd.Series(self.prevalence_array, index=self.progression_df.columns), ignore_index=True
                )
        return self.progression_df


class BariatricDiseaseProgression(DiseaseProgression):
    def __init__(self, initial_cohort):
        super().__init__(initial_cohort)

    def calculate_disease_progression(self):
        for cohort in self.age_cohorts:

            # Cycle through the year interval for every age cohort
            for year in self.year_interval:
                transition_matrix = BariatricTransitionMatrices(year).generate_df(cohort)
                # Multiply cohorts transition matrix by prevalence array for every year in year interval
                prevalence_array = self.prevalence_array.dot(transition_matrix)

                self.progression_df = pd.concat([self.progression_df, prevalence_array])


class OCADiseaseProgression(DiseaseProgression):
    def __init__(self, initial_cohort):
        super().__init__(initial_cohort)

    def calculate_disease_progression(self):
        for cohort in self.age_cohorts:

            # Cycle through the year interval for every age cohort
            for year in self.year_interval:
                transition_matrix = OCATransitionMatrices(year).generate_df(cohort)
                # Multiply cohorts transition matrix by prevalence array for every year in year interval
                prevalence_array = self.prevalence_array.dot(transition_matrix)

                self.progression_df = pd.concat([self.progression_df, prevalence_array])


if __name__ == '__main__':
    for age_cohort in ModelInputs.cohorts:
        DiseaseProgression(age_cohort).calculate_disease_progression()
