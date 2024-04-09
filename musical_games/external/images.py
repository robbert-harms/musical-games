__author__ = 'Robbert Harms'
__date__ = "2015-09-22"
__maintainer__ = "Robbert Harms"
__email__ = "robbert@xkls.nl"

from pathlib import Path

from musical_games.external.exceptions import MissingDependencyError
from musical_games.external.utils import run_command, bash_function_exists


def trim_image(image_in: Path, image_out: Path | None = None) -> Path:
    """Trim the given images.

    Args:
        image_in: the image to trim
        image_out: the output image, if not set it defaults to the input image

    Returns:
        The path to the output image.
    """
    if not bash_function_exists('convert'):
        raise MissingDependencyError('The function convert does not exists, '
                                     'please install ImageMagick or some similar tool.')

    image_out = image_out or image_in
    image_out.parent.mkdir(parents=True, exist_ok=True)
    run_command(['convert', '-trim', str(image_in), str(image_out)])
    return image_out
