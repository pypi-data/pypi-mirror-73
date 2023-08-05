from os import linesep

item_types = {
  'simple': '-',
  'bulleted': '*',
  'numbered': '#'
}

class ListItem:
  def __init__(self, text, item_type, depth=0):
    self.text = text
    self.item_type = item_type
    self.depth = depth
  
  def __str__(self):
    prefix = "".join([item_types[self.item_type] for _ in range(self.depth + 1)])
    return f'{prefix} {self.text}'

class List:
  def __init__(self, list_type='simple'):
    if list_type not in item_types:
      raise Exception(f'Invalid list type. The supported list types are [{",".join([list_type for list_type in item_types])}]')
  
    self.list_type = list_type
    self.items = []
  
  def append(self, item, item_type=None, depth=0):
    if depth < 0:
      raise Exception('List item depth cannot be negative')

    if not item_type:
      item_type = self.list_type
  
    self.items.append(ListItem(item, item_type, depth))
  
  def __str__(self):
    if not self.items:
      return ''
    
    return '\n'.join([str(item) for item in self.items])
