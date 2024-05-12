from __future__ import annotations

__author__ = 'Robbert Harms'
__date__ = '2024-04-07'
__maintainer__ = 'Robbert Harms'
__email__ = 'robbert@xkls.nl'
__licence__ = 'LGPL v3'

import tempfile
from abc import ABCMeta, abstractmethod
from pathlib import Path
from textwrap import dedent

from musical_games.external.base import SimpleExternalFunction, ExternalFunctionFactory, \
    ApplicableExternalFunctionFactory
from musical_games.external.utils import run_command


def midi_to_wav(midi_in: Path, wav_out: Path, soundfont: Path | None = None, gain: float | None = None) -> None:
    """Convert a midi to wav using an automatically detected midi converter.

    Args:
        midi_in: the location of the midi file
        wav_out: where to place the output wav file.
        soundfont: optionally, the path to the sound font file to use
        gain: number between 0 and 1 to indicate the desired output gain.
    """
    converter_factory = AutoMidiToWavFactory()
    converter_factory.set_soundfont(soundfont)
    converter = converter_factory.create()

    return converter.call(midi_in, wav_out, gain)


class MidiToWavFactory(ExternalFunctionFactory, metaclass=ABCMeta):

    @abstractmethod
    def set_soundfont(self, soundfont: Path | None):
        """Set the soundfont to use by the midi converter.

        Args:
            soundfont: the soundfont to use.
        """

    @abstractmethod
    def create(self) -> MidiToWav:
        """Get the midi to wav converter from this factory.

        Returns:
            The midi to wav converter we can use.
        """


class AutoMidiToWavFactory(MidiToWavFactory, ApplicableExternalFunctionFactory):

    def __init__(self):
        """Factory for midi to wav converters which automatically detects the best available tool on the OS.

        If no suitable tool can be found, a `MissingDependencyError` may be raised.
        """
        super().__init__([Timidity, FluidSynth])
        self._soundfont: Path | None = None

    def set_soundfont(self, soundfont: Path | None):
        self._soundfont = soundfont

    def create(self) -> MidiToWav:
        self._check_available()
        return self._available_functions[0](self._soundfont)


class MidiToWav(SimpleExternalFunction, metaclass=ABCMeta):

    @abstractmethod
    def call(self, midi_in: Path, wav_out: Path, gain: float | None = None) -> None:
        """Convert the given midi file to a wav file at the given location.

        Args:
            midi_in: the location of the midi file
            wav_out: where to place the output wav file.
            gain: number between 0 and 1 to indicate the desired output gain.
        """


class FluidSynth(MidiToWav):
    """Converts midi to wav using the fluidsynth package.

    This class requires the `fluidsynth` package to be installed on the user's system.
    """
    _function_name = 'fluidsynth'

    def __init__(self, soundfont: Path | None = None):
        self._soundfont = soundfont

    def call(self, midi_in: Path, wav_out: Path, gain: float | None = None) -> None:
        gain = gain or 0.1
        wav_out.parent.mkdir(parents=True, exist_ok=True)
        if self._soundfont:
            run_command(['fluidsynth', '-g', str(gain*10), '-F', wav_out, self._soundfont, midi_in])
        else:
            run_command(['fluidsynth', '-g', str(gain * 10), '-F', wav_out, midi_in])


class Timidity(MidiToWav):
    _function_name = 'timidity'

    def __init__(self, soundfont: Path | None = None):
        """Converts midi to wav using the timidity package.

        This class requires the `timidity` package to be installed on the user's system.
        """
        self._soundfont = soundfont
        self._timidity_config = dedent('''
            # Enable all midi effects
            opt -Ewpvsetoz

            # Don't cut sustain to save CPU
            opt --no-fast-decay

            # Pan quickly, even if it sounds bad
            opt --fast-panning

            # Set chorus and reverb by song & soundfont
            opt EFreverb=1
            opt EFchorus=1

            # Never kill voices to save CPU
            opt -k0

            # Sustain fades after three seconds (1500ms)
            opt -m3000
        ''')
        if self._soundfont:
            self._timidity_config += f'soundfont {str(self._soundfont)}'

    def call(self, midi_in: Path, wav_out: Path, gain: float | None = None) -> None:
        gain = gain or 0.1
        wav_out.parent.mkdir(parents=True, exist_ok=True)

        with tempfile.NamedTemporaryFile('w') as tmp_file:
            tmp_file.write(self._timidity_config)
            tmp_file.flush()
            run_command(['timidity', '-c', tmp_file.name, '--output-24bit', f'-A{gain*2000}', '-Ow', '-o', wav_out, midi_in])
