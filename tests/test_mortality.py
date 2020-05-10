from model.mortality import Mortality


def test_mortality_calculations():
    mortality_probability = Mortality().create_mortality_probability_dataframe()
    mortality_probability.to_csv('outputs/mortality_probability.csv')
    assert mortality_probability.to_numpy().sum() == 14.88905
