SERVER_ADDRESS = '/tmp/ledcolor_socket'

AUDIO_CHANNELS = [0]
AUDIO_RATE = 48000
DEFAULT_OUTPUT_TIME = 0.05

DEFAULT_LOW_COLOR = '#00ff00'
DEFAULT_HIGH_COLOR = '#ff0000'

VOLUME_LIMIT_FALL_TIME = 2
VOLUME_LOW_LIMIT = 0.001
VOLUME_MAX_LIMIT = 1.0
VOLUME_SAMPLE_TIME = 2

AUDIBLE_LOW_FREQ = 20
AUDIBLE_HIGH_FREQ = 20000

AUDIBLE_RANGES_HIGH_FREQ = [
    60,  # sub-bass
    250,  # bass
    500,  # low midrange
    2000,  # midrange
    4000,  # upper midrange
    6000,  # presence
]
