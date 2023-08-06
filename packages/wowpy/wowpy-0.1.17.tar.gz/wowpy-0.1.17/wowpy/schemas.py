from voluptuous import Schema, Required, All, Length, Range, Any, Optional

RESOURCE_SCHEMA = Schema({
    Required('version'): All(str, Length(min=0)),
    Required('name'): All(str, Length(min=0)),
})

# TODO: Move all values to template, only left required ones

LIVE_STREAM_SCHEMA = Schema({
    Required('type'): 'live_stream',
    Required('id'): All(str, Length(min=0)),
    Required('parameters'): { # key is live_stream
        Required('aspect_ratio_height'): All(int, Range(min=0)),
        Required('aspect_ratio_width'): All(int, Range(min=0)),
        Required('billing_mode'): All(str, Length(min=0)),
        Required('broadcast_location'): All(str, Length(min=0)),
        Required('encoder'): All(str, Length(min=0)),
        Required('name', default=''): All(str, Length(min=0)),
        Required('transcoder_type'): All(str, Length(min=0)),
        Required('delivery_method'): Any('pull','push'),
        ##
        Required('delivery_protocols', default=['rtmp','hls']): [All(str, Length(min=0)),All(str, Length(min=0))], # might be more
        Required('delivery_type', default='single-bitrate'): All(str, Length(min=0)),
        Required('disable_authentication', default=True): All(bool), # push
        Required('low_latency', default=False): All(bool),
        Required('recording', default=True): All(bool),
        Required('target_delivery_protocol', default='hls-https'): All(str, Length(min=0)),
        Required('use_stream_source', default=False): All(bool),
        Required('source_url', default='rtmp://'): All(str, Length(min=0)),  # pull
    }
})

TRANSCODER_SCHEMA = Schema({
    Required('type'): 'transcoder', 
    Required('id'): All(str, Length(min=0)),
    Required('outputs'): All(
        [
            All(str, Length(min=0))
        ]
    ),
    Required('parameters'): { # key is empty
        Required('idle_timeout', default=0): All(int, Range(min=0))
    }
})

OUTPUT_SCHEMA = Schema({
    Required('type'): 'output',
    Required('id'): All(str, Length(min=0)),
    Required('targets'): All(
        [
            All(str, Length(min=0))
        ]
    ),
    Required('parameters'): {  # key is output
        Required('stream_format'): All(str, Length(min=0)),
        Required('h264_profile'): All(str, Length(min=0)),
        Required('aspect_ratio_width'): All(int, Range(min=0)),
        Required('aspect_ratio_height'): All(int, Range(min=0)),
        Required('bitrate_video'): All(int, Range(min=0)),
        Required('bitrate_audio'): All(int, Range(min=0)),
        ###
        Required('framerate_reduction', default='0'): All(str, Length(min=0)),
        Required('keyframes', default='follow_source'): All(str, Length(min=0)),
        Required('passthrough_audio', default=True): All(bool),
        Required('passthrough_video', default=True): All(bool)
    }
})

CUSTOM_TARGET_SCHEMA = Schema({
    Required('type'): 'custom_target',
    Required('id'): All(str, Length(min=0)),
    Required('parameters'): {  # key is stream_target_custom
        Required('provider'): Any('akamai_cupertino', 'rtmp', 'akamai_rtmp'),
        Required('use_https', default=True): All(bool),
        Required('primary_url', default=''): All(str, Length(min=0)),
        Required('stream_name', default=''): All(str, Length(min=0))
    },
    Required('properties'):
        All(
            [
                {
                    Required('property'): {
                        Required('key'): All(str, Length(min=0)),
                        Required('section'): All(str, Length(min=0)),
                        Required('value'): All(int, Range(min=0))
                    }
                }
            ]
        )
})
