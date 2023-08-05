from os import linesep

class Writer:
  def __init__(self, stdout):
    self.stdout = stdout
  
  def write(self, text=''):
    self.stdout.write(str(text))
  
  def write_line(self, text=''):
    self.stdout.write(f'{str(text)}{linesep}')
  
  def write_lines(self, lines):
    for line in lines:
      self.stdout.write(f'{str(line)}{linesep}')
  
  def write_heading(self, text, level=1):
    if level not in range(1, 7):
      raise Exception('Invalid heading level. Levels can only be in the inclusive range [1..6]')
    self.stdout.write(f'h{level}.{str(text)}{linesep}')
  
  def write_hrule(self):
    self.stdout.write('----')