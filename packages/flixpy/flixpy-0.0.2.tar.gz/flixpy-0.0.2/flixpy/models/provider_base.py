from flixpy.models.provider import Provider
from flixpy.enum.streaming_provider import StreamingProvider


class ProviderBase:
  """Parent class for models which are on streaming providers

  Movies and Episodes are on streaming providers. 

  (Shows and Seasons are not. Shows holds Seasons which hold Episodes, which are on streaming providers)
  """

  @property
  def providers(self):
    # Get a list of streaming providers and the URL to the movie
    providers_list = []

    # pylint: disable=no-member
    for provider in self._availability:
      providers_list.append(
          Provider(
              provider['source_name'],
              provider['source_data']['web_link']
          )
      )
    return providers_list

  def is_on(self, streaming_provider: StreamingProvider):
    '''Returns true if the movie is on the streaming provider'''

    # pylint: disable=no-member
    for provider in self.providers:
      if streaming_provider == provider.streaming_provider:
        return True
    return False

  def link_for(self, streaming_provider: StreamingProvider):
    '''Get the link of the movie on the streaming_provider'''

    # pylint: disable=no-member
    for provider in self.providers:
      if provider.streaming_provider == streaming_provider:
        return provider.url
    return None
