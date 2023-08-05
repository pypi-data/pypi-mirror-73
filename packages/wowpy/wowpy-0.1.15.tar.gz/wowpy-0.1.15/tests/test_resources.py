import pytest
import json
from wowpy.resources import validate_resource

@pytest.fixture
def single_output_spec():
    with open('tests/fixtures/single_output_spec.json') as json_file:
        specification = json.load(json_file)
    return specification

def test_validate_resource(mocker, single_output_spec):
    valid = validate_resource(specification=single_output_spec)
    assert valid == True
    