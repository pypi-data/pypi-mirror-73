from wowpy.livestreams import LiveStream
from wowpy.transcoders import Transcoder
from wowpy.targets import TargetStream
from wowpy.utils import validate_schema
from wowpy import schemas

def create_resource(specification):

  # Get data from specification
  version = specification['version']
  resource_name = specification['name']
  
  resource_keys = list(specification.keys())

  for resource_key in resource_keys:

    item = specification[resource_key]

    if type(item) is not dict:
      continue

    resource_type = item.get('type', None)
    if resource_type in [None, 'custom_target', 'output']:
      continue

    if resource_type == 'live_stream':
      live_stream_data = {'live_stream': specification[resource_key]['parameters']}
      live_stream_data['live_stream']['name'] = resource_name
      live_stream = LiveStream.create_live_stream(data=live_stream_data)
      live_stream_id = live_stream['id']
      outputs = Transcoder.get_transcoder_outputs(transcoder_id=live_stream_id)
      specification[resource_key]['id'] = live_stream_id

      # Delete default output
      for output in outputs:
        output_id = output['id']
        Transcoder.delete_transcoder_output(transcoder_id=live_stream_id, output_id=output_id)
        target_id = output['output_stream_targets'][0]['stream_target']['id']
        TargetStream.delete_target(stream_type='fastly', stream_target_id=target_id)

    if resource_type == 'transcoder':
      transcoder_data = {'transcoder': specification[resource_key]['parameters']} 
      Transcoder.update_transcoder(transcoder_id=live_stream_id, data=transcoder_data)
      specification[resource_key]['id'] = live_stream_id

      output_keys = specification[resource_key]['outputs']
      for output_key in output_keys:
        output_data = {'output': specification[output_key]['parameters']}
        output_id = Transcoder.create_transcoder_output(transcoder_id=live_stream_id, data=output_data)
        specification[output_key]['id'] = output_id

        target_keys = specification[output_key]['targets']
        for target_key in target_keys:
          target_data = {'stream_target_custom': specification[target_key]['parameters']}
          target_provider = specification[target_key]['parameters']['provider'].split('_')
          target_provider_upper = target_provider[0].upper()
          target_name = '_'.join([resource_name, target_provider_upper])
          target_data['stream_target_custom']['name'] = target_name
          target_id = TargetStream.create_target(data=target_data)
          target_properties = specification[target_key]['properties']

          TargetStream.update_properties(stream_target_id=target_id, properties_data=target_properties)
          Transcoder.associate_target_stream(transcoder_id=live_stream_id, output_id=output_id, stream_target_id=target_id)
          specification[target_key]['id'] = target_id

  return specification
    
# TODO: Validate lists in resource blocks

def delete_resource():
  pass

def validate_resource(specification):
  block_keys = specification.keys()
  for block_key in block_keys:
    if block_key in ['version', 'prefix', 'name']:
      continue
    data_block = specification[block_key]
    schema_name = data_block['type']+'_'+'schema'
    schema_uppercase = schema_name.upper().replace(' ','_') # upper replaces underscore with space
    schema_model = getattr(schemas, schema_uppercase)
    response = validate_schema(schema=schema_model, data=data_block)
    if not response['valid']:
      return False
  return True

def get_resource_info(id):
  resource_info = {
    'livestream': {},
    'transcoder': {},
    'targets': [],
    'schedule': {}
  }

  live_stream_info = LiveStream.get_live_stream(id)
  resource_info['livestream'] = live_stream_info
  transcoder_info = Transcoder.get_transcoder(id)
  resource_info['transcoder'] = transcoder_info
  transcoder_outputs = transcoder_info['outputs']
  for output_item in transcoder_outputs:
    stream_targets = output_item['output_stream_targets']
    for target_item in stream_targets:
      stream_target_id = target_item['stream_target']['id']
      stream_target_type = target_item['stream_target']['type']
      stream_target_info = TargetStream.get_target(stream_type=stream_target_type, stream_target_id=stream_target_id)
      stream_target_properties = TargetStream.get_target_properties(stream_type=stream_target_type, stream_target_id=stream_target_id)
      resource_info['targets'].append({'config': stream_target_info, 'properties': stream_target_properties})

#   schedule_info = Schedule.get_schedule(scheduler_id=scheduler_id)
#   resource_info['schedule'] = schedule_info

  return resource_info