from urllib import request
import re

eune_url = "http://eune.op.gg/ranking/ajax2/ladders/start={}"
pattern = re.compile('<a href="/summoner/userName=.*?" class="Link">(.*?)</a>')

names_container = list()


def start():
  with open('eune_names.txt', 'w', encoding='utf-8') as f:
    for i in range(1, 1000000):
      names = []
      try:
        with request.urlopen(eune_url.format(i * 50)) as req:
          names = pattern.findall(req.read().decode('utf-8'))
          if len(names) == 0:
            break
      except Exception as e:
        print(e)
      f.write('{} => {}\n'.format(i, i * 50))
      f.writelines(map(lambda x: x + '\n', names))


if __name__ == '__main__':
  start()
