__author__ = 'Robbert Harms'
__date__ = "2016-02-06"
__maintainer__ = "Robbert Harms"
__email__ = "robbert.harms@maastrichtuniversity.nl"


class BarConverter(object):
    """Bar converters are used when rendering a given bar for use the AllBarsConcatenated typesetter"""

    def convert(self, bar):
        """Convert the given bar to a string.

        Args:
            bar (Bar): the bar to convert to string

        Returns:
            str: the bar converted to a string
        """


class SimpleBarConverter(BarConverter):
    """Simply converts the Bar object to a string"""

    def convert(self, bar):
        return str(bar)


class MozartBarConverter(BarConverter):
    """Converts the two repeats bar to a single bar with two voices"""

    def convert(self, bar):
        if bar.alternatives:
            return r'<< {\voiceOne ' + str(bar.alternatives[0]) + r'} \new Voice { \voiceTwo ' + str(bar) + '} >>'
        return str(bar)

