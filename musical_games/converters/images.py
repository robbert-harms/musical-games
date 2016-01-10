from musical_games.converters.utils import run_command, ensure_dir_exists, bash_function_exists

__author__ = 'Robbert Harms'
__date__ = "2015-09-22"
__maintainer__ = "Robbert Harms"
__email__ = "robbert.harms@maastrichtuniversity.nl"


def trim_image(image_fname, output_fname=None):
    """Trim the given images.

    Args:
        image_fname: the image to trim
        output_fname: the output image, if not set it defaults to the input image

    Returns:
        str: the name of the output image
    """
    if not bash_function_exists('convert'):
        raise RuntimeError('The function convert does not exists, please install ImageMagick or some similar tool.')

    output_fname = output_fname or image_fname
    run_command(['convert', '-trim', image_fname, output_fname])
    return output_fname


def draw_rectangle(image_fname, fill_color, stroke_color, stroke_width, position, end_position, output_fname=None):
    """Draw a rectangle on a given image.

    Args:
        image_fname: the image to draw on
        fill_color (str): the imagemagick color to use for filling
        stroke_color (str): the imagemagick color for the border
        stroke_width (int): the width fo the stroke
        position (tuple): the x,y position of the top-left of the rectangle
        end_position (tuple): the x,y end position of the rectangle to draw
        output_fname: the output image, if not set it defaults to the input image

    """
    if not bash_function_exists('convert'):
        raise RuntimeError('The function convert does not exists, please install ImageMagick or some similar tool.')

    output_fname = output_fname or image_fname

    command = ['convert', '-quality', '100', '-fill', fill_color, '-stroke', stroke_color,
               '-strokewidth', str(stroke_width),
               '-draw', 'rectangle ' + ','.join(map(str, position)) + ' ' + ','.join(map(str, end_position)),
               image_fname, output_fname]
    run_command(command)

    return image_fname


def get_image_size(image_fname):
    """Get the size of the given image.

    Args:
        image_fname (str): the image we want to get the width and height of

    Returns:
        tuple: width, height of the given image
    """
    if not bash_function_exists('identify'):
        raise RuntimeError('The function convert does not exists, please install ImageMagick or some similar tool.')
    value = run_command(['identify', '-format', '%[fx:w]x%[fx:h]', image_fname]).decode("utf-8")
    return list(map(int, value.split('x')))


def concatenate_images(output_fname, image_list):
    """Append all the given files to each other in the order given.

    Args:
        output_fname (str): the output filename
        image_list (list of str): the filenames of the images to append
    """
    if not bash_function_exists('convert'):
        raise RuntimeError('The function convert does not exists, please install ImageMagick or some similar tool.')

    ensure_dir_exists(output_fname)
    command = ['convert', '-append']
    command.extend(image_list)
    command.append(output_fname)
    run_command(command)
