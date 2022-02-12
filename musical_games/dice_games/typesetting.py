from __future__ import annotations  # needed until Python 3.10

__author__ = 'Robbert Harms'
__date__ = '2021-11-21'
__maintainer__ = 'Robbert Harms'
__email__ = 'robbert@xkls.nl'
__licence__ = 'LGPL v3'

from copy import copy
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any

import jinja2

jinja2_environment_options = dict(
    block_start_string=r'\BLOCK{',
    block_end_string='}',
    variable_start_string=r'\VAR{',
    variable_end_string='}',
    comment_start_string=r'\#{',
    comment_end_string='}',
    line_statement_prefix='%-',
    line_comment_prefix='%#',
    trim_blocks=True,
    autoescape=False,
    lstrip_blocks=True
)


@dataclass
class LilypondDiceGameTypesetter:
    bar_overview: TypesetTemplate
    composition_midi: TypesetTemplate
    composition_pdf: TypesetTemplate
    single_bar: TypesetTemplate

    @classmethod
    def from_dict(cls, data, jinja2_loader):
        """Load a dice game typesetter from a configuration dictionary.

        Args:
            data (Dict): the configuration dictionary
            jinja2_loader: the loader with the location of the template files.
        """
        env_options = copy(jinja2_environment_options)
        env_options.update({'loader': jinja2_loader})
        env = jinja2.Environment(**env_options)

        result = {}
        for key, config in data.items():
            result[key] = TypesetTemplate.from_dict(env.get_template(config['filename']), config.get('options'))

        return cls(**result)

    def typeset_bars_overview(self, game_mechanics, render_settings=None, out_file=None) -> str:
        """Typeset the bar overview.

        Args:
            game_mechanics (GameMechanics): the object with the game data
            render_settings (dict): rendering settings
            out_file (Optional[Path]): if set, we write the typeset lilypond to this location.

        Returns:
            The typeset lilypond as a string
        """
        return self.bar_overview.render({'game_mechanics': game_mechanics}, render_settings, out_file)

    def typeset_single_bar(self, game_mechanics, table_name, bar_nmr, render_settings=None, out_file=None) -> str:
        """Typeset a single bar of the dice game.

        Args:
            game_mechanics (GameMechanics): the object with the game data
            table_name (str): the name of the table
            bar_nmr (int): the bar number (1-indexed)
            render_settings (dict): the render settings
            out_file (Optional[Path]): if set, we write the typeset lilypond to this location.

        Returns:
            The typeset lilypond as a string
        """
        return self.single_bar.render(
            {'game_mechanics': game_mechanics, 'table_name': table_name, 'bar_nmr': bar_nmr},
            render_settings, out_file)

    def typeset_composition_pdf(self, game_mechanics, bar_nmrs, render_settings=None, out_file=None) -> str:
        """Typeset a PDF composition of this dice game.

        A dice game composition consists of a dice game and the choices for the dice throws.

        The dice throws are a list of indices from 1-6 or 1-12 (depending on the number dices) for each of the
        required dice throws and each stave of the dice game.

        Args:
            game_mechanics (GameMechanics): the object with the game data
            bar_nmrs (Dict[str, Dict[str, List[int]]]): the bars we would like to include in this composition.
                Indexed by table name, staff name and bar number.
            render_settings (dict): rendering settings
            out_file (Optional[Path]): if set, we write the typeset lilypond to this location.

        Returns:
            The typeset lilypond as a string
        """
        return self.composition_pdf.render(
            {'game_mechanics': game_mechanics, 'bar_nmrs': bar_nmrs},
            render_settings, out_file)

    def typeset_composition_midi(self, game_mechanics, bar_nmrs, render_settings=None, out_file=None) -> str:
        """Typeset a midi composition of this dice game.

        A dice game composition consists of a dice game and the choices for the dice throws.

        The dice throws are a list of indices from 1-6 or 1-12 (depending on the number dices) for each of the
        required dice throws and each stave of the dice game.

        Args:
            game_mechanics (GameMechanics): the object with the game data
            bar_nmrs (Dict[str, Dict[str, List[int]]]): the bars we would like to include in this composition.
                Indexed by table name, staff name and bar number.
            render_settings (Optional[CompositionMidiRenderSettings]): rendering settings
            out_file (Optional[Path]): if set, we write the typeset lilypond to this location.

        Returns:
            The typeset lilypond as a string
        """
        return self.composition_midi.render(
            {'game_mechanics': game_mechanics, 'bar_nmrs': bar_nmrs},
            render_settings, out_file)


class TypesetTemplate:

    def __init__(self, jinja2_template, options):
        """A template with preconfigured options.

        When rendering a template, it will check the provided settings against the configured template options.
        If required values are missing a warning is raised, else, either default values are used or the
        provided settings.

        Args:
             jinja2_template (jinja2.Template): the template to render
             options (Dict[str, TypesetOption]): typeset options indexed by variable name
        """
        self.jinja2_template = jinja2_template
        self.options = options

    @classmethod
    def from_dict(cls, jinja2_template, options_dict=None):
        options = {}
        if options_dict:
            options = {key: TypesetOption.from_dict(value) for key, value in options_dict.items()}
        return cls(jinja2_template, options)

    def render(self, render_data, render_settings, out_file=None):
        """Render this template using the provided game mechanics and settings.

        This will amend the provided settings with the default options in the case of missing settings.

        Args:
            render_data (dict): the data we want to render
            render_settings (dict): rendering settings, will be checked and formatted
            out_file (Optional[Path]): if set, we write the typeset lilypond to this location.

        Returns:
            The typeset lilypond as a string
        """
        final_settings = self._process_settings(render_settings)
        out_str = self.jinja2_template.render(render_settings=final_settings, **render_data)

        if out_file is not None:
            if isinstance(out_file, str):
                out_file = Path(out_file)

            out_file.parent.mkdir(parents=True, exist_ok=True)
            with open(out_file, 'w') as f:
                f.write(out_str)

        return out_str

    def _process_settings(self, render_settings) -> Dict[str, Any]:
        """Process the settings and check for missing or wrong values."""
        result = {}

        if render_settings:
            for key, value in render_settings.items():
                if key in self.options:
                    if not isinstance(value, self.options[key].dtype):
                        raise ValueError(f'The value for {key}, "{value}" is not '
                                         f'of the desired type {self.options[key].dtype}')
                else:
                    raise ValueError(f'The provided option {key} is not recognized as a valid render setting.')
                result[key] = value

        for key, value in self.options.items():
            if key not in result:
                result[key] = value.default_value

        return result


class TypesetOption:

    def __init__(self, dtype, default_value):
        self.dtype = dtype
        self.default_value = default_value

    @classmethod
    def from_dict(cls, data):
        dtypes = {
            'str': str,
            'bool': bool,
            'float': float,
            'int': int,
            'MidiSettings': MidiSettings
        }
        dtype = dtypes[data['type']]

        default_value = data.get('default')
        if dtype is MidiSettings:
            default_value = MidiSettings(*default_value)
        return cls(dtype, default_value)


class MidiSettings:

    def __init__(self, instrument='acoustic grand', min_volume=0, max_volume=1):
        """Container object for midi settings."""
        self.instrument = instrument
        self.min_volume = min_volume
        self.max_volume = max_volume
