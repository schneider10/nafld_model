import pandas as pd
from inputs import inputs
import pytest

# before writing tests, lets get each testable step to output results nicely here.
from transition_matrices import BariatricTransitionMatrices, OCATransitionMatrices


def generate_alternative_transition_matrices(year_index, transition_matrix, matrix_name):
    transition_matrices = {}

    for yr in year_index:
        for cohort in inputs.cohorts:
            transition_matrices.update(
                {f'{yr}:{cohort}': transition_matrix(year=yr).generate_transition_matrix(cohort)}
            )
            df = transition_matrix(year=yr).generate_transition_matrix(cohort)
            output_file = f'{yr}-{matrix_name}_t_matrices.csv'

            pd.DataFrame({'Cohort': cohort}, index=['Cohort']).to_csv(output_file, mode='a')
            df.to_csv(output_file, mode='a')


def generate_bariatric_transition_matrices():
    year_index = inputs.bariatric_substitutions.index
    generate_alternative_transition_matrices(year_index, BariatricTransitionMatrices, 'bariatric')


def generate_oca_transition_matrices():
    year_index = inputs.oca_substitutions.index
    generate_alternative_transition_matrices(year_index, OCATransitionMatrices, 'oca')



