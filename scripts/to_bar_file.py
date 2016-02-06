import os

__author__ = 'Robbert Harms'
__date__ = "2016-02-06"
__maintainer__ = "Robbert Harms"
__email__ = "robbert.harms@maastrichtuniversity.nl"


def convert_to_bar_file(input_measures_fname, output_fname=None):
    """Convert the input measures file (one line per measure) to a file suitable for musical games.

    This will enclose every line in the measure file with "" and prepend the line number to it. For example, if
    you have the file with the following lines:
        e''4 g'' e'' c''
        r8 e''8 g'' [f''] e'' [g''] e'' c''

    It will convert it to:
        "1","e''4 g'' e'' c''"
        "2","r8 e''8 g'' [f''] e'' [g''] e'' c''"

    Which can be used in musical games for the information about one instrument.

    Args:
        input_measures_fname (str): the file name of the input file
        output_fname (str): the output file name, if not given the input file is overwritten
    """
    output_fname = output_fname or input_measures_fname

    with open(input_measures_fname, 'r') as f:
        lines = f.readlines()

    result = []
    for ind, line in enumerate(lines):
        result.append('"{ind}","{line}"\n'.format(ind=ind + 1, line=line.strip()))

    with open(output_fname, 'w') as f:
        f.writelines(result)


convert_to_bar_file('/tmp/bach/left_hand.txt')
convert_to_bar_file('/tmp/bach/right_hand.txt')
