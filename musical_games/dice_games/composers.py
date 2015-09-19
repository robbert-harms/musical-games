from musical_games.dice_games.compositions import KirnbergerMenuetTrio, KirnbergerPolonaise, StadlerMenuetTrio, \
    MozartWaltz

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
    def safe_name(self):
        """Get a safe name of this composer. This should only contain alphanumeric signs and underscore.

        Returns:
            str: the safe name of this composer.
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
    def safe_name(self):
        return 'kirnberger'

    def get_music_works(self):
        return [KirnbergerMenuetTrio(), KirnbergerPolonaise()]


class Stadler(ComposerInfo):

    @property
    def name(self):
        return 'Stadler'

    @property
    def safe_name(self):
        return 'stadler'

    def get_music_works(self):
        return [StadlerMenuetTrio()]


class Mozart(ComposerInfo):

    @property
    def name(self):
        return 'Mozart'

    @property
    def safe_name(self):
        return 'mozart'

    def get_music_works(self):
        return [MozartWaltz()]


composers = [Kirnberger(), Stadler(), Mozart()]




