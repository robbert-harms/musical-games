import os
import textwrap
from musical_games.converters.audio import midi_to_wav, wav_to_mp3, wav_to_ogg
from musical_games.converters.images import trim_image, concatenate_images, draw_rectangle, get_image_size
from musical_games.converters.lilypond import lilypond, TypesetResults
from musical_games.converters.utils import run_command

__author__ = 'Robbert Harms'
__date__ = "2015-09-23"
__maintainer__ = "Robbert Harms"
__email__ = "robbert.harms@maastrichtuniversity.nl"


def correct_indent(string, nmr_spaces):
    """Dedents the string first, then indents by the given number of spaces.

    Args:
        string (str): the string to correct the indentation
        nmr_spaces (int): the number of spaces to indent by.

    Returns:
        string: the same string with the indent set to the nmr of spaces given.
    """
    return ' ' * nmr_spaces + textwrap.dedent(string).replace('\n', '\n' + ' ' * nmr_spaces)


def write_lilypond_book(filename, lilypond_book):
    """Write the given lilypond string to the given file.

    Args:
        filename (str): the full path and name of the file to write
        lilypond_book (LilypondBook): the book with the lilypond content.
    """
    if not os.path.isdir(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))

    with open(filename, 'w') as f:
        f.write(lilypond_book.book)


class PNGConcatenation(object):

    def concatenate(self, png_list, output_fname):
        """Concatenate the images.

        This will do some minor preprocessing to the output images. It will trim the whitespace and remove
        the page numbers from the pngs.

        Args:
            png_list (list of str): the list of pngs to concatenate
            output_fname (str): the name of the output file
        """
        processed_images = []
        for ind, png in enumerate(png_list):
            if ind > 0:
                processed_image = os.path.splitext(png)[0] + '_processed.png'

                if ind % 2:
                    draw_rectangle(png, 'white', 'white', 1, (0, 0), (60, 33), output_fname=processed_image)
                else:
                    image_size = get_image_size(png)
                    position = (image_size[0] - 60, 0)
                    end_position = (image_size[0], 33)

                    draw_rectangle(png, 'white', 'white', 1, position, end_position,
                                   output_fname=processed_image)

                processed_images.append(processed_image)

        concat_list = [png_list[0]]
        concat_list.extend(processed_images)

        concatenate_images(output_fname, concat_list)
        trim_image(output_fname)

        for png in processed_images:
            os.remove(png)


def auto_convert_lilypond_file(lilypond_filename, sound_font=None,
                               output_prefix=None, pdf=True, png=True, ps=False, mp3=True, ogg=True,
                               png_concatenation=None):
    """Converts a lilypond file to pdf, png, midi, wav, mp3 and ogg.

    The idea is that given a lilypond file you want to have some standard output. This wrapper function
    will give you the common output files.

    Args:
        lilypond_filename (str): the lilypond file name
        sound_font (str): the path to the soundfont to use. If not given we will not convert to wav, mp3 and ogg.
        output_prefix (str): path + file prefix. If None we use the dir and basename of the lilypond file.
        pdf (str): if we want pdf output
        png (boolean): if we want png output
        ps (boolean): if we want postscript output
        mp3 (boolean): if we want mp3 output, only applicable if the lilypond has midi output defined
        ogg (boolean): if we want ogg output, only applicable if the lilypond has midi output defined
        png_concatenation (PNGConcatenation): the concatenation routine to use for concatenating the PNGs

    Returns:
        LilypondConvertOutput: information about the file names that were outputted
    """
    output_prefix = output_prefix or os.path.splitext(lilypond_filename)[0]
    if output_prefix[-1:] == '/':
        output_prefix += 'lilypond'

    typeset_results = lilypond(lilypond_filename, output_prefix, pdf=pdf, png=png, ps=ps)

    concatenated_image = output_prefix + '_concat.png'
    png_concatenation = png_concatenation or PNGConcatenation()
    png_concatenation.concatenate(typeset_results.png_list, concatenated_image)

    wav_list = []
    mp3_list = []
    ogg_list = []

    if sound_font:
        for midi_file in typeset_results.midi_list:
            wav_file = os.path.splitext(midi_file)[0] + '.wav'
            midi_to_wav(midi_file, wav_file, sound_font)
            wav_list.append(wav_file)

            if mp3:
                mp3_file = os.path.splitext(midi_file)[0] + '.mp3'
                wav_to_mp3(wav_file, mp3_file)
                mp3_list.append(mp3_file)

            if ogg:
                ogg_file = os.path.splitext(midi_file)[0] + '.ogg'
                wav_to_ogg(wav_file, ogg_file)
                ogg_list.append(ogg_file)

    return ConvertLilypondResults(typeset_results,  concatenated_image, wav_list, mp3_list, ogg_list)


class ConvertLilypondResults(object):

    def __init__(self, typeset_results, concatenated_png, wav_list, mp3_list, ogg_list):
        """The output object from converting a lilypond file to the most common outputs.

        Args:
            typeset_results (TypesetResults): the original typeset results
            concatenated_png (str): the location of the concatenated png file
            wav_list (list of str): the location of the wav files
            mp3_list (list of str): the location of the mp3 files
            ogg_list (list of str): the location of the ogg files
        """
        self.typeset_results = typeset_results
        self.concatenated_png = concatenated_png
        self.wav_list = wav_list
        self.mp3_list = mp3_list
        self.ogg_list = ogg_list

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
