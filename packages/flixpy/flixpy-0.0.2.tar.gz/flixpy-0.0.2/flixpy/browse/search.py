import concurrent.futures

from flixpy.utils import get_json
from flixpy.models.movie import Movie
from flixpy.models.show import Show
from flixpy.browse.get import get_results


def search(query):
  '''Search for a particular query
  
  Arguments:
  - query: The query for the string (can be any string)

  Returns: List of Movies and Shows
  '''
  
  ENDPOINT = f'https://api.reelgood.com/v3.0/content/search/content?terms={query}'
  return get_results(ENDPOINT, key='items')


def title_matching(query):
  '''Search for only titles particular from a particular query'''

  ENDPOINT = f'https://api.reelgood.com/v3.0/content/search/typeahead?terms={query}'
  results = get_json(ENDPOINT)

  return results
