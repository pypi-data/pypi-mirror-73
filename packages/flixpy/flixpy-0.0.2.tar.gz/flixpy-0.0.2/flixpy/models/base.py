from flixpy.utils import get_json
from flixpy.enum.content_type import ContentType
from flixpy.enum.genre import Genre
from flixpy.enum.tag import Tag

import datetime


class Base:
  """The class from which Move and Show inherit from

  Properties:
  - content_type
  - _json
  - id
  - slug
  - title
  - overview
  - released_on
  - trailer
  - genres
  - tags

  """

  def __init__(self, slug_or_id, content_type: ContentType):
    self.content_type = content_type
    ENDPOINT = f'http://api.reelgood.com/v3.0/content/{self.content_type.value}/{slug_or_id}'

    if self.content_type not in [ContentType.SHOW, ContentType.MOVIE]:
      raise Exception(f'Invalid content_type {content_type}')

    self._json = get_json(ENDPOINT)
    if self._json == None:
      raise Exception(f'{self.content_type} with slug or ID "{slug_or_id}" does not exist')

    self.id = self._json['id']
    self.slug = self._json['slug']
    self.title = self._json['title']
    self.overview = self._json['overview']

    if self._json['released_on'] is not None:
      self.released_on = datetime.datetime.strptime(self._json['released_on'], '%Y-%m-%dT%H:%M:%SZ')
    else:
      self.released_on = None

  def __repr__(self):
    return f'<{self.content_type.value.capitalize()} {self.slug}>'

  @property
  def trailer(self):
    # Get the first trailer of the mobue, giving bias towards YouTube
    for trailer in self._json['trailers']:
      if trailer['site'] == 'youtube':
        return f'https://youtube.com/watch?v={trailer["key"]}'

  @property
  def genres(self):
    genre_list = []
    for genre_id in self._json['genres']:
      try:
        # if the genre (or tag) doesn't exist in the enum class, just ignore
        genre_list.append(Genre(genre_id))
      except:
        pass
    return genre_list

  @property
  def tags(self):
    tags_list = []
    for tag_json in self._json['tags']:
      tag_slug = tag_json['slug']
      try:
        tags_list.append(Tag(tag_slug))
      except:
        pass
    return tags_list
  
  # cannot make class immutable? TODO
  # def __setattr__(self, name, value):
  #   print(name, value)
