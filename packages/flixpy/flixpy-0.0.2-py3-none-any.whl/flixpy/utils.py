
import requests


def get_json(uri):
  request = requests.get(uri)
  if request.status_code == 200:
    return request.json()
  else:
    # could also be because network is bad?
    return None


