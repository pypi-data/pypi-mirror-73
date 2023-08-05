from flixpy.models.provider_base import ProviderBase

class Episode(ProviderBase):
  def __init__(self, id_, season_no, episode_no, title, availability):
    self.id = id_
    self.season_no = season_no
    self.episode_no = episode_no
    self.title = title
    self._availability = availability

  def __repr__(self):
    return f'<Episode {self.season_no}:{self.episode_no}>'
