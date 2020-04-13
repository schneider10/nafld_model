import pandas as pd
from inputs import ModelInputs
from disease_progression import DiseaseProgression


class FinalCalculations:
    """ We need to sum all values in the matrix above, at specified intervals.
        Split big matrix into chunks based on interval. Sum all values in chunk to get life years at interval.
    """

    def __init__(self, disease_progression):
        super().__init__()
        self.disease_progression = disease_progression
        self.final_calculations = pd.DataFrame({'Totals': ['Total Life Years',
                                                           'Total QALY',
                                                           'Total Cost',
                                                           'Total Cost PPPY']}).set_index('Totals')

    def get_total_life_years(self, cohort):
        """ Calculate total life years by summing all of the progression values
        """
        return self.disease_progression(cohort).calculate_progression().to_numpy().sum()

    def get_total_QALY(self, cohort):
        """ Calculate total QALY by summing each column of progression values,
            weighing these values and summing them. """
        return self.disease_progression.loc[cohort].sum(axis=0).multiply(
            ModelInputs.scoring_and_costing['Quality Weight']).sum()

    def get_total_cost(self, cohort):
        """ Calculate total cost by summing each column of progression values, weighing these values with a cost,
        summing them and then adding the total difference of death progression (delta death). """

        first_year_costs = ModelInputs.scoring_and_costing.loc['death']['First year costs']

        total_cost = self.disease_progression.loc[cohort].sum(axis=0).multiply(
            ModelInputs.scoring_and_costing['PPPY cost']).sum()
        delta_death = (self.disease_progression.loc[cohort].iloc[-1]['death'] -
                       self.disease_progression.loc[cohort].iloc[0]['death']) * first_year_costs
        return total_cost + delta_death

    def get_totals(self):
        """ For every initial age cohort, calculate all aggregate values.
        """

        for cohort in ModelInputs.cohorts:
            total_life_years = self.get_total_life_years(cohort)
            total_QALY = self.get_total_QALY(cohort)
            total_cost = self.get_total_cost(cohort)
            total_cost_pppy = total_cost / total_life_years

            self.final_calculations[cohort] = [total_life_years, total_QALY,
                                               total_cost, total_cost_pppy]

        # Calculate the sum of these totals for all cohorts
        self.final_calculations['All Cohorts'] = self.final_calculations.sum(axis=1)

        return self.final_calculations


FinalCalculations().get_totals()


def __init__(self):
    self.bariatric_totals = MarkovModel(type='bariatric').aggregate_cohort_totals()
    self.control_totals = MarkovModel().aggregate_cohort_totals()


def calculate_ICER(self):
    total_cost_diff = self.bariatric_totals['Total Cost'] - self.control_totals['Total Cost']
    total_qaly_diff = self.bariatric_totals['Total QALY'] - self.control_totals['Total QALY']

    icer = total_cost_diff / total_qaly_diff
    return icer


def write_totals_to_csv(self):
    icer = self.calculate_ICER()
    self.bariatric_totals = self.bariatric_totals.rename(columns={"Total Cost": "Bariatric Total Cost",
                                                                  "Total QALY": "Bariatric Total QALY",
                                                                  "Total Cost PPPY": "Bariatric Total Cost PPPY",
                                                                  "Total Life Years": "Bariatric Total Life Years"})

    concatenated_totals = pd.concat([self.bariatric_totals,
                                     self.control_totals,
                                     icer.to_frame(name='ICER')], axis=1)

    MarkovModel().write_to_csv(concatenated_totals)


if __name__ == '__main__':
    print('test')
