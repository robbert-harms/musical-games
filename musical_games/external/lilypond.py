__author__ = 'Robbert Harms'
__date__ = "2015-09-22"
__maintainer__ = "Robbert Harms"
__email__ = "robbert@xkls.nl"

from dataclasses import dataclass
from pathlib import Path
import os

from musical_games.external.images import trim_image
from musical_games.external.utils import run_command


def typeset_lilypond(lilypond_in: Path, output_basename: Path, pdf: bool = True, png: bool = True, ps: bool = False,
                     trim_png: bool = True):
    """Typeset a lilypond file and produce midi and/or a composition from the input file.

    This runs the shell command lilypond to on the inputs. Note that Midi output needs to be defined in the lilypond
    file and can not be set on the command line.

    Args:
        lilypond_in: the location of the lilypond file to convert.
        output_basename: the location for the output files, suffixes will be added.
        pdf: if we want pdf output
        png: if we want png output
        ps: if we want postscript output
        trim_png: if we want to automatically trim the PNG images.

    Raises:
        RuntimeError: if the compilation of the lilypond file failed somehow.

    Returns:
        LilypondTypesetResults: the result set with the location of the output files.
    """
    output_basename.parent.mkdir(parents=True, exist_ok=True)

    command = ['lilypond']
    if pdf:
        command.append('--pdf')
    if png:
        command.append('--png')
    if ps:
        command.append('--ps')
    command.extend(['-o', output_basename, lilypond_in])

    run_command(command)

    pdf_list = [output_basename.with_suffix('.pdf')] if pdf else []
    png_list = _get_png_list(output_basename) if png else []
    ps_list = [output_basename.with_suffix('.ps')] if ps else []
    midi_list = _get_midi_list(output_basename)

    if trim_png:
        for png in png_list:
            trim_image(png)

    return LilypondTypesetResults(pdf_list, png_list, ps_list, midi_list)


@dataclass(frozen=True, slots=True)
class LilypondTypesetResults:
    """Result set for the output of the lilypond function.

    Args:
        pdf_list: the locations of the output pdf files
        png_list: the locations of the png files
        ps_list: the locations of the ps files
        midi_list: the locations of the midi files
    """
    pdf_list: list[Path]
    png_list: list[Path]
    ps_list: list[Path]
    midi_list: list[Path]


def _get_png_list(output_basename: Path) -> list[Path]:
    """Get the list of PNG images created by the lilypond typesetter.

    Args:
        output_basename: the basename of the output

    Returns:
        A list of paths to the generated output files.
    """
    png_list = []
    if output_basename.with_suffix('.png').exists():
        png_list.append(output_basename.with_suffix('.png'))

    i = 1
    while os.path.isfile(str(output_basename) + '-page{}.png'.format(i)):
        png_list.append(Path(str(output_basename) + '-page{}.png'.format(i)))
        i += 1
    return png_list


def _get_midi_list(output_basename: Path) -> list[Path]:
    """Get the list of midi images created by the lilypond typesetter.

    Args:
        output_basename: the basename of the output

    Returns:
        A list of paths to the generated midi files.
    """
    midi_list = []
    if output_basename.with_suffix('.midi').exists():
        midi_list.append(output_basename.with_suffix('.midi'))

    i = 1
    while os.path.isfile(str(output_basename) + '-{}.midi'.format(i)):
        midi_list.append(Path(str(output_basename) + '-{}.midi'.format(i)))
        i += 1

    return midi_list
