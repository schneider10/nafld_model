import pandas as pd
from model.inputs import inputs

# before writing tests, lets get each testable step to output results nicely here.
from model.transition_matrices import BariatricTransitionMatrices, OCATransitionMatrices, TransitionMatrices


def generate_alternative_transition_matrices(year_index, transition_matrix=TransitionMatrices, matrix_name='control'):
    for yr in year_index:
        for cohort in inputs.cohorts:
            matrix = transition_matrix(year=yr).generate_df(cohort)
            output_file = f'outputs/{yr}-{matrix_name}_t_matrices.csv'
            pd.DataFrame({'Cohort': cohort}, index=['Cohort']).to_csv(output_file, mode='a')
            matrix.to_csv(output_file, mode='a')

            yield {f'{yr}:{cohort}': matrix}


def generate_bariatric_transition_matrices():
    year_index = inputs.bariatric_substitutions.index
    return generate_alternative_transition_matrices(year_index, BariatricTransitionMatrices, 'bariatric')


def generate_oca_transition_matrices():
    year_index = inputs.oca_substitutions.index
    return generate_alternative_transition_matrices(year_index, OCATransitionMatrices, 'oca')


def test_bariatric_transition_matrix_generation(test_inputs):
    matrices = generate_bariatric_transition_matrices()
    for m in matrices:
        test_case = {'matrix': 'Tx Year 1:45-49', 'sum': 12.31293563228806}

        if test_case['matrix'] in m:
            assert m[test_case['matrix']].to_numpy().sum() == test_case['sum']
            break


def test_oca_transition_matrix_generation(test_inputs):
    matrices = generate_oca_transition_matrices()
    for m in matrices:
        test_case = {'matrix': 'Tx Year 1:45-49', 'sum': 12.174775270831246}

        if test_case['matrix'] in m:
            assert m[test_case['matrix']].to_numpy().sum() == test_case['sum']
            break


def test_control_transition_matrix_generation(test_inputs):
    for cohort in inputs.cohorts:
        matrix = TransitionMatrices().generate_df(cohort)
