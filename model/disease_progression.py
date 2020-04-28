import pandas as pd

from model.inputs import inputs
from model.transition_matrices import TransitionMatrices, BariatricTransitionMatrices, OCATransitionMatrices
from model.state_prevalence import StatePrevalence


class DiseaseProgression:
    """ We must multiply each transition matrix by its corresponding disease prevalence array.
    These results are stored in the progression_df dataframe.
    """
    disease_prevalence = StatePrevalence().calculate_disease_prevalence_per_age_cohort()

    def __init__(self, initial_cohort):
        super().__init__()

        # Get age cohorts specific to the initial cohort selected.
        self.relevant_age_cohorts = inputs.cohorts[inputs.cohorts.index(initial_cohort):]

        # Get initial prevalence array for initial cohort.
        self.progression_df = self.disease_prevalence.loc[[initial_cohort]].reset_index(drop=True)

        self.prevalence_array = self.progression_df.to_numpy()[0]
        self.default_year_interval = range(5)

    def calculate_progression(self):
        for cohort in self.relevant_age_cohorts:

            # Get transition matrix for current cohort if transition matrices are traditional.
            transition_matrix = TransitionMatrices().generate_df(cohort)

            # Cycle through the year interval for every age cohort
            for _ in self.default_year_interval:
                # Multiply cohorts transition matrix by prevalence array for every year in year interval
                self.prevalence_array = self.prevalence_array.dot(transition_matrix)

                self.progression_df = self.progression_df.append(
                    pd.Series(self.prevalence_array, index=self.progression_df.columns), ignore_index=True
                )
        return self.progression_df


class AlternativeDiseaseProgression(DiseaseProgression):
    def __init__(self, initial_cohort, transition_matrices):
        super().__init__(initial_cohort)
        self.initial_cohort = initial_cohort
        self.alternative_transition_matrices = transition_matrices

    def is_initial_cohort(self, cohort):
        return cohort == self.initial_cohort

    def calculate_progression(self):
        for cohort in self.relevant_age_cohorts:
            if self.is_initial_cohort(cohort):

                # Cycle through the year interval for every age cohort. Range is 5 for 5 new bariatric tx matrices.
                for year in self.default_year_interval:
                    transition_matrix = self.alternative_transition_matrices(year).generate_df(cohort)

                    # Multiply cohorts transition matrix by prevalence array for every year in year interval
                    self.prevalence_array = self.prevalence_array.dot(transition_matrix)

                    self.progression_df = self.progression_df.append(
                        pd.Series(self.prevalence_array, index=self.progression_df.columns), ignore_index=True
                    )
            else:
                transition_matrix = TransitionMatrices().generate_df(cohort)

                # Cycle through the year interval for every age cohort
                for _ in self.default_year_interval:
                    # Multiply cohorts transition matrix by prevalence array for every year in year interval
                    self.prevalence_array = self.prevalence_array.dot(transition_matrix)

                    self.progression_df = self.progression_df.append(
                        pd.Series(self.prevalence_array, index=self.progression_df.columns), ignore_index=True
                    )

        return self.progression_df


class BariatricDiseaseProgression(AlternativeDiseaseProgression):
    substitutions = inputs.bariatric_substitutions

    def __init__(self, initial_cohort):
        super().__init__(initial_cohort, BariatricTransitionMatrices)


class OCADiseaseProgression(AlternativeDiseaseProgression):
    substitutions = inputs.oca_substitutions

    def __init__(self, initial_cohort):
        super().__init__(initial_cohort, OCATransitionMatrices)
