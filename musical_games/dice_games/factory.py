import importlib
import os
import pkg_resources
import six
import yaml
from musical_games.base import KeySignature, TimeSignature, TempoIndication, MidiOptions
from .utils import load_dice_table, load_bars_from_file
from .base import Composition, CompositionPart, Instrument, Staff

__author__ = 'Robbert Harms'
__date__ = "2015-12-05"
__maintainer__ = "Robbert Harms"
__email__ = "robbert.harms@maastrichtuniversity.nl"


class ComposerInfo(object):

    def is_applicable(self, composer_name, composition_name, instruments_name):
        """Check if this class can generate a composition with the given settings.

        Args:
            composer_name (str): the name of the composer
            composition_name (str): the name of the composition
            instruments_name (str or list of str): the instrument name or a list of names with one name per
                compositional part. If one name is given we use it for all the parts in the composition, else
                one name per part should be given.

        Returns:
            boolean: true if this object can generate a composition for the given settings.
        """

    def get_composition(self, composer_name, composition_name, instruments_name):
        """Get the composition for the given settings.

        Args:
            composer_name (str): the name of the composer
            composition_name (str): the name of the composition
            instruments_name (str or list of str): the instrument name or a list of names with one name per
                compositional part.

        Returns:
            Composition: the generated composition object
        """

    def get_composer_name(self):
        """Get the name of the composer contained in this composer info.

        Returns:
            str: the name of the composer
        """

    def get_compositions(self):
        """Get a list of available compositions for this composer.

        Returns:
            list of str: the list of composition names available for this composer
        """

    def get_instruments(self, composition):
        """Get a list of the available instruments for the given composition of the given composer.

        Args:
            composition (str): the name of the composition

        Returns:
            list of list of str: the list of instruments available per music part.
        """

    def get_composition_parts(self, composition):
        """Get a list of the composition parts in the given composition.

        Args:
            composition (str): the name of the composition

        Returns:
            list of str: the list of composition parts in the asked composition.
        """


class SimpleComposerInfo(ComposerInfo):

    def __init__(self, directory):
        """Reads all the necessary information from a directory.

        This assumes that there is a file named 'manifest.conf' in the root of the given directory and that
        the directory is structured in the order:
            - composition name
                - composition parts
                    - dice table
                    - instruments
                        - staff files
                    ...
                ...
            ...
        """
        self._directory = directory
        self._manifest = self._load_manifest()

    def get_composer_name(self):
        return self._manifest['name']

    def get_compositions(self):
        return [list(composition.items())[0][0] for composition in self._manifest['compositions']]

    def get_instruments(self, composition):
        composition_info = self._get_composition_info(composition)
        part_info = [list(part.items())[0][1] for part in composition_info['parts']]
        instruments = []

        for part in part_info:
            part_instruments = []
            for instrument in part['instruments']:
                part_instruments.extend(instrument.keys())
            instruments.append(part_instruments)

        return instruments

    def get_composition_parts(self, composition):
        composition_info = self._get_composition_info(composition)
        part_info = [list(part.items())[0][0] for part in composition_info['parts']]
        return part_info

    @classmethod
    def from_internal(cls, dir_name):
        return cls(pkg_resources.resource_filename('musical_games', 'data/' + dir_name + '/'))

    def _load_manifest(self):
        """Load the manifest from the given directory"""
        with open(self._directory + '/manifest.conf') as f:
            return yaml.load(f)

    def is_applicable(self, composer_name, composition_name, instruments_name):
        if not self._manifest:
            return False

        try:
            self.get_composition(composer_name, composition_name, instruments_name)
            return True
        except NotFoundException:
            return False

    def get_composition(self, composer_name, composition_name, instruments_name):
        if self._manifest['name'] != composer_name:
            raise NotFoundException('Composer does not match')

        composition_info = self._get_composition_info(composition_name)
        page_limit_composition = composition_info.get('page_limit_composition', None)
        page_limit_measure_overview = composition_info.get('page_limit_measure_overview', None)

        composition_manager_module = importlib.import_module('musical_games.dice_games.composition_managers')
        composition_manager = getattr(composition_manager_module, composition_info['composition_manager'])()

        return Composition(composition_name, composer_name, self._load_composition(composition_info, instruments_name),
                           composition_manager, page_limit_composition, page_limit_measure_overview)

    def _get_composition_info(self, composition_name):
        """Get the info dictionary from the manifest for the composition with the given name.

        Args:
            composition_name (str): the name of the composition we want to get the info of

        Returns:
            dict: the yaml information dictionary

        Raises:
            NotFoundException: if the composition could not be found.
        """
        for composition in self._manifest['compositions']:
            name, info = list(composition.items())[0]
            if name == composition_name:
                return info
        raise NotFoundException('Composition could not be found')

    def _load_composition(self, composition_info, instruments_name):
        """Load the actual composition

        Args:
            composition_info (dict): the composition information dict
            instruments_name (str or list of str): the instrument name or a list of names with one name per
                compositional part.
        """
        parts = []

        instruments_choice = instruments_name
        if isinstance(instruments_name, six.string_types):
            instruments_choice = [instruments_name] * len(composition_info['parts'])

        if len(instruments_choice) < len(composition_info['parts']):
            instruments_choice *= len(composition_info['parts'])

        for ind, part in enumerate(composition_info['parts']):
            name, part_info = list(part.items())[0]

            instrument = self._load_instrument(composition_info['dir'] + '/' + part_info['dir'],
                                               part_info['instruments'], instruments_choice[ind])

            show_title = part_info.get('show_title', True)

            parts.append(CompositionPart(name, instrument, show_title=show_title))

        return parts

    def _load_instrument(self, relative_path, instruments, instrument_name):
        name, instrument_info = self._find_instrument(instruments, instrument_name)

        staffs = self._load_staffs(relative_path + '/' + instrument_info['dir'], instrument_info['staffs'])
        tempo_indication = TempoIndication(*instrument_info['tempo_indication'])
        repeats = instrument_info['repeats']

        converter_module = importlib.import_module('musical_games.dice_games.lilypond.bar_converters')
        bar_converter = getattr(converter_module, instrument_info.get('bar_converter', 'SimpleBarConverter'))()

        staff_layout_module = importlib.import_module('musical_games.dice_games.lilypond.staff_layouts')
        staff_layout = getattr(staff_layout_module, instrument_info.get('staff_layout', 'AutoLayout'))()

        dice_tables_linked = instrument_info.get('dice_tables_linked', True)

        return Instrument(name, staffs, tempo_indication, repeats, staff_layout, bar_converter, dice_tables_linked)

    def _find_instrument(self, instruments_list, instrument_name):
        for item in instruments_list:
            name, instrument_info = list(item.items())[0]
            if name == instrument_name:
                return name, instrument_info
        raise NotFoundException('One of the requested instruments could not be found.')

    def _load_staffs(self, relative_path, staffs_list):
        staffs = []
        for staff in staffs_list:
            name, staff_info = list(staff.items())[0]

            dice_table = self._load_dice_table(relative_path + '/' + staff_info['dice_table'])
            clef = staff_info['clef']
            bars = load_bars_from_file(self._directory + '/' + relative_path + '/' + staff_info['file'])
            key_signature = KeySignature(*staff_info['key_signature'])
            time_signature = TimeSignature(*staff_info['time_signature'])
            instrument_name = staff_info['instrument_name']
            midi_options = MidiOptions(**staff_info['midi_options'])

            staffs.append(Staff(name, dice_table, clef, bars, key_signature, time_signature,
                                instrument_name, midi_options))

        return staffs

    def _load_dice_table(self, relative_path):
        return load_dice_table(os.path.join(self._directory, relative_path))


