import pytest
from inputs import ModelInputs


@pytest.fixture
def test_inputs():
    yield ModelInputs(input_file='test_model_inputs.xlsx')

