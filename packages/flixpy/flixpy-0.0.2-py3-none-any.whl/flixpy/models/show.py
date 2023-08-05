from flixpy.utils import get_json
from flixpy.models.base import Base
from flixpy.models.provider import Provider
from flixpy.models.season import Season
from flixpy.models.episode import Episode
from flixpy.enum.content_type import ContentType

import datetime


class Show(Base):
  """Show class

  Additional properties:
  - completed_on
  - seasons

  Additional methods:
  - __len__
    Shows the length of the show in seasons

  - __getitem__
    Allows for iterating through the seasons of the show:

    Example:
    for season in show:
      ...

  """

  def __init__(self, slug_or_id):
    super().__init__(slug_or_id, content_type=ContentType.SHOW)

    if self._json['completed_on'] is not None:
      self.completed_on = datetime.datetime.strptime(self._json['completed_on'], '%Y-%m-%dT%H:%M:%SZ')
    else:
      self.completed_on = None

  @property
  def seasons(self):
    seasons_list = []

    episodes_json = self._json['episodes']
    # episodes_json contains a dictionary of all episodes
    # episode_id: {...}

    for season_json in self._json['seasons']:

      episodes_list = []  # to be populated in the loop
      episode_id_list = season_json['episodes']

      for episodes_id in episode_id_list:

        # make the episode
        episode = Episode(
            id_=episodes_id,
            season_no=season_json['number'],
            episode_no=episodes_json[episodes_id]['number'],
            title=episodes_json[episodes_id]['title'],
            availability=episodes_json[episodes_id]['availability'],
        )
        episodes_list.append(episode)

      season = Season(
          show_slug=self.slug,
          season_id=season_json['id'],
          season_no=season_json['number'],
          episodes=episodes_list
      )
      seasons_list.append(season)

    # reelgood provides it in reverse order (season 1 last, so reverse it here)
    seasons_list.reverse()
    return seasons_list

  def __len__(self):
    """Get the length of the show in seasons

    Example:
      show = Show("...")
      no_seasons = len(seasons)
    """
    return len(self.seasons)

  def __getitem__(self, season_no):
    """Get a season

    Example:
      show = Show("...")
      seasons_one = show[0]

      for season in show:
        print(season)
    """
    return self.seasons[season_no]
