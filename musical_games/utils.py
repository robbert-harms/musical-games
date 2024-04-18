from __future__ import annotations

__author__ = 'Robbert Harms'
__date__ = "2015-09-23"
__maintainer__ = "Robbert Harms"
__email__ = "robbert@xkls.nl"

from concurrent.futures.thread import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path

from musical_games.external.wav_converters import wav_to_mp3, wav_to_ogg
from musical_games.external.midi_converters import midi_to_wav
from musical_games.external.lilypond import typeset_lilypond, LilypondTypesetResults


def auto_convert_lilypond_file(lilypond_in: Path, soundfont: Path | None = None, output_basename: Path | None = None,
                               pdf: bool = True, png: bool = True, ps: bool = False, mp3: bool = True,
                               ogg: bool = True, midi_gain: float | None = None,
                               trim_png: bool = True) -> AutoConvertLilypondResults:
    """Converts a lilypond file to pdf, png, midi, wav, mp3 and ogg.

    Given a lilypond file we create some common output files you are typically interested in.

    Args:
        lilypond_in: the lilypond file name
        soundfont: the path to the soundfont to use. If not given we will not convert to wav, mp3 and ogg.
        output_basename: path + file prefix. If None we use the dir and basename of the lilypond file.
        pdf: if we want pdf output
        png: if we want png output
        ps: if we want postscript output
        mp3: if we want mp3 output, only applicable if the lilypond has midi output defined
        ogg: if we want ogg output, only applicable if the lilypond has midi output defined
        midi_gain: the gain for use during the midi to wav conversion
        trim_png: if we want to automatically trim the png outputs

    Returns:
        Information about the file names that were outputted
    """
    if not output_basename:
        output_basename = lilypond_in.parent / lilypond_in.stem

    typeset_results = typeset_lilypond(lilypond_in, output_basename, pdf=pdf, png=png, ps=ps, trim_png=trim_png)

    wav_list = []
    mp3_list = []
    ogg_list = []

    with ThreadPoolExecutor() as executor:
        for midi_conversion_result in executor.map(lambda midi_file: _convert_midi(midi_file, soundfont=soundfont,
                                                                                   midi_gain=midi_gain,
                                                                                   output_mp3=mp3, output_ogg=ogg),
                                                   typeset_results.midi_list):
            wav_list.append(midi_conversion_result['wav'])
            if 'mp3' in midi_conversion_result:
                mp3_list.append(midi_conversion_result['mp3'])
            if 'ogg' in midi_conversion_result:
                ogg_list.append(midi_conversion_result['ogg'])

    return AutoConvertLilypondResults(typeset_results, wav_list, mp3_list, ogg_list)


def _convert_midi(midi_in: Path, soundfont: Path | None = None,
                  midi_gain: float | None = None, output_mp3: bool = True,
                  output_ogg: bool = True) -> dict[str, Path]:
    """Small utility for use in multiprocessing, converting midi to wav, mp3 and ogg.

    Args:
        midi_in: the input midi file to convert
        soundfont: the optional soundfont to use
        midi_gain: the midi gain for midi conversion
        output_mp3: if we want to output mp3
        output_ogg: if we want to output ogg

    Returns:
        A dictionary with at least the key "wav" and optionally the keys "mp3" and "ogg".
    """
    results = {}

    wav_file = midi_in.with_suffix('.wav')
    midi_to_wav(midi_in, wav_file, soundfont, gain=midi_gain)
    results['wav'] = wav_file

    if output_mp3:
        mp3_file = wav_file.with_suffix('.mp3')
        wav_to_mp3(wav_file, mp3_file)
        results['mp3'] = mp3_file

    if output_ogg:
        ogg_file = wav_file.with_suffix('.ogg')
        wav_to_ogg(wav_file, ogg_file)
        results['ogg'] = ogg_file

    return results


@dataclass(frozen=True, slots=True)
class AutoConvertLilypondResults:
    """Results from converting the lilypond input to common output files.

    Args:
        typeset_results: the typeset musical scores output
        wav_list: list of generated wav files
        mp3_list: list of generated mp3 files
        ogg_list: list of generated ogg files
    """
    typeset_results: LilypondTypesetResults
    wav_list: list[Path]
    mp3_list: list[Path]
    ogg_list: list[Path]

    @property
    def pdf_list(self):
        return self.typeset_results.pdf_list

    @property
    def png_list(self):
        return self.typeset_results.png_list

    @property
    def ps_list(self):
        return self.typeset_results.ps_list

    @property
    def midi_list(self):
        return self.typeset_results.midi_list
