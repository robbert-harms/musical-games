__author__ = 'Robbert Harms'
__date__ = "2015-10-22"
__maintainer__ = "Robbert Harms"
__email__ = "robbert.harms@maastrichtuniversity.nl"


class StaffAnnotator(object):

    def annotate_begin(self):
        """Return the annotations for at the beginning of the piece.

        Returns:
            str: lilypond code for the annotations at the beginning of the piece.
        """
        return ''

    def annotate_end(self):
        """Return the annotations for at the end of the piece.

        Returns:
            str: lilypond code for the annotations at the end of the piece.
        """
        return ''


class NoOptAnnotator(StaffAnnotator):
    pass


class FineAtEnd(StaffAnnotator):

    def annotate_end(self):
        return '\\once \\override Score.RehearsalMark #\'self-alignment-X = #right ' \
               r'\mark \markup {\fontsize #-1 \italic "Fine"}'


class DaCapoAtEnd(StaffAnnotator):

    def annotate_end(self):
        return '\\once \\override Score.RehearsalMark #\'self-alignment-X = #right ' \
               r'\mark \markup {\fontsize #-1 \italic "D.C. al Fine"}'
