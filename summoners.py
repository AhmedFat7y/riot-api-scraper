from cassiopeia import riotapi
from cassiopeia.type.core.summoner import Summoner
from cassiopeia.type.dto.summoner import Summoner as SummonerData
from cassiopeia.type.api.exception import APIError
from cassiopeia.type.api.store import DataStore
import os

base = ''
region = 'euw'
output_file = base + region + '_summoners.txt'
input_file = base + region + '_names.processed.txt'
api_key = os.environ['RIOT_API_KEY']


class MyDataStore(DataStore):
  def get(self, class_, keys, key_field):
    return [None for i in range(len(keys))]


riotapi.set_region(region.upper())
riotapi.set_api_key(api_key)
riotapi.set_data_store(MyDataStore())


def get_riot_summoners(names):
  summoners = []
  loop = True
  success = False
  while loop:
    loop = False
    try:
      summoners = riotapi.get_summoners_by_name(names)
      success = True
    except APIError as e:
      print('Got Exception:', e)
      if 499 < e.error_code < 600:  # recoverable error
        loop = True
    except Exception as e:  # unexpected exception
      print('Got Exception:', e)
  return success, [summoner for summoner in summoners if summoner]


def include_missing_summoners(names, summoners):
  # get missing names
  missing_names = set(names) - set([summoner.data.name for summoner in summoners])
  for missing_name in missing_names:
    summoners.append(Summoner(SummonerData({'name': missing_name, 'id': False})))
  return summoners


def get_json_summoners(names):
  success, summoners = get_riot_summoners(names)
  if len(summoners) != 40:
    summoners = include_missing_summoners(names, summoners)
  return summoners


def generate_summoners():
  with open(input_file, encoding='utf-8') as f:
    for line in f:
      line = line.strip()
      if line:
        names = line.split(',')
        for summoner in get_json_summoners(names):
          yield summoner.to_json(indent=None)


def start():
  with open(output_file, 'w', encoding='utf-8') as f:
    for summoner in generate_summoners():
      f.write(summoner)
      f.write('\n')


if __name__ == '__main__':
  start()
