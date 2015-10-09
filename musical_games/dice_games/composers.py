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

    def get_music_works(self):
        """Get the musical works from this composer.

        Returns:
            list of MusickWork: the list of musical works we support
        """
        pass


class Kirnberger(ComposerInfo):

    @property
    def name(self):
        return 'Kirnberger'

    @property
    def id(self):
        return 'kirnberger'

    def get_music_works(self):
        return [KirnbergerMenuetTrioInfo(), KirnbergerPolonaiseInfo()]


class Stadler(ComposerInfo):

    @property
    def name(self):
        return 'Stadler'

    @property
    def id(self):
        return 'stadler'

    def get_music_works(self):
        return [StadlerMenuetTrioInfo()]


class Mozart(ComposerInfo):

    @property
    def name(self):
        return 'Mozart'

    @property
    def id(self):
        return 'mozart'

    def get_music_works(self):
        return [MozartWaltzInfo()]


composers = [Kirnberger(), Stadler(), Mozart()]




