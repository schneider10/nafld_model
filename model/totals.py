from model.inputs import inputs


class Totals:
    """ We need to sum all values in the matrix above, at specified intervals.
        Split big matrix into chunks based on interval. Sum all values in chunk to get life years at interval.
    """

    def __init__(self, progression, cohort):
        self.disease_progression_matrix = progression(cohort).calculate_progression()
        self.total_cost = self.get_total_cost()
        self.total_QALY = self.get_total_QALY()
        self.total_life_years = self.get_total_life_years()

    def get_total_life_years(self):
        """ Calculate total life years by summing all of the progression values
        This is not necessary to calculate an icer.
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

    def get_total_cost_pppy(self):
        # This is not necessary to calculate an icer.
        return self.total_cost / self.total_life_years
