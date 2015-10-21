from musical_games.dice_games.compositions import KirnbergerMenuetTrioInfo, KirnbergerPolonaiseInfo, \
    StadlerMenuetTrioInfo, MozartWaltzInfo

__author__ = 'Robbert Harms'
__date__ = "2015-09-18"
__maintainer__ = "Robbert Harms"
__email__ = "robbert.harms@maastrichtuniversity.nl"


class ComposerInfo(object):

    @property
    def name(self):
        """The name of this composer.

        Returns:
            str: the name of this composer
        """
        return ''

    @property
    def id(self):
        """Get a id of this composer. This should only contain alphanumeric signs and underscore.

        Returns:
            str: the id key of this composer.
        """
        return ''

    def get_compositions_info(self):
        """Get the information about the compositions from this composer.

        Returns:
            list of CompositionInfo: the list of musical compositions this object supports
        """
        return ()

    def get_composition_info_by_id(self, composition_id):
        """Get composition info by id key.

        This searches the list of compositions for the composition information object that matches the given id.

        Args:
            composition_id (str): the composition id

        Returns:
            CompositionInfo: the composition information object for the requested composer.

        Raises:
            ValueError: if the given composition info object could not be found.
        """
        for composition_info in self.get_compositions_info():
            if composition_info.id == composition_id:
                return composition_info
        raise ValueError('The composition information for id {} could not be found.'.format(composition_id))


class Kirnberger(ComposerInfo):

    @property
    def name(self):
        return 'Kirnberger'

    @property
    def id(self):
        return 'kirnberger'

    def get_compositions_info(self):
        return [KirnbergerMenuetTrioInfo(), KirnbergerPolonaiseInfo()]


class Stadler(ComposerInfo):

    @property
    def name(self):
        return 'Stadler'

    @property
    def id(self):
        return 'stadler'

    def get_compositions_info(self):
        return [StadlerMenuetTrioInfo()]


class Mozart(ComposerInfo):

    @property
    def name(self):
        return 'Mozart'

    @property
    def id(self):
        return 'mozart'

    def get_compositions_info(self):
        return [MozartWaltzInfo()]


composers = [Kirnberger(), Stadler(), Mozart()]


def get_composer_info_by_id(composer_id):
    """Get a composer by id key.

    This searches the list of composers for the composer that matches the given id.

    Args:
        composer_id (str): the composer id

    Returns:
        ComposerInfo: the composer information object for the requested composer.

    Raises:
        ValueError: if the given composer could not be found.
    """
    for composer in composers:
        if composer.id == composer_id:
            return composer
    raise ValueError('The composer with the id {} could not be found.'.format(composer_id))



