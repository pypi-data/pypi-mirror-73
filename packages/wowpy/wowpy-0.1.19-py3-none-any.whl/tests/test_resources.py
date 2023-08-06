import pytest
import json
import requests
from unittest import skipIf
from mock import patch, Mock
from wowpy.resources import validate_resource, create_resource
from wowpy.constants import SKIP_REAL

@pytest.fixture
def single_output_spec():
    with open('tests/fixtures/single_output_spec.json') as json_file:
        specification = json.load(json_file)
    return specification

def test_validate_resource(single_output_spec):
    valid = validate_resource(specification=single_output_spec)
    assert valid == True

@patch('wowpy.resources.Transcoder.associate_target_stream')
@patch('wowpy.resources.TargetStream.update_properties')
@patch('wowpy.resources.TargetStream.create_target')
@patch('wowpy.resources.Transcoder.create_transcoder_output') # returns an output id
@patch('wowpy.resources.Transcoder.update_transcoder')
@patch('wowpy.resources.Transcoder.get_transcoder_outputs')
@patch('wowpy.resources.LiveStream.create_live_stream')
def test_create_resource(mock_create_live,
                         mock_get_trans,
                         mock_update_trans, 
                         mock_create_output, 
                         mock_create_target, 
                         mock_update_target, 
                         mock_target_associate, 
                         single_output_spec):
    mock_create_live.return_value = {'id': 'abc123'}
    mock_get_trans.return_value = []
    mock_update_trans.return_value = 'some'
    mock_create_output.return_value = 'abc123'
    mock_create_target.return_value = 'abc-123'
    mock_update_trans.return_value = 'some'
    mock_target_associate.return_value = 'some'
    specification = create_resource(specification=single_output_spec)
    assert type(specification) is dict

###

@skipIf(SKIP_REAL, 'Skipping tests that hit the real API server.')
def test_real_create_resource(mocker, single_output_spec):
    specification = create_resource(specification=single_output_spec)
    assert type(specification) is dict