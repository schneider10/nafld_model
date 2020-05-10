from model.state_prevalence import StatePrevalence


def test_state_prevalence():
    state_prevalence = StatePrevalence().disease_prevalence_per_age_cohort
    state_prevalence.to_csv('outputs/state_prevalence.csv')
    assert state_prevalence.to_numpy().sum() == 124435.96999471086
