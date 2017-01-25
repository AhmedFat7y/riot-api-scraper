from urllib import request
import re

eune_url = "http://eune.op.gg/ranking/ajax2/ladders/start={}"
pattern = re.compile('<a href="/summoner/userName=.*?" class="Link">(.*?)</a>')


def start():
  with open('eune_names.txt', 'w', encoding='utf-8') as f:
    for i in range(1, 1000000):
      f.write('{} => {}'.format(i, i * 50))
      f.write('\n')
      with request.urlopen(eune_url.format(i * 50)) as req:
        names = pattern.findall(req.read().decode('utf-8'))
        if len(names) == 0:
          break
        f.write('\n'.join(names))
        f.write('\n')


if __name__ == '__main__':
  start()
