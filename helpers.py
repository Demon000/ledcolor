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

def LIGHT(update_time):
  return [(update_time, (255, 255, 255))]

def DARK(update_time):
  return [(update_time, (0, 0, 0))]

def MORSE_LIGHT_DICT(light, dark):
  return {
    '.': light,
    '-': light * 3,
    ' ': dark * 3,
    '/': dark * 7,
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

def morse_to_config(morse, update_time):
  light = LIGHT(update_time)
  dark = DARK(update_time)
  morse_light_dict = MORSE_LIGHT_DICT(light, dark)

  config = []
  config.extend(dark * 8)
  for char in morse:
    colors = morse_light_dict[char]
    config.extend(colors)
    config.extend(dark)


  return config

def args_to_config(args):
  config = []
  for arg in args:
    duration_string, color_string = arg.split(':')

    try:
      duration = float(duration_string)
    except ValueError:
      raise Exception('`{}` is not a valid duration.'.format(duration_string))

    if not is_color(color_string):
      raise Exception('`{}` is not a valid color.'.format(color_string))

    color = color_string_to_rgb(color_string)
    config.append((duration, color)) 

  return config
