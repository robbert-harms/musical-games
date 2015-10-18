import os
import itertools
from musical_games.converters.audio import midi_to_wav, wav_to_mp3, wav_to_ogg
from musical_games.converters.images import trim_image, concatenate_images
from musical_games.converters.lilypond import lilypond

__author__ = 'Robbert Harms'
__date__ = "2015-09-23"
__maintainer__ = "Robbert Harms"
__email__ = "robbert.harms@maastrichtuniversity.nl"


def correct_indent(string, nmr_spaces):
    """Remove the lowest nmr of spaces (> 0) from every string and then indent by the given number of tabs.

    This will first convert all tabs to 4 spaces.

    Args:
        string (str): the string to correct the indentation
        nmr_spaces (int): the number of spaces to indent by.

    Returns:
        string: the same string with the indent offset corrected
    """
    string = string.replace("\t", ' '*4)
    lines = string.split("\n")

    def nmr_front_tabs(line):
        if len(line.strip()) == 0:
            return None
        return len(list(itertools.takewhile(lambda c: c == ' ', line)))

    try:
        offset_remove = min(filter(lambda v: v is not None, map(nmr_front_tabs, lines)))
        lines = [' ' * nmr_spaces + line[offset_remove:] for line in lines]
    except ValueError:
        pass

    return "\n".join(lines)


def write_lilypond_file(filename, lilypond_str):
    """Write the given lilypond string to the given file.

    Args:
        filename (str): the full path and name of the file to write
        lilypond_str (str): the string with the lilypond content.
    """
    if not os.path.isdir(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))

    with open(filename, 'w') as f:
        f.write(lilypond_str)


def auto_convert_lilypond_file(lilypond_filename, soundfont=None, output_prefix=None, pdf=True, png=True, ps=False):
    """Converts a lilypond file to pdf, png, midi, wav, mp3 and ogg.

    The idea is that given a lilypond file you want to have some standard output. This wrapper function
    will give you the common output files.

    Args:
        lilypond_filename (str): the lilypond file name
        soundfont (str): the path to the soundfont to use. If not given we will not convert to wav, mp3 and ogg.
        output_prefix (str): path + file prefix. If None we use the dir and basename of the lilypond file.
        pdf (str): if we want pdf output
        png (boolean): if we want png output
        ps (boolean): if we want postscript output

    Returns:
        LilypondConvertOutput: all the filenames that were outputted
    """
    output_prefix = output_prefix or os.path.splitext(lilypond_filename)[0]

    lilypond_conversion_results = lilypond(lilypond_filename, output_prefix, pdf=pdf, png=png, ps=ps)

    list(map(trim_image, lilypond_conversion_results.png_list))

    concatenated_image = output_prefix + '_concat.png'
    concatenate_images(concatenated_image, lilypond_conversion_results.png_list)

    wav_list = []
    mp3_list = []
    ogg_list = []

    if soundfont:
        for midi_file in lilypond_conversion_results.midi_list:
            wav_file = os.path.splitext(midi_file)[0] + '.wav'
            mp3_file = os.path.splitext(midi_file)[0] + '.mp3'
            ogg_file = os.path.splitext(midi_file)[0] + '.ogg'

            midi_to_wav(midi_file, wav_file, soundfont)
            wav_to_mp3(wav_file, mp3_file)
            wav_to_ogg(wav_file, ogg_file)

            wav_list.append(wav_file)
            mp3_list.append(mp3_file)
            ogg_list.append(ogg_file)

    return ConvertLilypondResults(
        lilypond_conversion_results.pdf_list,
        lilypond_conversion_results.png_list,
        concatenated_image,
        lilypond_conversion_results.midi_list,
        wav_list, mp3_list, ogg_list)


class ConvertLilypondResults(object):

    def __init__(self, pdf_list, png_list, concatenated_png, midi_list, wav_list, mp3_list, ogg_list):
        """The output object from converting a lilypond file to the most common outputs."""
        self.pdf_list = pdf_list
        self.png_list = png_list
        self.concatenated_png = concatenated_png
        self.midi_list = midi_list
        self.wav_list = wav_list
        self.mp3_list = mp3_list
        self.ogg_list = ogg_list