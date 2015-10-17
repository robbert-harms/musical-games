from musical_games.dice_games.lilypond.base import Staff

__author__ = 'Robbert Harms'
__date__ = "2015-10-08"
__maintainer__ = "Robbert Harms"
__email__ = "robbert.harms@maastrichtuniversity.nl"


class StaffBuilder(object):

    def get_staffs(self):
        """Get a list of Staffs to be used by the typesetter.

        Returns:
            list of Staff: list of staff objects to use during typesetting of a piece.
        """
        pass


class NoRepeat(StaffBuilder):

    def __init__(self, tracts_info):
        """Concatenates all bars."""
        self.tracts_info = tracts_info

    def get_staffs(self):
        staffs = []
        for tract_info in self.tracts_info:
            notes = []
            for bar in tract_info.bars:
                notes.append(self._bar_to_notes(bar))
            staffs.append(Staff("\n".join(notes) + r' \bar "|."', tract_info.clef))

        return staffs

    def _bar_to_notes(self, bar):
        return str(bar)


class SingleMeasure(StaffBuilder):

    def __init__(self, tracts_info, measure_ind):
        """Return the overview for a single bar.

        Args:
            tracts_info
            measure_ind (int): the index (from the table) of the Bar we would like to view.
                This is supposed to be 1 indiced.
        """
        self.tracts_info = tracts_info
        self.measure_ind = measure_ind

    def get_staffs(self):
        staffs = []
        for tract_info in self.tracts_info:
            notes = []
            for ind, bar in enumerate(tract_info.bars):
                if ind == self.measure_ind - 1:
                    notes.append(self._bar_to_notes(bar))
            staffs.append(Staff("\n".join(notes) + r' \bar "|."', tract_info.clef))

        return staffs

    def _bar_to_notes(self, bar):
        return str(bar)


class MozartNoRepeat(NoRepeat):
    """The no repeat listing for the Mozart Waltz.

    In the Mozart bar listing the alternative endings are superimposed on each other as two voices. We copied
    that scheme using this class.
    """
    def _bar_to_notes(self, bar):
        return mozart_superimpose_voices(bar)


class MozartSingleMeasure(SingleMeasure):
    """The single measure listing for the Mozart Waltz.

    In the Mozart bar listing the alternative endings are superimposed on each other as two voices. We copied
    that scheme using this class for the single measure case.
    """
    def _bar_to_notes(self, bar):
        return mozart_superimpose_voices(bar)


def mozart_superimpose_voices(bar):
    """Superimpose the alternative endings using voices."""
    if bar.alternatives:
        return r'<< {\voiceOne ' + str(bar.alternatives[0]) + r'} \new Voice { \voiceTwo ' + str(bar) + '} >>'
    else:
        return str(bar)


class WithRepeat(StaffBuilder):

    def __init__(self, tracts_info, measure_indices, repeat_points):
        """Concatenates all bars."""
        self.tracts_info = tracts_info
        self.measure_indices = measure_indices
        self.repeat_points = repeat_points

    def get_staffs(self):
        staffs = []

        bar_dicts = [ti.get_bars_dict() for ti in self.tracts_info]

        lines_total = [[] for i in range(len(self.tracts_info))]
        bars = [[] for i in range(len(self.tracts_info))]

        for count, measure_ind in enumerate(self.measure_indices):
            for tract_info_ind, bar_dict in enumerate(bar_dicts):
                bars[tract_info_ind].append(bar_dict[measure_ind])

            if count+1 in self.repeat_points:
                self._repeat_point(lines_total, bars)

        for ind, tract_info in enumerate(self.tracts_info):
            result_str = "\n".join(lines_total[ind])
            if bars[tract_info_ind]:
                result_str += "\n".join([self._bar_to_notes(bar) for bar in bars[ind]]) + r' \bar "|."'

            staffs.append(Staff(result_str, tract_info.clef))

        return staffs

    def _bar_to_notes(self, bar):
        return str(bar)

    def _repeat_point(self, lines_total, bars):
        if any(bars[i][len(bars[i]) - 1].alternatives for i in range(len(bars))):
            for tract_info_ind in range(len(lines_total)):
                lines_total[tract_info_ind].append(r'\repeat volta 2{')
                lines_total[tract_info_ind].extend([self._bar_to_notes(bar) for bar in bars[tract_info_ind][:-1]])
                lines_total[tract_info_ind].append('}')

                last_bar = bars[tract_info_ind][len(bars[tract_info_ind])-1]

                if last_bar.alternatives:
                    lines_total[tract_info_ind].append(r'\alternative {{' + self._bar_to_notes(last_bar) + '} {' +
                                                        self._bar_to_notes(last_bar.alternatives[0]) + '}}')
                else:
                    lines_total[tract_info_ind].append(r'\alternative {{' + self._bar_to_notes(last_bar) + '} {' +
                                                        self._bar_to_notes(last_bar) + '}}')

                bars[tract_info_ind] = []
        else:
            for tract_info_ind in range(len(lines_total)):
                lines_total[tract_info_ind].append(r'\repeat volta 2{')
                lines_total[tract_info_ind].extend([self._bar_to_notes(bar) for bar in bars[tract_info_ind]])
                lines_total[tract_info_ind].append('}')
                bars[tract_info_ind] = []