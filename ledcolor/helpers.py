from rivalcfg.helpers import is_color, color_string_to_rgb

from color import Color, AnimatedColor

MORSE_CODE_DICT = {
  ' ': '/',
  'a': '.-',
  'b': '-...',
  'c': '-.-.',
  'd': '-..',
  'e': '.',
  'f': '..-.',
  'g': '--.',
  'h': '....',
  'i': '..',
  'j': '.---',
  'k': '-.-',
  'l': '.-..',
  'm': '--',
  'n': '-.',
  'o': '---',
  'p': '.--.',
  'q': '--.-',
  'r': '.-.',
  's': '...',
  't': '-',
  'u': '..-',
  'v': '...-',
  'w': '.--',
  'x': '-..-',
  'y': '-.--',
  'z': '--..',
}

def get_light_color(on_duration):
  return AnimatedColor(on_duration, 0, (255, 255, 255))

def get_dark_color(on_duration):
  return AnimatedColor(on_duration, 0, (0, 0, 0))

def get_morse_char_colors(on_duration):
  return {
    '.': get_light_color(on_duration),
    '-': get_light_color(on_duration * 3),
    ' ': get_dark_color(on_duration * 3),
    '/': get_dark_color(on_duration * 7),
  }

def text_to_morse(s):
  text = s.lower()

  morse = []
  for char in text:
    if char not in MORSE_CODE_DICT:
      raise Exception('`{}` is not a valid char.'.format(char))

    morse_char = MORSE_CODE_DICT[char]
    morse.append(morse_char)

  return ' '.join(morse)

def morse_to_colors(morse, on_duration):
  morse_light_dict = get_morse_char_colors(on_duration)
  start = get_dark_color(on_duration * 8)
  separator = get_dark_color(on_duration)

  colors = []
  colors.append(start)
  for char in morse:
    char_colors = morse_light_dict[char]
    colors.append(char_colors)
    colors.append(separator)

  return colors

def duration_from_string(duration_string):
  try:
    duration = float(duration_string)
  except ValueError:
    raise Exception('`{}` is not a valid duration.'.format(duration_string))

  return duration

def rgb_from_string(color_string):
  if not is_color(color_string):
    raise Exception('`{}` is not a valid color.'.format(color_string))

  return color_string_to_rgb(color_string)

def color_from_string(color_string):
  rgb = rgb_from_string(color_string)
  return Color(rgb)

def args_to_colors(args):
  colors = []
  for arg in args:
    color_string, on_duration_string, fade_duration_string = arg.split(':')

    rgb = rgb_from_string(color_string)
    on_duration = duration_from_string(on_duration_string)
    fade_duration = duration_from_string(fade_duration_string)

    color = AnimatedColor(on_duration, fade_duration, rgb)
    colors.append(color)

  if not len(colors):
    raise Exception('No colors have been supplied.')

  return colors
