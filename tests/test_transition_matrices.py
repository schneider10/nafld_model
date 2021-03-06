import pandas as pd
from model.inputs import inputs, round_4

# before writing tests, lets get each testable step to output results nicely here.
from model.transition_matrices import BariatricTransitionMatrices, OCATransitionMatrices, TransitionMatrices


class OutputTransitionMatrices:
    def __init__(self, transition_matrix=TransitionMatrices):
        self.transition_matrix = transition_matrix

    def output_alt_transition_matrices(self):
        for yr in self.transition_matrix.year_index:
            output_file = f'outputs/matrices/{self.transition_matrix.name}-{yr}_t_matrices.csv'
            pd.DataFrame().to_csv(output_file)

            for cohort in inputs.cohorts:
                matrix = self.transition_matrix(year=yr).generate_df(cohort)
                pd.DataFrame({'Cohort': cohort}, index=['Cohort']).to_csv(output_file, mode='a')
                matrix.to_csv(output_file, mode='a')

                yield {f'{yr}:{cohort}': matrix}

    def output_control_transition_matrices(self):
        output_file = f'outputs/matrices/control_t_matrices.csv'
        pd.DataFrame().to_csv(output_file)

        for cohort in inputs.cohorts:
            matrix = self.transition_matrix().generate_df(cohort)
            pd.DataFrame({'Cohort': cohort}, index=['Cohort']).to_csv(output_file, mode='a')
            matrix.to_csv(output_file, mode='a')

            yield {f'{cohort}': matrix}


def test_bariatric_transition_matrix_generation():
    # TODO: add test to assert rows add up to one
    matrices = OutputTransitionMatrices(BariatricTransitionMatrices).output_alt_transition_matrices()
    for m in matrices:
        test_case = {'cohort': 'Tx Year 5:75-79', 'sum': 13.1806}

        if test_case['cohort'] in m:
            matrix_sum = m[test_case['cohort']].to_numpy().sum()
            assert round_4(matrix_sum) == test_case['sum']

    
def test_oca_transition_matrix_generation():
    matrices = OutputTransitionMatrices(OCATransitionMatrices).output_alt_transition_matrices()
    for m in matrices:
        test_case = {'cohort': 'Tx Year 5:75-79', 'sum': 13.1806}

        if test_case['cohort'] in m:
            matrix_sum = m[test_case['cohort']].to_numpy().sum()
            assert round_4(matrix_sum) == test_case['sum']


def test_control_transition_matrix_generation():
    matrices = OutputTransitionMatrices().output_control_transition_matrices()
    for m in matrices:
        test_case = {'cohort': '75-79', 'sum': 13.1806}

        if test_case['cohort'] in m:
            matrix_sum = m[test_case['cohort']].to_numpy().sum()
            assert round_4(matrix_sum) == test_case['sum']
