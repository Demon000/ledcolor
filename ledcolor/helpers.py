from rivalcfg.helpers import is_color, color_string_to_rgb

from color import Color, AnimatedColor

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
