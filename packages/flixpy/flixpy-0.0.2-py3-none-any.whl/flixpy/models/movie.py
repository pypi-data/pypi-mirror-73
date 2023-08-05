from flixpy.models.base import Base
from flixpy.models.provider_base import ProviderBase
from flixpy.models.provider import Provider

from flixpy.utils import get_json

from flixpy.enum.content_type import ContentType
from flixpy.enum.streaming_provider import StreamingProvider


class Movie(Base, ProviderBase):
  """Movie class

  Additional properties:
  - providers

  Additional attributes
  - _availability (points to JSON, used in ProviderBase)

  """

  def __init__(self, slug_or_id,):
    super().__init__(slug_or_id, content_type=ContentType.MOVIE)

    # private
    self._availability = self._json['availability']
