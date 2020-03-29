import pandas as pd


class LoadIn:
    inputs = pd.read_excel('model_inputs.xlsx', sheet_name=None)


class ModelInputs:
    NAFLD_inputs = LoadIn.inputs['Cohort and NAFLD Prevalence'].set_index('Cohorts')

    other_disease_inputs = LoadIn.inputs['Other Disease State Prevalences'].set_index('Disease States')

    background_mortality = LoadIn.inputs['Age-specific Probabilities'].set_index('Age Cohorts')[
        'Background mortality annual probability']

    NAFLD_annual_probabilities = LoadIn.inputs['Age-specific Probabilities'].set_index('Age Cohorts')[
        'NAFLD annual probability']

    age_specific_rr = LoadIn.inputs['Age-specific Relative Risks'].set_index('Age Cohorts')

    transition_probabilities = LoadIn.inputs['Transition Probabilities'].set_index('Base Transition Matrix')

    mortality_risk = LoadIn.inputs['Disease-specific Mortality Risk'].set_index('Disease States')

    scoring_and_costing = LoadIn.inputs['Health Scoring and Costing'].set_index('Disease States').fillna(0)

    bariatric_substitutions = LoadIn.inputs['Treatment Effects'].set_index('Treatment Year')

    cohorts = NAFLD_inputs.index

    disease_states = scoring_and_costing.index
