from __future__ import annotations  # needed until Python 3.10

__author__ = 'Robbert Harms'
__date__ = '2021-01-26'
__maintainer__ = 'Robbert Harms'
__email__ = 'robbert@xkls.nl'
__licence__ = 'LGPL v3'

import os
from functools import reduce
from operator import mul

import jinja2
import numpy as np
from numpy.random import RandomState
from pathlib import Path
from typing import Tuple, Dict, Optional
from dataclasses import dataclass, fields
from typing import List

from musical_games.dice_games.utils import get_default_value
import dacite
from ruamel.yaml import YAML


def load_dice_game(fname):
    """Load the data from the provided configuration file and return an DiceGame object.

    Args:
        fname (str): the filename of the composition config file to load

    Returns:
        DiceGame: the dice game
    """
    with open(fname, 'r', encoding='utf-8') as f:
        return load_dice_game_config_string(f.read())


def load_dice_game_config_string(yaml_str):
    """Load the data from the provided yaml formatted string and return a DiceGame object

    Args:
        yaml_str (str): an yaml formatted string to load

    Returns:
        DiceGame: the dice game
    """
    yaml = YAML(typ='safe')
    data = yaml.load(yaml_str)
    return dacite.from_dict(DiceGame, data, config=dacite.Config(
        type_hooks={
            Tuple[int, int]: tuple,
            Tuple[str, str]: tuple
        },
        cast=[Path, DiceTable]))


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
class DiceGame(SimpleDiceGameNode):
    composer: str = None
    title: str = None
    dice_tables: Dict[str, DiceTable] = None
    bars: Dict[str, Dict[str, Dict[int, Optional[str]]]] = None
    typeset_env: jinja2.Environment = None

    def get_full_bar(self, table_name, bar_nmr):
        """Get the full bar with all the staves in a list.

        Args:
            table_name (str): the name of the dice table for which we want the full bar list.
            bar_nmr (int): the number of the bar for which we want all the staves

        Returns:
            List[str]: all the staves in a list
        """
        full_bar = []
        for stave_name, note_items in self.bars[table_name].items():
            full_bar.append(note_items[bar_nmr])
        return full_bar

    def get_full_bar_list(self, table_name):
        """Get the full bars (with all the staves).

        Args:
            table_name (str): the name of the dice table for which we want the full bar list.

        Returns:
            Dict[int, List[str]]: the bars indexed by bar number as a list of staves.
        """
        full_bars = {}
        for stave_name, note_items in self.bars[table_name].items():
            for bar_nmr, notes in note_items.items():
                if bar_nmr not in full_bars:
                    full_bars[bar_nmr] = []
                full_bars[bar_nmr].append(notes)
        return full_bars

    def get_duplicate_bars(self, table_name):
        """Get all the duplicate bars in a given table.

        Args:
            table_name (str): the name of the table

        Returns:
            List[tuple]: list of all the duplicates of the given table, by bar number.
        """
        bar_items = list(self.get_full_bar_list(table_name).items())
        mask = np.zeros(len(bar_items))

        groups = []
        for primary_ind in range(len(bar_items)):
            current_group = [bar_items[primary_ind][0]]
            for secundary_ind in range(primary_ind + 1, len(bar_items)):
                if not mask[secundary_ind]:
                    if bar_items[primary_ind][1] == bar_items[secundary_ind][1]:
                        current_group.append(bar_items[secundary_ind][0])
                        mask[secundary_ind] = 1
            if len(current_group) > 1:
                groups.append(current_group)
        return groups

    def count_unique_compositions(self, count_duplicates=False):
        """Count the number of unique compositions possible by this dice game.

        Args:
            count_duplicates (boolean): if set to False, we exclude all identical bars in a column of the dice matrix.

        Returns:
            int: the number of unique compositions
        """
        def count_unique_bars(table_name, bar_numbers):
            """Count the number of unique bars in the provided list of bar numbers."""
            return len(set([tuple(self.get_full_bar(table_name, nmr)) for nmr in bar_numbers]))

        table_counts = []
        for table_name, table in self.dice_tables.items():
            if count_duplicates:
                table_counts.append(table.max_dice_value ** table.nmr_throws)
            else:
                table_counts.append(reduce(mul, [count_unique_bars(table_name, column)
                                                 for column in table.list_columns()]))
        return reduce(mul, table_counts)

    def random_composition(self, seed=None):
        """Generate a random composition by throwing the dice multiple times.

        Args:
            seed (int): the seed for the random number generator

        Returns:
            DiceGameComposition: the composition object derived from this dice game.
        """
        choices = {}
        for table_name, dice_table in self.dice_tables.items():
            bar_nmrs = dice_table.get_random_selection(seed)

            choices[table_name] = {}
            for stave_name in self.bars[table_name].keys():
                choices[table_name][stave_name] = bar_nmrs

        return DiceGameComposition(self, choices)

    def typeset_bars_overview(self, out_fname, jinja2_environment=None, render_options=None):
        """Typeset an overview of all the measures.

        Args:
            out_fname (str): the output filename
            jinja2_environment (jinja2.Environment): the jinja2 environment to use for typesetting
                If not provided, we will try to load the environment indicated in ``typeset_env``
            render_options (dict): set of render options. Available options are:
                - large_page (boolean): if we want to create a single large page with all content
        """
        if jinja2_environment is None:
            jinja2_environment = self.typeset_env

        render_options = render_options or {}

        if not os.path.exists(dir := os.path.dirname(out_fname)):
            os.makedirs(dir)

        template = jinja2_environment.get_template('bar_overview.ly')
        out_file = template.render(dice_game=self, render_options=render_options)

        with open(out_fname, 'w', encoding='utf-8') as f:
            f.write(out_file)

    def typeset_single_bar(self, table_name, bar_nmr, out_fname, jinja2_environment=None):
        """Typeset a single bar.

        This typesets all the staves of the indicated bar.

        Args:
            table_name (str): the name of the table
            bar_nmr (int): the bar number (1-indexed)
            out_fname (str): the output filename
            jinja2_environment (jinja2.Environment): the jinja2 environment to use for typesetting
                If not provided, we will try to load the environment indicated in ``typeset_env``
        """
        if jinja2_environment is None:
            jinja2_environment = self.typeset_env

        if not os.path.exists(dir := os.path.dirname(out_fname)):
            os.makedirs(dir)

        template = jinja2_environment.get_template('single_bar.ly')
        out_file = template.render(dice_game=self, table_name=table_name, bar_nmr=bar_nmr)

        with open(out_fname, 'w', encoding='utf-8') as f:
            f.write(out_file)


