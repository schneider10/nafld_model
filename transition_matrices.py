import itertools
import numpy as np
from mortality import Mortality
from inputs import ModelInputs


class Regression:

    @staticmethod
    def calculate(value):
        return value * ModelInputs.age_specific_rr['Disease Regression RR']


class Progression:

    @staticmethod
    def calculate(value):
        return value * ModelInputs.age_specific_rr['Disease Progression RR ']


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
        ).assign(Cohorts=age_cohort).set_index('Cohorts', append=True).swaplevel(i=0, j=1)

    def insert_residual_probabilities(self):
        """
        Calculates All Residual Probabilities for each row in the transition matrix and insert them into their correct location.
        Residual Probability is set to None in 'insert_probabilities' to allow 'fillna' to insert these probabilities.
        """

        residual_probabilities = self.df.apply(lambda x: 1 - np.sum(x), axis=1)

        for age_cohort, state in residual_probabilities.index:
            self.df.loc[age_cohort, state].fillna(residual_probabilities[age_cohort, state], inplace=True)

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
        self.f3_to_f2 = ModelInputs.bariatric_substitutions['F3, F2 transition probability ']

        if year is not None:
            self.generate_bariatric_df(year)

    def generate_bariatric_df(self, year):
        """
        need to generate new substitution dfs based on f2 to f1 and f3 to f2 bariatric probability substitutions.
        new df for every year.
        :param year:
        :return:
        """
        self.set_probability(initial_state='F2', final_state='F1', probability=self.f2_to_f1[year])
        self.set_probability(initial_state='F3', final_state='F2', probability=self.f3_to_f2[year])


def generate_bariatric_transition_matrices():
    bariatric_transition_matrices = {}

    for yr in ModelInputs.bariatric_substitutions.index:
        for cohort in ModelInputs.cohorts:
            bariatric_transition_matrices.update(
                {f'{yr}:{cohort}': BariatricTransitionMatrices(year=yr).generate_transition_matrix(cohort)}
            )
            df = BariatricTransitionMatrices(year=yr).generate_transition_matrix(cohort)
            df.to_csv(f'{yr}-bariatric_t_matrices.csv', mode='a')
