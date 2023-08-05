from wowpy.livestreams import LiveStream
from wowpy.transcoders import Transcoder
from wowpy.targets import TargetStream
from wowpy.utils import validate_schema
from wowpy import schemas

# def create_resource(specification):

#   # Get data from specification
#   betgenius_id = specification['betgenius']
#   source_id = specification['source_id']
#   external_id = specification['external_id']
#   camera_id = specification['camera_id']
#   start_time = specification['event_info']['start_time']
#   event_name = specification['event_info']['name']
#   context = specification['event_info']['context']
#   gs_outputs = specification['gs_outputs']
#   delivery_method = specification['gs_input']['type']
#   livestream_data = {'live_stream': specification['gs_input']['config']['live_stream']}
#   transcoder_data = {'transcoder': specification['gs_input']['config']['transcoder']}
#   schedule_data = {'schedule': specification['schedule_params']['schedule']}
#   time_before = specification['schedule_params']['time_before']
#   time_after = specification['schedule_params']['time_after']

#   # Create wowza livestream 
#   livestream_name = BATON_PREFIX + SEPARATOR + str(betgenius_id)
#   livestream_data['live_stream']['name'] = livestream_name
#   stream = Livestream.create_livestream(data=livestream_data)
#   live_stream_id = stream['id']
#   outputs = Transcoder.get_transcoder_outputs(transcoder_id=live_stream_id)
#   Transcoder.update_transcoder(transcoder_id=live_stream_id, data=transcoder_data)

#   # Delete default output
#   output_id = outputs[0]['id']
#   Transcoder.delete_transcoder_output(transcoder_id=live_stream_id, output_id=output_id)
#   # Delete default target
#   target_id = outputs[0]['output_stream_targets'][0]['stream_target']['id']
#   TargetStream.delete_target(stream_type=WSC_TARGET_NAME, stream_target_id=target_id)

#   # Create outputs and associated targets 
#   for gs_output in gs_outputs:    
#     output_id = Transcoder.create_transcoder_output(transcoder_id=live_stream_id, data=gs_output['config'])
#     for target in gs_output['targets']:
#       target_data = {'stream_target_custom': target['config']['stream_target_custom']}
#       primary_url = target['primary_url'].format(betgenius_id=betgenius_id)
#       stream_name = target['stream_name'].format(betgenius_id=betgenius_id)
#       target_properties = target['properties']
#       target_conf = target['type'].split('_')
#       stream_protocol = target_conf[0].upper()
#       # target_name = SEPARATOR.join([BATON_PREFIX, betgenius_id, source_id, external_id, str(camera_id), stream_protocol])
#       target_name = SEPARATOR.join([BATON_PREFIX, betgenius_id, stream_protocol])
#       target_data['stream_target_custom']['name'] = target_name
#       target_data['stream_target_custom']['primary_url'] = primary_url
#       target_data['stream_target_custom']['stream_name'] = stream_name
#       stream_target_id = TargetStream.create_target(data=target_data)
#       TargetStream.update_properties(stream_target_id=stream_target_id, properties_data=target_properties)
#       Transcoder.associate_target_stream(transcoder_id=live_stream_id, output_id=output_id, stream_target_id=stream_target_id)

#   resource_id = ''
#   return resource_id

# TODO: Validate lists in resource blocks

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
    'input': {
      'livestream': {}
    },
    'output': {
      'transcoder': {},
      'targets': []
    },
    'schedule': {}
  }

  live_stream_info = LiveStream.get_live_stream(id)
  resource_info['input']['livestream'] = live_stream_info
  transcoder_info = Transcoder.get_transcoder(id)
  resource_info['output']['transcoder'] = transcoder_info
  transcoder_outputs = transcoder_info['outputs']
  for output_item in transcoder_outputs:
    stream_targets = output_item['output_stream_targets']
    for target_item in stream_targets:
      stream_target_id = target_item['stream_target']['id']
      stream_target_type = target_item['stream_target']['type']
      stream_target_info = TargetStream.get_target(stream_type=stream_target_type, stream_target_id=stream_target_id)
      stream_target_properties = TargetStream.get_target_properties(stream_type=stream_target_type, stream_target_id=stream_target_id)
      resource_info['output']['targets'].append({'config': stream_target_info, 'properties': stream_target_properties})

#   schedule_info = Schedule.get_schedule(scheduler_id=scheduler_id)
#   resource_info['schedule'] = schedule_info

  return resource_info