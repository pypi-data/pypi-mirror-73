from flixpy.enum.streaming_provider import StreamingProvider

class Provider:
  def __init__(self, source_name: str, url):
    self.streaming_provider = StreamingProvider(source_name)
    self.url = url

  def __repr__(self):
    return f'<Provider {self.streaming_provider}>'
