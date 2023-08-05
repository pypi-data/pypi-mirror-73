from enum import Enum, unique
from flixpy.utils import get_json
from flixpy.browse.get import get_results

from flixpy.enum.content_type import ContentType
from flixpy.enum.genre import Genre
from flixpy.enum.tag import Tag
from flixpy.enum.streaming_provider import StreamingProvider


@unique
class By(Enum):
  STREAMING_PROVIDER = 'source'
  GENRE = 'genre'
  TAG = 'tag'


@unique
class Sort(Enum):
  IMDB_RATING = 2
  RELEASE_DATE = 3
  ALPHABETICALLY = 4


def browse(by: By, skip: int = 0, streaming_provider: StreamingProvider = None, genre: Genre = None, tag: Tag = None, content_kind: ContentType = None, sort: Sort = None):
  """Get a list of movies based on the parameters

  Parameters:
  - by: The main option to get movies, can be by streaming provider, genre, or tag
  - skip: The number of positions to skip in the list. This is useful for pagination
  - streaming_provider: The streaming provider to limit the results to
  - genre: The genre to limit the results to
  - tag: The tag to limit the results to
  - content_kind: Whether the function should return movies or shows (or both)
  - sort: Choose the method to sort by (see Sort enum class)

  Examples:
  - browse(By.STREAMING_PROVIDER, streaming_provider=StreamingProvider.NETFLIX, content_kind=ContentType.SHOW)
    Find all NETFLIX SHOWS

  - browse(By.GENRE, genre=Genre.ANIMATION, content_kind=ContentType.MOVIE, streaming_provider=StreamingProvider.NETFLIX)
    Find all MOVIES of genre ANIMATION on NETFLIX

  - browse(By.TAG, tag=Tag.WAR, content_kind=ContentType.MOVIE, streaming_provider=StreamingProvider.NETFLIX)
    Find all MOVIES of tag WAR on NETFLIX
  """

  # filter by STREAMING_PROVIDER
  if by == By.STREAMING_PROVIDER:
    if streaming_provider is None:
      raise Exception('No streaming_provider provided')
    ENDPOINT = f'https://api.reelgood.com/v3.0/content/browse/source/{streaming_provider.value}?'

  # filter by GENRE
  elif by == By.GENRE:
    if genre is None:
      raise Exception('No genre provided')
    ENDPOINT = f'https://api.reelgood.com/v3.0/content/browse/genre/{genre.value}?'

    # if tag is provided, limit by tag too
    if tag is not None:
      ENDPOINT += f'&tag={tag.value}'

  # filter by TAG
  elif by == By.TAG:
    if tag is None:
      raise Exception('No tag provided')
    ENDPOINT = f'https://api.reelgood.com/v3.0/content/browse/tag/{tag.value}?'

    # if genre is provided, limit by genre too
    if genre is not None:
      ENDPOINT += f'&genre={genre.value}'

  # Add the skip value
  ENDPOINT += f'&skip={skip}'

  # content_kind is optional
  if content_kind is not None:
    ENDPOINT += f'&content_kind={content_kind.value}'

  if (by == By.GENRE or by == By.TAG):
    if streaming_provider:
      # search from the specific source
      ENDPOINT += f'&override_user_sources=true&overriding_sources={streaming_provider.value}'
    else:
      # if it's by genre or tag but streaming_provider is not provided, search from all sources
      ENDPOINT += '&availability=onAnySource'
  
  # sorting by is also optional
  if sort is not None:
    ENDPOINT += f'&sort={sort.value}'

  # for debug
  # return ENDPOINT

  return get_results(ENDPOINT)
