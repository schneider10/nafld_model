import itertools
import numpy as np
import pandas as pd
from mortality import Mortality
from inputs import ModelInputs


class Regression:

    @staticmethod
    def calculate(value):
        return value * ModelInputs.age_specific_rr['Disease Regression RR']


class Progression:

    @staticmethod
    def calculate(value):
        return value * ModelInputs.age_specific_rr['Disease Progression RR']


class HccToLt:

    @staticmethod
    def calculate(value):
        return value * ModelInputs.age_specific_rr['HCC, LT Y1 RR']


class TransitionMatrices(Mortality):
    def __init__(self):
        super().__init__()
        self.df = ModelInputs.transition_probabilities  # matrix with all the string substitutions
        self.disease_states = ModelInputs.disease_states

    def set_probability(self, initial_state, final_state, probability):
        self.df.loc[initial_state, final_state] = probability
        # print(f'Setting {initial_state}: {final_state} to {probability}')

    def get_transition_type(self, initial_state, final_state):
        """
        Check if transition is regression, HCC and LT, progression or if they are the same (do nothing)
        """
        # Todo: make less brittle by making another table that maps transitions to values and factors
        if list(self.disease_states).index(initial_state) > list(self.disease_states).index(final_state):
            return Regression
        elif ('HCC' in initial_state) and ('LT' in final_state):
            return HccToLt
        elif initial_state == final_state:
            return None
        else:
            return Progression

    def replace_strings_with_inputs(self, age_cohort):
        """ Replace all the strings with input values, see what transition_probability looks like. """
        self.df = self.df.replace(
            {'NAFLD annual probability': ModelInputs.NAFLD_annual_probabilities.loc[age_cohort],
             'Background mortality annual probability': ModelInputs.background_mortality.loc[age_cohort],
             'NAFLD mortality probability': self.mortality_prob['NAFLD mortality probability'].loc[age_cohort],
             'F1 mortality probability': self.mortality_prob['F1 mortality probability'].loc[age_cohort],
             'F2 mortality probability': self.mortality_prob['F2 mortality probability'].loc[age_cohort],
             'F3 mortality probability': self.mortality_prob['F3 mortality probability'].loc[age_cohort],
             'F4 mortality probability': self.mortality_prob['F4 mortality probability'].loc[age_cohort],
             'residual_prob': None}
        )

    def insert_residual_probabilities(self):
        """
        Calculates All Residual Probabilities for each row in the transition matrix and insert them into their correct location.
        Residual Probability is set to None in 'insert_probabilities' to allow 'fillna' to insert these probabilities.
        """

        residual_probabilities = self.df.apply(lambda x: 1 - np.sum(x), axis=1)

        for state in residual_probabilities.index:
            self.df.loc[state].fillna(residual_probabilities[state], inplace=True)

    def generate_transition_matrix(self, age_cohort):
        """
        Substitute strings in transition matrix with associated input values for each age cohort.
        transition_matrices = {}

        for cohort in ModelInputs.cohorts:
            transition_matrices.update({cohort: TransitionMatrices().generate_transition_matrix(cohort)})
        """

        # Loop through every possible transition and calculate progression probability if necessary
        for initial_state, final_state in itertools.product(self.disease_states, self.disease_states):

            # Get value using x and y coordinates
            value = self.df.loc[initial_state, final_state]

            # if value is not a string and and final state != 'death'
            if not isinstance(value, str) and final_state != 'death':
                # Get the transition type based on initial and final state
                transition_type = self.get_transition_type(initial_state, final_state)
                if transition_type:
                    probability = transition_type.calculate(value)[age_cohort]
                    self.set_probability(initial_state, final_state, probability)

        self.replace_strings_with_inputs(age_cohort)
        self.insert_residual_probabilities()
        return self.df