class NotFoundException(Exception):
    pass


class DiceGameFactory(object):

    composers_info = []

    def get_composers(self):
        """Get a list of available composers

        Args:
            list of str: the list of available composers sorted alphabetically
        """
        return list(sorted(info.get_composer_name() for info in self.composers_info))

    def get_compositions(self, composer):
        """Get a list of available compositions for the given composer.

        Args:
            composer (str): the name of the composer

        Returns:
            list of str: the list of composition names available for this composer
        """
        for info in self.composers_info:
            if info.get_composer_name() == composer:
                return info.get_compositions()

    def get_instruments(self, composer, composition):
        """Get a list of the available instruments for the given composition of the given composer.

        Args:
            composer (str): the name of the composer
            composition (str): the name of the composition

        Returns:
            list of list of str: the list of instruments available for this composition
        """
        for info in self.composers_info:
            if info.get_composer_name() == composer:
                return info.get_instruments(composition)

    def get_composition_parts(self, composer, composition):
        """Get a list of the names of the composition parts in this composition.

        The order of the list is the same as that in the 'get_instruments' function.

        Args:
            composer (str): the name of the composer
            composition (str): the name of the composition

        Returns:
            list of str: the list of composition parts in this composition
        """
        for info in self.composers_info:
            if info.get_composer_name() == composer:
                return info.get_composition_parts(composition)

    def get_composition(self, composer, composition, instruments):
        """Get a Composition object for a composition of the given composer with the given instruments.

        Args:
            composer (str): the name of the composer
            composition(str): the name of the composition
            instruments (str or list of str): the instrument name or a list of names with one name per
                compositional part.

        Returns:
            Composition: the composition object
        """
        args = [composer, composition, instruments]
        for info in self.composers_info:
            if info.is_applicable(*args):
                return info.get_composition(*args)
        raise ValueError('The given composition could not be found.')


for composer in os.listdir(pkg_resources.resource_filename('musical_games', 'data')):
    composer_info = SimpleComposerInfo(pkg_resources.resource_filename('musical_games', 'data/' + composer))
    DiceGameFactory.composers_info.append(composer_info)
