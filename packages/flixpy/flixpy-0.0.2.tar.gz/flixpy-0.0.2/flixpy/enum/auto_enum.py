from enum import Enum


class AutoEnumLower(Enum):
  # use to automiatcally generate enaum value (SOME_ENUM => some_enum)
  # pylint: disable=no-self-argument
  def _generate_next_value_(name, start, count, last_values):
    return str(name).lower()


class AutoEnumDashes(Enum):
  # convert AB_C to ab-c
  # pylint: disable=no-self-argument
  def _generate_next_value_(name, start, count, last_values):
    return str(name).lower().replace('_', '-')