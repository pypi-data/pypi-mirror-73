
class Season:
  """Information on each season of the show
  
  Methods:
  - __len__
    Shows the length of the season in episodes

  - __getitem__
    Allows for iterating through the episodes of the shows

    Example:
    for episode on season:
      ...
  
  """
  
  def __init__(self, show_slug, season_id, season_no, episodes):
    self.show_slug = show_slug
    self.season_id = season_id
    self.season_no = season_no
    self.episodes = episodes

  def __repr__(self):
    return f'<Season {self.show_slug}: {self.season_no}>'

  def __len__(self):
    """Get the length of the show in episodes

    Example:
      show = Show("...")
      season_one = show[0]

      no_episodes = season_one[0]
    """
    return len(self.episodes)

  def __getitem__(self, episode_no):
    """Get a specific episode

    Example:
      show = Show("...")
      seasons_one = show[0]

      for episode in season_one:
        print(episode)
    """
    return self.episodes[episode_no]
