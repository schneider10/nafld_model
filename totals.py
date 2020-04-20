import pandas as pd

from inputs import inputs
from disease_progression import DiseaseProgression, BariatricDiseaseProgression, OCADiseaseProgression


class Totals:
    """ We need to sum all values in the matrix above, at specified intervals.
        Split big matrix into chunks based on interval. Sum all values in chunk to get life years at interval.
    """

    def __init__(self, progression, cohort):
        self.disease_progression_matrix = progression(cohort).calculate_progression()

    def get_total_life_years(self):
        """ Calculate total life years by summing all of the progression values
        """
        return self.disease_progression_matrix.to_numpy().sum()

    def get_total_QALY(self):
        """ Calculate total QALY by summing each column of progression values,
            weighing these values and summing them. """
        return self.disease_progression_matrix.sum(axis=0).multiply(
            inputs.scoring_and_costing['Quality Weight']).sum()

    def get_total_cost(self):
        """ Calculate total cost by summing each column of progression values, weighing these values with a cost,
        summing them and then adding the total difference of death progression (delta death). """

        first_year_costs = inputs.scoring_and_costing.loc['death']['First year costs']

        total_cost = self.disease_progression_matrix.sum(axis=0).multiply(
            inputs.scoring_and_costing['Per patient per year cost']).sum()

        delta_death = (self.disease_progression_matrix.iloc[-1]['death'] -
                       self.disease_progression_matrix.iloc[0]['death']) * first_year_costs

        return total_cost + delta_death

    @staticmethod
    def get_total_cost_pppy(total_cost, total_life_years):
        return total_cost / total_life_years

    def get_totals(self):
        """ For every initial age cohort, calculate all aggregate values.
        """

        total_life_years = self.get_total_life_years()
        total_QALY = self.get_total_QALY()
        total_cost = self.get_total_cost()
        total_cost_pppy = self.get_total_cost_pppy(total_cost, total_life_years)

        return [total_life_years, total_QALY, total_cost, total_cost_pppy]


class OutputTotals:
    def __init__(self):
        self.final_calculations = pd.DataFrame({'Totals': ['Total Life Years',
                                                           'Total QALY',
                                                           'Total Cost',
                                                           'Total Cost PPPY']}).set_index('Totals')

    def output_totals_df(self, disease_progression, output_file=None):
        for cohort in inputs.cohorts:
            disease_progression_matrix = disease_progression(cohort).calculate_progression()

            # populate final calculations dataframe
            self.final_calculations[cohort] = Totals(disease_progression_matrix).get_totals()

            # Calculate the sum of these totals for all cohorts
        self.final_calculations['All Cohorts'] = self.final_calculations.sum(axis=1)
        if output_file:
            self.final_calculations.to_csv(output_file)

        return self.final_calculations

    def get_control_totals_df(self, output_file=None):
        return self.output_totals_df(DiseaseProgression, output_file)

    def get_bariatric_totals_df(self, output_file=None):
        return self.output_totals_df(BariatricDiseaseProgression, output_file)

    def get_oca_totals_df(self, output_file=None):
        return self.output_totals_df(OCADiseaseProgression, output_file)
