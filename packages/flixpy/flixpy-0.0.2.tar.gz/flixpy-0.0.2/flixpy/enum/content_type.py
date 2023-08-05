from enum import Enum, unique, auto
from flixpy.enum.auto_enum import AutoEnumLower


@unique
class ContentType(AutoEnumLower):
  MOVIE = auto()
  SHOW = auto()
