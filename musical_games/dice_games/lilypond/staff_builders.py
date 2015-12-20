__author__ = 'Robbert Harms'
__date__ = "2015-10-08"
__maintainer__ = "Robbert Harms"
__email__ = "robbert.harms@maastrichtuniversity.nl"


class StaffTypeset(object):

    def __init__(self, bars_lists):
        """Typeset the given list of bar lists

        Args:
            bars_lists (list of list of Bar): the list of Bars we will typeset
        """
        self.bars_lists = bars_lists

    def typeset(self):
        """Get the typeset music expression for the given Bars

        Returns:
            list of str: per list of Bars one typeset music expression
        """


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

    def convert(self, bar):
        return str(bar)


class MozartBarConverter(BarConverter):

    def convert(self, bar):
        if bar.alternatives:
            return r'<< {\voiceOne ' + str(bar.alternatives[0]) + r'} \new Voice { \voiceTwo ' + str(bar) + '} >>'
        return str(bar)


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


class NoneAnnotator(StaffAnnotator):
    pass


class FineAtEnd(StaffAnnotator):

    def annotate_end(self):
        return '\\once \\override Score.RehearsalMark #\'self-alignment-X = #right ' \
               r'\mark \markup {\fontsize #-1 \italic "Fine"}'


class DaCapoAtEnd(StaffAnnotator):

    def annotate_end(self):
        return '\\once \\override Score.RehearsalMark #\'self-alignment-X = #right ' \
               r'\mark \markup {\fontsize #-1 \italic "D.C. al Fine"}'


class AllBarsConcatenated(StaffTypeset):

    def __init__(self, bars_lists, bar_converter):
        """Typeset the given list of bar lists

        Args:
            bars_lists (list of list of Bar): the list of Bars we will typeset
            bar_converter (BarConverter): the bar converter to use for the conversions
        """
        super(AllBarsConcatenated, self).__init__(bars_lists)
        self.bar_converter = bar_converter

    def typeset(self):
        music_expressions = []
        for bar_list in self.bars_lists:
            music_expressions.append("\n".join(self.bar_converter.convert(bar) for bar in bar_list) + r' \bar "|."')
        return music_expressions


class WithRepeat(StaffTypeset):

    def __init__(self, bars_lists, repeats, staff_annotator):
        """Typeset all the bars with the necessary repeats.

        Args:
            bars_lists (list of list of Bar): the list of Bars we will typeset
            repeats (list of tuples of int): the bars we repeat. For example: [(0, 8), (8, 16)] indicates
                two repeats, one in which 0 to 8 is repeated and one in which 8 to 16 is repeated.
            staff_annotator (StaffAnnotator): the staff annotator to use for annotating the staff
        """
        super(WithRepeat, self).__init__(bars_lists)
        self.repeats = repeats
        self.staff_annotator = staff_annotator

    def typeset(self):
        nmr_staffs = len(self.bars_lists)
        nmr_bars = len(self.bars_lists[0])

        result_staffs = [[] for i in range(nmr_staffs)]
        result_staffs[-1].append(self.staff_annotator.annotate_begin())

        to_repeat = [[] for i in range(nmr_staffs)]
        in_repeat = False

        for bar_ind in range(nmr_bars):
            begin_of_repeat = any(bar_ind == repeat[0] for repeat in self.repeats)
            end_of_repeat = any(bar_ind == repeat[1] for repeat in self.repeats)

            if end_of_repeat:
                in_repeat = False
                self._render_repeats(result_staffs, to_repeat)
                to_repeat = [[] for i in range(nmr_staffs)]

            if begin_of_repeat:
                in_repeat = True

            if in_repeat:
                for staff_ind, bar_list in enumerate(self.bars_lists):
                    to_repeat[staff_ind].append(bar_list[bar_ind])
            else:
                for staff_ind, bar_list in enumerate(self.bars_lists):
                    result_staffs[staff_ind].append(str(bar_list[bar_ind]))

        repeat_on_last = False
        if in_repeat:
            self._render_repeats(result_staffs, to_repeat)
            repeat_on_last = True

        result_staffs[-1].append(self.staff_annotator.annotate_end())

        result = []
        for staff in result_staffs:
            expr = "\n".join(staff).rstrip()
            if not repeat_on_last:
                expr += r' \bar "|."'
            result.append(expr)
        return result

    def _render_repeats(self, result_staffs, to_repeat):
        for staff in result_staffs:
            staff.append(r'\repeat volta 2{')

        if any(staff[-1].alternatives for staff in to_repeat):
            for staff_ind, bars in enumerate(to_repeat):
                result_staffs[staff_ind].extend(map(str, bars[:-1]))
                result_staffs[staff_ind].append('}')

                last_bar = bars[-1]

                if last_bar.alternatives:
                    result_staffs[staff_ind].append(r'\alternative { {' + str(last_bar) + '} {' +
                                                    str(last_bar.alternatives[0]) + '} }')
                else:
                    result_staffs[staff_ind].append(r'\alternative { {' + str(last_bar) + '} {' +
                                                    str(last_bar) + '} }')
        else:
            for staff_ind, bars in enumerate(to_repeat):
                result_staffs[staff_ind].extend(map(str, bars))
                result_staffs[staff_ind].append('}')
