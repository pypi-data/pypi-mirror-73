def wrap(text, wrap_sequence):
  return f'{wrap_sequence}{text}{wrap_sequence}' if text else ''

def emphasis(text):
  return wrap(text, '_')

def strong(text):
  return wrap(text, '*')

def citation(text):
  return wrap(text, '??')

def strikethrough(text):
  return wrap(text, '-')

def underline(text):
  return wrap(text, '+')

def superscript(text):
  return wrap(text, '^')

def subscript(text):
  return wrap(text, '~')

def monospace(text):
  return '{{' + text + '}}' if text else ''

def block_quote(text):
  return f'bq. {text}' if text else ''

def colour(text, colour):
  return f'{{color:{colour}}}{text}{{color}}' if text and colour else ''