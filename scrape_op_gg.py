from urllib import request
import re
from urllib.error import HTTPError, URLError

eune_url = "http://eune.op.gg/ranking/ajax2/ladders/start={}"
pattern = re.compile('<a href="/summoner/userName=.*?" class="Link">(.*?)</a>')

names_container = list()


def start():
  with open('eune_names.txt', 'w', encoding='utf-8') as f:
    for i in range(1, 1000000):
      names = []
      f.write('{} => {}\n'.format(i, i * 50))
      try:
        with request.urlopen(eune_url.format(i * 50)) as req:
          names = pattern.findall(req.read().decode('utf-8'))
          if len(names) == 0:
            break
      except HTTPError as e:
        # do something
        print('HttpError: ', e)
      except URLError as e:
        # do something
        print('UrlError: ', e)
        break
      f.write(','.join(names) + '\n')


if __name__ == '__main__':
  start()
