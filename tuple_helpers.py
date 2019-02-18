def t_mul(t, s):
  return tuple(x * s for x in t)

def t_add(a, b):
  return tuple(x + y for (x, y) in zip(a, b))

def t_int(t):
  return tuple(int(x) for x in t) 
