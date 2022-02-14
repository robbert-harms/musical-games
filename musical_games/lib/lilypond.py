import os
import subprocess

__author__ = 'Robbert Harms'
__date__ = "2015-09-22"
__maintainer__ = "Robbert Harms"
__email__ = "robbert.harms@maastrichtuniversity.nl"


def lilypond(lilypond_fname, output, pdf=True, png=True, ps=False):
    """Typeset music and/or produce midi from file.

    This runs the shell command lilypond to on the inputs. Note that Midi output needs to be defined in the lilypond
    file and can not be set on the command line.

    Args:
        lilypond_fname (Path or str): the location of the lilypond file to convert.
        output (str): the location for the output files, suffixes will be added.
        pdf (bool): if we want pdf output
        png (boolean): if we want png output
        ps (boolean): if we want postscript output

    Raises:
        RuntimeError: if the compilation of the lilypond file failed somehow.

    Returns:
        TypesetResults: the result set with the location of the output files.
    """
    if not os.path.isdir(os.path.dirname(output)):
        os.makedirs(os.path.dirname(output))

    command = ['lilypond']
    if pdf:
        command.append('--pdf')
    if png:
        command.append('--png')
    if ps:
        command.append('--ps')
    command.extend(['-o', output, lilypond_fname])

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    std_err = process.communicate()[1]
    rc = process.returncode

    if rc == 1:
        raise RuntimeError('Error converting lilypond file. Error message: ' + str(std_err))

    pdf_list = [output + '.pdf'] if pdf else []
    png_list = _get_png_list(output, png)
    ps_list = [output + '.ps'] if ps else []
    midi_list = _get_midi_list(output)

    return TypesetResults(pdf_list, png_list, ps_list, midi_list)


class TypesetResults(object):

    def __init__(self, pdf_list, png_list, ps_list, midi_list):
        """Result set for the output of the lilypond function.

        Args:
            pdf_list (list of str): the locations of the output pdf files
            png_list (list of str): the locations of the png files
            ps_list (list of str): the locations of the ps files
            midi_list (list of str): the locations of the midi files
        """
        self.pdf_list = pdf_list
        self.png_list = png_list
        self.ps_list = ps_list
        self.midi_list = midi_list


def _get_png_list(output, png_enabled):
    if png_enabled:
        png_list = []
        if os.path.isfile(output + '.png'):
            png_list.append(output + '.png')

        i = 1
        while os.path.isfile(output + '-page{}.png'.format(i)):
            png_list.append(output + '-page{}.png'.format(i))
            i += 1
        return png_list
    return []


def _get_midi_list(output):
    midi_list = []
    if os.path.isfile(output + '.midi'):
        midi_list.append(output + '.midi')

    i = 1
    while os.path.isfile(output + '-{}.midi'.format(i)):
        midi_list.append(output + '-{}.midi'.format(i))
        i += 1

    return midi_list
