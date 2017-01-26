import json
from cassiopeia import riotapi

base = ''
riotapi.set_region('EUNE')
riotapi.set_api_key('RGAPI-2eef322c-76f7-4ac4-952f-9f4b1b8b94ba')


def generate_summoners():
  with open(base + 'eune_names.processed.txt', encoding='utf-8') as f:
    for line in f:
      line = line.strip()
      if line:
        names = line.split(',')
        summoners = riotapi.get_summoners_by_name(names)
        for summoner in summoners:
          if summoner:
            yield json.loads(summoner.data.to_json(), encoding='utf-8')


with open(base + 'summoners-data.txt', 'a', encoding='utf-8') as f:
  for summoner in generate_summoners():
    json.dump(summoner, f, ensure_ascii=False)
    f.write('\n')
