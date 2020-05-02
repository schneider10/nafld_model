from model.mortality import Mortality


def test_mortality_calculations(test_inputs):
    mortality_probability = Mortality().create_mortality_probability_dataframe()
    mortality_probability.to_csv('outputs/mortality_probability.csv')
    assert mortality_probability.to_numpy().sum() == 14.888955344