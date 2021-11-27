__author__ = 'Robbert Harms'
__date__ = '2021-11-21'
__maintainer__ = 'Robbert Harms'
__email__ = 'robbert@xkls.nl'
__licence__ = 'LGPL v3'

from pathlib import Path

import jinja2

from musical_games.dice_games.dice_game import DiceGame


class LilypondDiceGameTypesetter:

    def __init__(self, dice_game, jinja2_template_loader):
        """Construct a lilypond typesetter for the provided dice game.

        This requires a loaded dice game and an initialized jinja2 template loader containing the Lilypond templates.

        Args:
            dice_game (DiceGame):
            jinja2_template_loader (jinja2.loaders.BaseLoader): the template loader
        """
        self.dice_game = dice_game
        self.jinja2_template_loader = jinja2_template_loader
        self._jinja2_env = jinja2.Environment(
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
            lstrip_blocks=True,
            loader=jinja2_template_loader)

    def typeset_bars_overview(self, render_options=None, out_file=None) -> str:
        """Typeset the bar overview.

        Args:
            render_options (Optional[Dict]): rendering options, passed directly to the template
            out_file (Optional[Path]): if set, we write the typeset lilypond to this location.

        Returns:
            The typeset lilypond as a string
        """
        render_options = render_options or {}
        template = self._jinja2_env.get_template('bar_overview.ly')
        out_str = template.render(dice_game=self.dice_game, render_options=render_options)

        if out_file is not None:
            self._write_to_file(out_str, out_file)
        return out_str

    def typeset_single_bar(self, table_name, bar_nmr, out_file=None) -> str:
        """Typeset a single bar of the dice game.

        Args:
            table_name (str): the name of the table
            bar_nmr (int): the bar number (1-indexed)
            out_file (Optional[Path]): if set, we write the typeset lilypond to this location.

        Returns:
            The typeset lilypond as a string
        """
        template = self._jinja2_env.get_template('single_bar.ly')
        out_str = template.render(dice_game=self.dice_game, table_name=table_name, bar_nmr=bar_nmr)

        if out_file is not None:
            self._write_to_file(out_str, out_file)
        return out_str

    def typeset_composition(self, bar_nmrs, render_options=None, out_file=None) -> str:
        """Typeset a composition of this dice game.

        A dice game composition consists of a dice game and the choices for the dice throws.

        The dice throws are a list of indices from 1-6 or 1-12 (depending on the number dices) for each of the
        required dice throws and each stave of the dice game.

        Args:
            bar_nmrs (Dict[str, Dict[str, List[int]]]): the bars we would like to include in this composition.
            render_options (Optional[Dict]): rendering options, passed directly to the template
            out_file (Optional[Path]): if set, we write the typeset lilypond to this location.

        Returns:
            The typeset lilypond as a string
        """
        render_options = render_options or {}

        class Composition:

            def __init__(self, dice_game, bar_nmrs):
                self.dice_game = dice_game
                self.bar_nmrs = bar_nmrs

            def get_staff(self, table_name, staff_name, bar_index):
                """Get the chosen bar for the indicated table, staff and bar index.

                Args:
                    table_name (str): the name of the dice table
                    staff_name (str): the name of the staff
                    bar_index (int): the index of the bar

                Returns:
                    str: the lilypond text for the requested staff
                """
                bar_nmr = self.bar_nmrs[table_name][staff_name][bar_index]
                return self.dice_game.bars[table_name][staff_name][bar_nmr]

        template = self._jinja2_env.get_template('composition.ly')
        out_str = template.render(composition=Composition(self.dice_game, bar_nmrs), render_options=render_options)

        if out_file is not None:
            self._write_to_file(out_str, out_file)
        return out_str

    @staticmethod
    def _write_to_file(lilypond_data, out_file):
        """Internal method to write the lilypond data to a file.

        Args:
            lilypond_data (str): the typeset string
            out_file (str or Path): the location to write to
        """
        if isinstance(out_file, str):
            out_file = Path(out_file)

        out_file.parent.mkdir(parents=True, exist_ok=True)
        with open(out_file, 'w') as f:
            f.write(lilypond_data)
