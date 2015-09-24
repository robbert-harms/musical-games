from musical_games.converters.utils import run_command, ensure_dir_exists

__author__ = 'Robbert Harms'
__date__ = "2015-09-22"
__maintainer__ = "Robbert Harms"
__email__ = "robbert.harms@maastrichtuniversity.nl"


def trim_image(image_fname):
    """Trim the given images.

    Args:
        image_fname: the image to trim
    """
    run_command('convert -trim {0} {0}'.format(image_fname))
    return image_fname


def concatenate_images(output_fname, image_list):
    """Append all the given files to each other in the order given.

    Args:
        output_fname (str): the output filename
        image_list (list of str): the filenames of the images to append
    """
    ensure_dir_exists(output_fname)
    run_command('convert -append {inputs} {output}'.format(inputs=' '.join(image_list), output=output_fname))