from totals import OutputTotals
from disease_progression import BariatricDiseaseProgression, OCADiseaseProgression

from inputs import ModelInputs


class FinalCalculations:
    def __init__(self, progression, cohort):
        self.disease_progression_matrix = progression(cohort).calculate_progression()
        if progression == BariatricDiseaseProgression:
            self.substitutions = ModelInputs.bariatric_substitutions
        elif progression == OCADiseaseProgression:
            self.substitutions = ModelInputs.oca_substitutions

    def get_patients_treated(self):
        return self.disease_progression_matrix.iloc[0]['F2'] + self.disease_progression_matrix.iloc[0]['F3']

    def get_treatment_costs(self):
        cost_PPPY = self.substitutions['Treatment cost ($) PPPY']
        F2_costs = cost_PPPY.values * self.disease_progression_matrix.iloc[0:5]['F2'].values
        F3_costs = cost_PPPY.values * self.disease_progression_matrix.iloc[0:5]['F3'].values
        return sum(F2_costs) + sum(F3_costs)

    def get_control_qaly(self):
        pass

    def get_qaly_gained(self):
        pass

    def get_qaly_gained_per_patient_treated(self):
        pass

    def get_treatment_costs_per_patient_treated(self):
        pass

    def get_control_costs(self):
        pass

    def get_net_cost(self):
        pass

    def get_net_cost_per_patient_treated(self):
        pass

    def get_icer(self):
        # control_totals = OutputTotals().get_control_totals_df()

        # # Get totals per the treatment method of disease progression. This is measured against the control
        # self.treatment_totals = OutputTotals().output_totals_df(disease_progression)

        # Total Cost - Control Costs
        #     total_cost_diff = self.bariatric_totals['Total Cost'] - self.control_totals['Total Cost']
        #     # Year 1-60 Cost - Control QALY
        #     total_qaly_diff = self.bariatric_totals['Total QALY'] - self.control_totals['Total QALY']
        #
        #     # (Total Cost - Control Costs) / (Year 1-60 cost - Control QALY)
        #     icer = total_cost_diff / total_qaly_diff
        #     return icer
        #
        pass


# def calculate_ICER(self):

#
# def write_totals_to_csv(self):
#     icer = self.calculate_ICER()
#     self.bariatric_totals = self.bariatric_totals.rename(columns={"Total Cost": "Bariatric Total Cost",
#                                                                   "Total QALY": "Bariatric Total QALY",
#                                                                   "Total Cost PPPY": "Bariatric Total Cost PPPY",
#                                                                   "Total Life Years": "Bariatric Total Life Years"})
#
#     concatenated_totals = pd.concat([self.bariatric_totals,
#                                      self.control_totals,
#                                      icer.to_frame(name='ICER')], axis=1)
#
#     MarkovModel().write_to_csv(concatenated_totals)


if __name__ == '__main__':
    treatments = [BariatricDiseaseProgression, OCADiseaseProgression]

    for treatment in treatments:
        for age_cohort in ModelInputs.cohorts:
            FinalCalculations(treatment, age_cohort).get_treatment_costs()
