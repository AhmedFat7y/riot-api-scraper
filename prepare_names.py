import re

base = ''
filename = base + 'eune_names.txt'
filename2 = base + 'eune_names.processed.txt'
pattern = re.compile('\d+ => \d+')

c = 0
lines = list()
counterFound = False
empty = list()

with open(filename2, 'w', encoding='utf-8') as f2:
  with open(filename, encoding='utf-8') as f:
    for line in f:
      line = line.strip()
      if pattern.fullmatch(line) or line == '':
        if counterFound and line != '':
          empty.append(line)
        else:
          counterFound = True
      else:
        c += 1
        lines.append(line)
        counterFound = False
      if c == 40:
        f2.write(','.join(lines) + '\n')
        lines = list()
        c = 0
    if len(lines) != 0:
      f2.write(','.join(lines) + '\n')
  f2.write('Empty:\n')
  f2.writelines(map(lambda x: x + '\n', empty))
