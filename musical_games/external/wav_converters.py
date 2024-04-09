from __future__ import annotations

__author__ = 'Robbert Harms'
__date__ = "2015-09-22"
__maintainer__ = "Robbert Harms"
__email__ = "robbert@xkls.nl"

from abc import ABCMeta, abstractmethod
from pathlib import Path

from musical_games.external.base import ExternalFunctionFactory, ApplicableExternalFunctionFactory, \
    SimpleExternalFunction
from musical_games.external.utils import run_command


def wav_to_mp3(wav_in: Path, mp3_out: Path):
    """Auto-detects a wav converter to convert the wav to an mp3 file.

    Args:
        wav_in: the location of the wav file
        mp3_out: the path to the output mp3 file
    """
    converter_factory = AutoWavConverterFactory()
    converter = converter_factory.create()
    return converter.to_mp3(wav_in, mp3_out)


def wav_to_ogg(wav_in: Path, ogg_out: Path):
    """Auto-detects a wav converter to convert the wav to an ogg file.

    Args:
        wav_in: the location of the wav file
        mp3_out: the path to the output mp3 file
    """
    converter_factory = AutoWavConverterFactory()
    converter = converter_factory.create()
    return converter.to_ogg(wav_in, ogg_out)


class WavConverterFactory(ExternalFunctionFactory, metaclass=ABCMeta):

    @abstractmethod
    def create(self) -> WavConverter:
        """Get the WAV converter from this factory.

        Returns:
            The wav converter we can use.
        """


class AutoWavConverterFactory(WavConverterFactory, ApplicableExternalFunctionFactory):

    def __init__(self):
        """Factory for wav converters which automatically detects the best available tool on the OS.

        If no suitable tool can be found, a `MissingDependencyError` may be raised.
        """
        super().__init__([FFMpeg])

    def create(self) -> WavConverter:
        self._check_available()
        return self._available_functions[0]()


class WavConverter(SimpleExternalFunction, metaclass=ABCMeta):
    """Converter for converting wav to any other media format."""

    @abstractmethod
    def to_mp3(self, wav_in: Path, mp3_out: Path):
        """Convert the given wav file to an mp3 file.

        Args:
            wav_in: the wav filename
            mp3_out: the output file
        """

    @abstractmethod
    def to_ogg(self, wav_in: Path, ogg_out: Path):
        """Convert the given wav file to an ogg file.

        Args:
            wav_in: the wav filename
            ogg_out: the output file
        """


class FFMpeg(WavConverter):
    _function_name = 'ffmpeg'

    def to_mp3(self, wav_in: Path, mp3_out: Path):
        mp3_out.parent.mkdir(parents=True, exist_ok=True)
        run_command(['ffmpeg', '-y', '-i', wav_in, '-vn', '-ar', '44100',
                     '-ac', '2', '-ab', '192k', '-f', 'mp3', mp3_out])

    def to_ogg(self, wav_in: Path, ogg_out: Path):
        ogg_out.parent.mkdir(parents=True, exist_ok=True)
        run_command(['ffmpeg', '-y', '-i', wav_in, '-acodec', 'libvorbis', ogg_out])
