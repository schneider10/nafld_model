from totals import Totals
from disease_progression import DiseaseProgression


class FinalCalculations(Totals):
    def __init__(self, progression, cohort):
        super().__init__(progression, cohort)
        self.controls = Totals(DiseaseProgression, cohort)
        self.substitutions = progression.substitutions
        self.patients_treated = self.get_patients_treated()
        self.control_qaly = self.controls.get_total_QALY()
        self.control_costs = self.controls.get_total_cost()

    def get_patients_treated(self):
        return self.disease_progression_matrix.iloc[0]['F2'] + self.disease_progression_matrix.iloc[0]['F3']

    def get_treatment_costs(self):
        cost_pppy = self.substitutions['Treatment cost ($) PPPY']
        F2_costs = cost_pppy.values * self.disease_progression_matrix.iloc[0:5]['F2'].values
        F3_costs = cost_pppy.values * self.disease_progression_matrix.iloc[0:5]['F3'].values
        return sum(F2_costs) + sum(F3_costs)

    def get_qaly_gained(self):
        return self.get_total_QALY() - self.control_qaly

    def get_qaly_gained_per_patient_treated(self):
        return self.get_qaly_gained() / self.patients_treated

    def get_treatment_costs_per_patient_treated(self):
        return self.get_treatment_costs() / self.patients_treated

    def get_net_savings(self):
        return self.control_costs - self.get_total_cost()

    def get_net_savings_per_patient_treated(self):
        return self.get_net_savings() / self.patients_treated

    def get_icer(self):
        return - self.get_net_savings() / self.get_qaly_gained()