@dataclass
class DiceTable(SimpleDiceGameNode):
    table: np.ndarray

    def __post_init__(self):
        self.table = np.array(self.table)

    @property
    def nmr_dices(self):
        return self.max_dice_value % 2

    @property
    def max_dice_value(self):
        return self.table.shape[0]

    @property
    def nmr_throws(self):
        return self.table.shape[1]

    def list_rows(self):
        """Get a list with the list of row values"""
        return [self.get_row(ind) for ind in range(self.nmr_dices)]

    def list_columns(self):
        """Get a list with the list of column values"""
        return [self.get_column(ind) for ind in range(self.nmr_throws)]

    def get_column(self, column_ind):
        return self.table[:, column_ind]

    def get_row(self, row_ind):
        return self.table[row_ind, :]

    def get_random_selection(self, seed=None):
        """Get a random selection of bar numbers

        Returns:
            List[int]: list of random bar numbers from the table
        """
        prng = RandomState(seed)
        dice_throws = prng.randint(0, self.table.shape[0], self.table.shape[1])
        return self.table[dice_throws, range(self.table.shape[1])]


@dataclass
class DiceGameComposition:
    """A dice game composition consists of a dice game and the choices for the dice throws.

    The dice throws are a list of indices from 1-6 or 1-12 (depending on the number dices) for each of the
    required dice throws and each stave of the dice game.
    """
    dice_game: DiceGame
    bar_nmrs: Dict[str, Dict[str, List[int]]]

    def typeset(self, out_fname, jinja2_environment=None, render_options=None):
        """Typeset a composition as a lilypond .ly file.

        Args:
            out_fname (str): the output filename
            jinja2_environment (jinja2.Environment): the jinja2 environment to use for typesetting
                If not provided, we will try to load the environment indicated in ``DiceGame.typeset_env``
            render_options (dict): set of render options. Available options (depending on the composition) are:
                - large_page (boolean): if we want to create a single large page with all content
        """
        if jinja2_environment is None:
            jinja2_environment = self.dice_game.typeset_env

        render_options = render_options or {}

        if not os.path.exists(dir := os.path.dirname(out_fname)):
            os.makedirs(dir)

        template = jinja2_environment.get_template('composition.ly')
        out_file = template.render(composition=self, render_options=render_options)

        with open(out_fname, 'w', encoding='utf-8') as f:
            f.write(out_file)

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