class BariatricTransitionMatrices(TransitionMatrices):
    def __init__(self, year=None):
        """
        Bariatric Transition Matrices are the same as the normal transition matrices with the exception that they
        also contain extra matrices for Years 1-5 for every cohort (5 x cohort amount extra matrices).
        """
        super().__init__()
        # transition prob located in 'progression calc'
        self.f2_to_f1 = ModelInputs.bariatric_substitutions['F2, F1 transition probability']
        self.f3_to_f2 = ModelInputs.bariatric_substitutions['F3, F2 transition probability']
        self.f1_to_f2 = ModelInputs.bariatric_substitutions['F1, F2 transition probability']
        self.f2_to_f3 = ModelInputs.bariatric_substitutions['F2, F3 transition probability']

        if year is not None:
            self.generate_bariatric_df(year)

    def generate_bariatric_df(self, year):
        """
        need to generate new substitution dfs based on f2 to f1 and f3 to f2 bariatric probability substitutions.
        new df for every year.
        :param year:
        :return:
        """
        transitions = (('F2', 'F1', self.f2_to_f1),
                       ('F3', 'F2', self.f3_to_f2),
                       ('F1', 'F2', self.f1_to_f2),
                       ('F2', 'F3', self.f2_to_f3)
                       )
        for initial_state, final_state, probability in transitions:
            self.set_probability(initial_state, final_state, probability[year])


class OCATransitionMatrices(TransitionMatrices):
    def __init__(self, year=None):
        """
        OCA Transition Matrices are the same as the normal transition matrices with the exception that they
        also contain extra matrices for Years 1-5 for every cohort (5 x cohort amount extra matrices).
        """
        super().__init__()
        # transition prob located in 'progression calc'
        self.f2_to_f1 = ModelInputs.oca_substitutions['F2, F1 transition probability']
        self.f3_to_f2 = ModelInputs.oca_substitutions['F3, F2 transition probability']
        self.f1_to_f2 = ModelInputs.oca_substitutions['F1, F2 transition probability']
        self.f2_to_f3 = ModelInputs.oca_substitutions['F2, F3 transition probability']
        self.f3_to_f1 = ModelInputs.oca_substitutions['F3, F1 transition probability']
        self.f2_to_nafld_y2_beyond = ModelInputs.oca_substitutions['F2, NAFLD Y2-beyond transition probability']

        if year is not None:
            self.generate_oca_df(year)

    def generate_oca_df(self, year):
        """
        need to generate new substitution dfs based on f2 to f1 and f3 to f2 oca probability substitutions.
        new df for every year.
        :param year:
        :return:
        """
        transitions = (('F2', 'F1', self.f2_to_f1),
                       ('F3', 'F2', self.f3_to_f2),
                       ('F1', 'F2', self.f1_to_f2),
                       ('F2', 'F3', self.f2_to_f3),
                       ('F3', 'F1', self.f3_to_f1),
                       ('F2', 'NAFLD Y2-beyond', self.f2_to_nafld_y2_beyond)
                       )
        for initial_state, final_state, probability in transitions:
            self.set_probability(initial_state, final_state, probability[year])


def generate_alternative_transition_matrices(year_index, transition_matrix, matrix_name):
    transition_matrices = {}

    for yr in year_index:
        for cohort in ModelInputs.cohorts:
            transition_matrices.update(
                {f'{yr}:{cohort}': transition_matrix(year=yr).generate_transition_matrix(cohort)}
            )
            df = transition_matrix(year=yr).generate_transition_matrix(cohort)
            output_file = f'{yr}-{matrix_name}_t_matrices.csv'

            pd.DataFrame({'Cohort': cohort}, index=['Cohort']).to_csv(output_file, mode='a')
            df.to_csv(output_file, mode='a')


def generate_bariatric_transition_matrices():
    year_index = ModelInputs.bariatric_substitutions.index
    generate_alternative_transition_matrices(year_index, BariatricTransitionMatrices, 'bariatric')


def generate_oca_transition_matrices():
    year_index = ModelInputs.oca_substitutions.index
    generate_alternative_transition_matrices(year_index, OCATransitionMatrices, 'oca')
