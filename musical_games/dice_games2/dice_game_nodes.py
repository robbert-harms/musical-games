from __future__ import annotations  # needed until Python 3.10

__author__ = 'Robbert Harms'
__date__ = '2021-01-26'
__maintainer__ = 'Robbert Harms'
__email__ = 'robbert@xkls.nl'
__licence__ = 'LGPL v3'


from typing import Tuple, Dict
from dataclasses import dataclass, field, fields
from typing import List
from musical_games.dice_games2.utils import get_default_value


@dataclass
class DiceGameNode:
    """Basic inheritance class for all dice games related content nodes."""

    def get_default_value(self, attribute_name):
        """Get the default value for an attribute of this node.

        Args:
            attribute_name (str): the name of the attribute for which we want the default value

        Returns:
            Any: the default value
        """
        raise NotImplementedError()


class SimpleDiceGameNode(DiceGameNode):
    """Simple implementation of the required methods of an DiceGameNode."""

    @classmethod
    def get_default_value(cls, field_name):
        """By default, resolve the default value using the dataclass fields."""
        for field in fields(cls):
            if field.name == field_name:
                return get_default_value(field)
        raise AttributeError('No default value found for class.')

    def __post_init__(self):
        """By default, initialize the fields using the :func:`get_default_value` using the dataclass fields."""
        for field in fields(self):
            value = getattr(self, field.name)
            if value is None:
                setattr(self, field.name, get_default_value(field))


@dataclass
class Composition(SimpleDiceGameNode):
    composer: str = None
    title: str = None
    parts: List[CompositionParts] = field(default_factory=list)
    output_options: OutputOptions = field(default_factory=lambda: OutputOptions())


@dataclass
class CompositionParts(SimpleDiceGameNode):
    title: str = None
    repeats: List = field(default_factory=list)
    tempo: Tuple[int, int] = None
    instruments: List[InstrumentPart] = field(default_factory=list)
    output_options: OutputOptions = field(default_factory=lambda: OutputOptions())


@dataclass
class InstrumentPart(SimpleDiceGameNode):
    instrument: str = None
    key: Tuple[str, str] = None
    time: Tuple[int, int] = None
    staffs: List[InstrumentPartStaff] = field(default_factory=list)


@dataclass
class InstrumentPartStaff(SimpleDiceGameNode):
    clef: str = None
    bars: Dict[int, str] = None
    dice_table: List[List] = None
    output_options: OutputOptions = field(default_factory=lambda: OutputOptions())


@dataclass
class OutputOptions(SimpleDiceGameNode):
    pdf: PDFOutputOptions = field(default_factory=lambda: PDFOutputOptions())
    midi: MidiOutputOptions = field(default_factory=lambda: MidiOutputOptions())


@dataclass
class PDFOutputOptions(SimpleDiceGameNode):
    """The PDF output flags.

    Args:
        page_limit (int): the page limit, lilypond tries to limit the pdf output to this number of pages.
        show_title (str): if we show the title of this composition or sub-composition
    """
    page_limit: int = None
    show_title: bool = True


@dataclass
class MidiOutputOptions(SimpleDiceGameNode):
    """The MIDI output flags.

    Args:
        instrument (str): the midi instrument to use
        min_volume (str): the minimum dynamic volume for this composition, subcompsition or staff
        max_volume (str): the maximum dynamic volume for this composition, subcompsition or staff
    """
    instrument: str = 'acoustic grand'
    min_volume: float = 0
    max_volume: float = 1
