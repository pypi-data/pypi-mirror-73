from flixpy.utils import get_json
from flixpy.models.movie import Movie
from flixpy.models.show import Show

import concurrent.futures


def get_movie_or_show(slug, content_type):
  ''' Returns the full Movie/Show based on a list of slugs and a list of their content types (either 'm' or 's') '''
  # shared logic, so no need to copy paste code
  if content_type == 'm':
    return Movie(slug)
  return Show(slug)


def get_results(endpoint, key='results'):
  ''' Returns the results of an endpoint

  Used to get the results of a search or browse
  
  By default, the results are the value of the key 'results' in the JSON output. This key can be overriden with the `key` parameter
  '''
  
  json = get_json(endpoint)

  # the default key for the results of the query/search/browse is results
  # but it's "items" for searching
  results = json[key]

  # need to know if movie or show
  slug_list = [mov['slug'] for mov in results]
  content_type_list = [mov['content_type'] for mov in results]

  with concurrent.futures.ThreadPoolExecutor(max_workers=30) as exe:
    movies_list = exe.map(get_movie_or_show, slug_list, content_type_list)
    return list(movies_list)
