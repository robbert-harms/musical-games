from __future__ import annotations  # needed until Python 3.10

__author__ = 'Robbert Harms'
__date__ = '2021-01-26'
__maintainer__ = 'Robbert Harms'
__email__ = 'robbert@xkls.nl'
__licence__ = 'LGPL v3'

from abc import ABCMeta
from functools import reduce
from operator import mul

import numpy as np
from numpy.random import RandomState
from pathlib import Path
from typing import Tuple, Dict, Optional
from dataclasses import dataclass, fields
from typing import List

from musical_games.dice_games.utils import get_default_value
import dacite
from ruamel.yaml import YAML


@dataclass
class DiceGameNode(metaclass=ABCMeta):
    """Basic inheritance class for all dice games related content nodes."""


@dataclass
class SimpleDiceGameNode(DiceGameNode):
    """Simple implementation of the required methods of an DiceGameNode."""

    def __post_init__(self):
        """By default, initialize the fields using the dataclass fields."""
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

    @classmethod
    def from_file(cls, fname) -> DiceGame:
        """Load the data from the provided configuration file and return an DiceGame object.

        Args:
            fname (str): the filename of the YAML config file to load

        Returns:
            The loaded dice game
        """
        with open(fname, 'r', encoding='utf-8') as f:
            return cls.from_yaml_config(f.read())

    @classmethod
    def from_yaml_config(cls, yaml_str) -> DiceGame:
        """Load the data from the provided yaml formatted string and return a DiceGame object

        Args:
            yaml_str (str): an yaml formatted string to load

        Returns:
            The loaded dice game
        """
        yaml = YAML(typ='safe')
        data = yaml.load(yaml_str)
        return dacite.from_dict(DiceGame, data, config=dacite.Config(
            type_hooks={
                Tuple[int, int]: tuple,
                Tuple[str, str]: tuple
            },
            cast=[Path, DiceTable]))

    def get_full_bar(self, table_name, bar_nmr) -> List[str]:
        """Get the full bar with all the staves in a list.

        Args:
            table_name (str): the name of the dice table for which we want the full bar list.
            bar_nmr (int): the number of the bar for which we want all the staves

        Returns:
            All the staves in a list
        """
        full_bar = []
        for stave_name, note_items in self.bars[table_name].items():
            full_bar.append(note_items[bar_nmr])
        return full_bar

    def get_full_bar_list(self, table_name) -> Dict[int, List[str]]:
        """Get the full bars (with all the staves).

        Args:
            table_name (str): the name of the dice table for which we want the full bar list.

        Returns:
            The bars indexed by bar number as a list of staves.
        """
        full_bars = {}
        for stave_name, note_items in self.bars[table_name].items():
            for bar_nmr, notes in note_items.items():
                if bar_nmr not in full_bars:
                    full_bars[bar_nmr] = []
                full_bars[bar_nmr].append(notes)
        return full_bars

    def get_duplicate_bars(self, table_name) -> List[List]:
        """Get all the duplicate bars in a given table.

        Args:
            table_name (str): the name of the table

        Returns:
            List of all the duplicates of the given table, by bar number.
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

    def count_unique_compositions(self, count_duplicates=False) -> int:
        """Count the number of unique compositions possible by this dice game.

        Args:
            count_duplicates (boolean): if set to False, we exclude all identical bars in a column of the dice matrix.

        Returns:
            The number of unique compositions
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

    def get_random_bar_nmrs(self, seed=None) -> Dict[str, Dict[str, List[int]]]:
        """Get a selection of random bar numbers to form a composition.

        Args:
            seed (int): the seed for the random number generator

        Returns:
            A composition represented as a dictionary of random bar numbers.
        """
        choices = {}
        for table_name, dice_table in self.dice_tables.items():
            bar_nmrs = dice_table.get_random_selection(seed)

            choices[table_name] = {}
            for stave_name in self.bars[table_name].keys():
                choices[table_name][stave_name] = bar_nmrs
        return choices


@dataclass
class DiceTable(SimpleDiceGameNode):
    """Representation of a dice table used in playing the dice games."""
    table: np.ndarray

    def __post_init__(self):
        super().__post_init__()
        self.table = np.array(self.table)
        if np.any((self.table - self.table.astype(int)) != 0):
            raise ValueError('The dice table must be initialized with only integer values.')

    @property
    def nmr_dices(self) -> int:
        """Get the number of dices this table needs."""
        return self.max_dice_value % 2

    @property
    def max_dice_value(self) -> int:
        """Get the maximum dice value needed to select row from this dice table."""
        return self.table.shape[0]

    @property
    def nmr_throws(self) -> int:
        """Get the maximum number of throws needed to select all the columns from this dice table."""
        return self.table.shape[1]

    def list_rows(self) -> List[List[int]]:
        """Get a list with the list of row values"""
        return self.table.tolist()

    def list_columns(self) -> List[List[int]]:
        """Get a list with the list of column values"""
        return self.table.T.tolist()

    def get_column(self, column_ind) -> List[int]:
        return self.table[:, column_ind]

    def get_row(self, row_ind) -> List[int]:
        return self.table[row_ind, :]

    def get_random_selection(self, seed=None) -> List[int]:
        """Get a random selection of bar numbers

        Returns:
            A list of random bar numbers from the table
        """
        prng = RandomState(seed)
        dice_throws = prng.randint(0, self.table.shape[0], self.table.shape[1])
        return self.table[dice_throws, range(self.table.shape[1])]
