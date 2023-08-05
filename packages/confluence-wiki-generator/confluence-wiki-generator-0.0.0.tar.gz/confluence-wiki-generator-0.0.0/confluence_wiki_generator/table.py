import itertools

class Table:
  def __init__(self, columns, vertical=False):
    self.vertical = vertical
    self.columns = columns
    self.rows = []

  def append(self, row):
    self.rows.append(row)

  def __str__(self):
    lines = []

    if self.vertical:
      rotated_table = itertools.zip_longest(*self.rows[::])
      for (column, vertical_row) in itertools.zip_longest(self.columns, rotated_table):
        lines.append(f'||{column}|{"|".join([item if item else " " for item in vertical_row])}|')
    else:
      lines.append(f'||{"||".join([column for column in self.columns])}||')
      for row in self.rows:
        lines.append(f'|{"|".join([item for item in row])}|')
    return '\n'.join(lines)
