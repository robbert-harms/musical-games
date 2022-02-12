__author__ = 'Robbert Harms'
__date__ = '2022-01-03'
__maintainer__ = 'Robbert Harms'
__email__ = 'robbert@xkls.nl'
__licence__ = 'LGPL v3'


from importlib import resources
from dataclasses import dataclass
from typing import Dict, Any, List

import jinja2
from ruamel.yaml import YAML

from musical_games.dice_games.game_mechanics import GameMechanics
from musical_games.dice_games.typesetting import LilypondDiceGameTypesetter, MidiSettings, TypesetOption


@dataclass
class DiceGame:
    composer: str
    title: str
    game_mechanics: GameMechanics
    typesetter: LilypondDiceGameTypesetter

    def get_typeset_options(self, render_method) -> Dict[str, TypesetOption]:
        """Get the available render options for each of the render methods.

        Args:
            render_method (str): one of {'bars_overview', 'single_bar', 'composition_pdf', 'composition_midi'}

        Returns:
            The available typeset options for the specific render method
        """
        templates = {
            'bars_overview': self.typesetter.bar_overview,
            'single_bar': self.typesetter.single_bar,
            'composition_pdf': self.typesetter.composition_pdf,
            'composition_midi': self.typesetter.composition_midi,
        }
        if render_method not in templates:
            raise ValueError(f'The requested render method {render_method} is not recognized.')
        return templates[render_method].options

    def typeset_bars_overview(self, render_settings=None, out_file=None) -> str:
        """Typeset the bar overview.

        Args:
            render_settings (dict): rendering settings
            out_file (Optional[Path]): if set, we write the typeset lilypond to this location.

        Returns:
            The typeset lilypond as a string
        """
        return self.typesetter.typeset_bars_overview(self.game_mechanics, render_settings, out_file)

    def typeset_single_bar(self, table_name, bar_nmr, render_settings=None, out_file=None) -> str:
        """Typeset a single bar of the dice game.

        Args:
            table_name (str): the name of the table
            bar_nmr (int): the bar number (1-indexed)
            render_settings (dict): the render settings
            out_file (Optional[Path]): if set, we write the typeset lilypond to this location.

        Returns:
            The typeset lilypond as a string
        """
        return self.typesetter.typeset_single_bar(self.game_mechanics, table_name, bar_nmr, render_settings, out_file)

    def typeset_composition_pdf(self, bar_nmrs, render_settings=None, out_file=None) -> str:
        """Typeset a PDF composition of this dice game.

        A dice game composition consists of a dice game and the choices for the dice throws.

        The dice throws are a list of indices from 1-6 or 1-12 (depending on the number dices) for each of the
        required dice throws and each stave of the dice game.

        Args:
            bar_nmrs (Dict[str, Dict[str, List[int]]]): the bars we would like to include in this composition.
                Indexed by table name, staff name and bar number.
            render_settings (dict): rendering settings
            out_file (Optional[Path]): if set, we write the typeset lilypond to this location.

        Returns:
            The typeset lilypond as a string
        """
        return self.typesetter.typeset_composition_pdf(self.game_mechanics, bar_nmrs, render_settings, out_file)

    def typeset_composition_midi(self, bar_nmrs, render_settings=None, out_file=None) -> str:
        """Typeset a midi composition of this dice game.

        A dice game composition consists of a dice game and the choices for the dice throws.

        The dice throws are a list of indices from 1-6 or 1-12 (depending on the number dices) for each of the
        required dice throws and each stave of the dice game.

        Args:
            bar_nmrs (Dict[str, Dict[str, List[int]]]): the bars we would like to include in this composition.
                Indexed by table name, staff name and bar number.
            render_settings (Optional[CompositionMidiRenderSettings]): rendering settings
            out_file (Optional[Path]): if set, we write the typeset lilypond to this location.

        Returns:
            The typeset lilypond as a string
        """
        return self.typesetter.typeset_composition_midi(self.game_mechanics, bar_nmrs, render_settings, out_file)


class CPEBachCounterpoint(DiceGame):

    def __init__(self):
        config = _load_inbuild_config_yaml('cpe_bach_counterpoint')
        super().__init__(**config)


class KirnbergerMenuetTrio(DiceGame):

    def __init__(self):
        config = _load_inbuild_config_yaml('kirnberger_menuet_trio')
        super().__init__(**config)


class KirnbergerPolonaise(DiceGame):

    def __init__(self):
        config = _load_inbuild_config_yaml('kirnberger_polonaise')
        super().__init__(**config)


class MozartWaltz(DiceGame):

    def __init__(self):
        config = _load_inbuild_config_yaml('mozart_waltz')
        super().__init__(**config)


class StadlerMenuetTrio(DiceGame):

    def __init__(self):
        config = _load_inbuild_config_yaml('stadler_menuet_trio')
        super().__init__(**config)


def _load_inbuild_config_yaml(dir_name) -> Dict[str, Any]:
    """Load an YAML configuration from a directory in this package.

    Args:
        dir_name (str): a directory name within the folder "musical_games/data/dice_games"

    Returns:
        All the objects from the configuration loaded
    """
    jinja2_template_loader = jinja2.PackageLoader('musical_games', f'data/dice_games/{dir_name}')

    with resources.path(f'musical_games.data.dice_games.{dir_name}', 'config.yaml') as path:
        with open(path, 'r', encoding='utf-8') as f:
            yaml = YAML(typ='safe')
            data = yaml.load(f)
            return {
                'title': data['title'],
                'composer': data['composer'],
                'game_mechanics': GameMechanics.from_dict(data['game_mechanics']),
                'typesetter': LilypondDiceGameTypesetter.from_dict(data['lilypond_templates'], jinja2_template_loader)
            }
