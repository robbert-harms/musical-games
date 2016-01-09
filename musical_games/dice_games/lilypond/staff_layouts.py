from musical_games.utils import correct_indent

__author__ = 'Robbert Harms'
__date__ = "2016-01-04"
__maintainer__ = "Robbert Harms"
__email__ = "robbert.harms@maastrichtuniversity.nl"


class StaffInfo(object):

    def __init__(self, music_block, instrument_name, options_block=''):
        """This contains enough information about one staff in order to typeset it.

        Args:
            music_block (str): the block containing the music for this staff
            instrument_name (str): the name of this instrument, needed for display
            options_block (str): the optional options block
        """
        self.music_block = music_block
        self.instrument_name = instrument_name
        self.options_block = options_block

    def typeset_staff(self, display_instrument_name=False):
        """Typeset this staff

        Args:
            display_instrument_name (str): if we want to display the instrument name or not

        Returns:
            str: the typeset staff
        """
        instrument = ''
        if display_instrument_name:
            instrument = '\set Staff.instrumentName = #"{} "'.format(self.instrument_name)

        return correct_indent(r'''
            \new Staff
            <<
            {instrument}
            {options}
            {music}
            >>
        ''', 0).format(instrument=correct_indent(instrument, 4),
                       options=correct_indent(self.options_block, 4),
                       music=correct_indent(self.music_block, 4))


class StaffLayout(object):

    def typeset_staffs(self, staff_info_list):
        """Typeset the given staffs.

        This will typeset the given staffs according to a specific staff layout. For example, in lilypond we can
        combine two staffs using a piano staff. Also, lilypond allows nesting staffs, mixing staffs, etc. This is all
        taken care of by staff layouts.

        Args:
            staff_info_list (list of StaffInfo): the list of staff info to use for rendering

        Returns:
            str: the rendered staffs
        """


class PianoLayout(StaffLayout):

    def typeset_staffs(self, staff_info_list):
        staffs = '\n'.join([s.typeset_staff(False) for s in staff_info_list])

        return correct_indent(correct_indent(r'''
            \new PianoStaff
            <<
            {staffs}
            >>
            \layout {{
                indent = 0\mm
            }}
        ''', 0).format(staffs=correct_indent(staffs, 4)), 16)


class SimpleNamedLayout(StaffLayout):

    def typeset_staffs(self, staff_info_list):
        staffs = '\n'.join([s.typeset_staff(True) for s in staff_info_list])
        return correct_indent(correct_indent(r'''
            <<
            {staffs}
            >>
        ''', 0).format(staffs=correct_indent(staffs, 4)), 16)


class SimpleWithPianoLayout(StaffLayout):

    def typeset_staffs(self, staff_info_list):
        layout = '\n<<'

        former_is_piano = False

        for staff_info in staff_info_list:
            is_piano_staff = 'piano' in staff_info.instrument_name.lower()

            if is_piano_staff and not former_is_piano:
                layout += '\\new PianoStaff <<'
                layout += r'\set PianoStaff.instrumentName = #"Piano"'

            layout += correct_indent(staff_info.typeset_staff(display_instrument_name=not is_piano_staff), 4)

            if former_is_piano:
                layout += '>>'
                former_is_piano = False
            else:
                if is_piano_staff:
                    former_is_piano = True

        layout += '\n>>'
        return correct_indent(layout, 16)


class AutoLayout(StaffLayout):

    def typeset_staffs(self, staff_info_list):
        if self._all_piano(staff_info_list):
            return PianoLayout().typeset_staffs(staff_info_list)

        if self._has_piano(staff_info_list):
            return SimpleWithPianoLayout().typeset_staffs(staff_info_list)

        return SimpleNamedLayout().typeset_staffs(staff_info_list)

    def _has_piano(self, staff_info_list):
        previous_piano = False
        for staff_info in staff_info_list:
            if 'piano' in staff_info.instrument_name.lower():
                if previous_piano:
                    return True
                previous_piano = True
        return False

    def _all_piano(self, staff_info_list):
        return all('piano' in staff_info.instrument_name.lower() for staff_info in staff_info_list)
