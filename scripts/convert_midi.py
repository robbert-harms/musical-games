import glob
import os
import re
import collections

from musical_games.converters.utils import run_command

__author__ = 'Robbert Harms'
__date__ = "2016-01-02"
__maintainer__ = "Robbert Harms"
__email__ = "robbert.harms@maastrichtuniversity.nl"


def extract_channel_name(channel_str):
    """Extract from the given channel string the track name

    Args:
        channel_str (str): the channel string as extracted by for example 'extract_channels'.
            It should look like for example:
            'trackBchannelB = {a\\'16 cis\\'\\' e\\'\\' a\\'\\' a\\'\\'8 e\\'\\' cis\\'\\' a\\'  | % 2}'

    Returns:
        str: the channel name from the given string. Assuming the example, it returns 'trackBchannelB'
    """
    return re.findall(r'track\w+', channel_str)[0].strip()


def extract_track_key(channel_name):
    """Extract the track key from the channel name.

    This assumes that the channel name is formatted like "track[track_key]channel[channel_key]"

    Args:
        channel_name (str): the channel name

    Returns:
        str: the key to the channel (normally a single letter)
    """
    return channel_name[5:6]


def extract_instrument_name(channel_str):
    """Given a channel string containing the instrument name, extract that instrument name.

    An example of an input string is:
        'trackBchannelA = {\\set Staff.instrumentName = "Sopran"}'
    From which we will return 'Sopran'.

    Args:
        channel_str (str): the channel from which to extract the instrument name

    Returns:
        str: the instrument name in the given channel
    """
    return re.search(r'instrumentName\s=\s\"(\w+)\"', channel_str).group(1).strip()


def extract_music_expression(channel_str):
    """Extract the music expression and voice number from the given string.

    This expects a channel string with something like:
        trackDchannelB = {
          \voiceOne
          a'8. cis''16 e'' a'' gis'' b'' e'8 cis'
          | % 2

        }

    The voice is optional and if present will be matched.

    Args:
        channel_str (str): the channel from which to extract the music expression and voice number

    Returns:
        tuple: boolean, int, string: the first boolean indicates if there is a voice indication present, the second
            is the voice number (if a voice is present), the last is the music expression
    """
    match = re.search(r'{\s*(\\voice(One|Two))?([^\}]*)}', channel_str)

    has_voice = match.group(1) is not None
    voice_nmr = None
    if has_voice:
        voice_nmr = 1 if match.group(2).strip() == 'One' else 2

    music_expr = match.group(3).strip()

    return has_voice, voice_nmr, music_expr


def remove_comments(music_expr_line):
    """Remove all comments from the given line of lilypond music expr

    Args:
        music_expr_line (str): a single line of a music expression.

    Returns:
        str: the music expression line without the comments
    """
    pos = music_expr_line.find('%')
    if pos >= 0:
        return music_expr_line[0:pos]
    return music_expr_line


def remove_durations_in_chords(music_expr):
    """Remove the absolute durations within chord signs: < and >

    Args:
        music_expr (str): the music expression

    Returns:
        str: the same music expression but with the durations removed from within chords.
    """
    cleaned = ''

    in_chord = False
    in_timing = False

    for char in music_expr:
        if char == '<':
            in_chord = True
            cleaned += char
        elif char == '>':
            in_chord = False
            in_timing = False
            cleaned += char
        else:
            if not in_chord:
                cleaned += char
            else: # in chord
                if in_timing:
                    if char.isalpha() or char == ' ':
                        in_timing = False
                        cleaned += char
                else:
                    if char.isdigit():
                        in_timing = True
                    else:
                        cleaned += char
    return cleaned


def clean_music_expr(music_expr):
    """Clean the given music expression by removing all comments, bars, double spaces, tabs and new lines.

    Args:
        music_expr (str): the music expression. Example: "a'8. cis''16 e'' a'' gis'' b'' e'8 cis' | % 2"

    Returns:
        str: the music expression without all redundant information.
    """
    cleaned = ''

    for line in music_expr.split('\n'):
        cleaned += remove_comments(line)

    cleaned = cleaned.replace('|', '')
    cleaned = cleaned.replace('\t', '')
    cleaned = remove_durations_in_chords(cleaned)

    while cleaned.find('  ') >= 0:
        cleaned = cleaned.replace('  ', ' ')

    return cleaned.strip()


def extract_channels(lilypond_file):
    """From the given lilypond file, extract all channel blocks present.

    Args:
        lilypond_file (str): the lilypond file from which to extract the channels

    Returns:
        list: the list of channel strings
    """
    p = re.compile(r'track[\w\s=\\]*\s+\{[^\}]*}')
    with open(lilypond_file, 'r') as f:
        info = f.read()
        return re.findall(p, info)


def autodict():
    return collections.defaultdict(autodict)


def extract_tracks(lilypond_file):
    channel_strings = extract_channels(lilypond_file)

    tracks = autodict()
    for channel in channel_strings:
        if r'\time' not in channel:

            track_key = extract_track_key(extract_channel_name(channel))

            if 'instrumentName' in channel:
                tracks[track_key]['instrument'] = extract_instrument_name(channel)
            else:
                has_voice, voice_nmr, music_expr = extract_music_expression(channel)
                music_expr = clean_music_expr(music_expr)

                if has_voice:
                    tracks[track_key]['music_expr'].update({voice_nmr: music_expr})
                else:
                    tracks[track_key]['music_expr'] = music_expr

    per_instrument = {}
    for info in tracks.values():
        per_instrument[info['instrument']] = info['music_expr']
    return per_instrument


def midi_to_lilypond(midi_fname, output_fname=None, overwrite=False):
    """Convert the given midi file to a lilypond source file.

    This uses the command midi2ly with the absolute pitches and explicit durations flag.
    Afterwards it will remove all utf-8 from the source file.

    Args:
        midi_fname (str): the filename of the midi file
        output_fname (str): the output lilypond file if None we use the basename of the midi file
        overwrite (boolean): if we overwrite the lilypond file if it already exists

    Returns:
        str: the path to the lilypond source file
    """
    output_fname = output_fname or os.path.splitext(midi_fname)[0] + '.ly'

    if overwrite:
        if os.path.isfile(output_fname):
            os.remove(output_fname)
    else:
        if os.path.isfile(output_fname):
            return output_fname

    run_command(['midi2ly', '-a', '-e', '-o', output_fname, midi_fname])
    run_command(['iconv', '-f', 'utf-8', '-t', 'utf-8', '-c', output_fname, '-o', output_fname])

    return output_fname


def get_per_file_staffs(folder):
    per_file = {}
    for item in glob.glob(folder + '/*.mid'):
        bname = os.path.basename(item)

        lilypond_file = midi_to_lilypond(item)
        channel_info = extract_tracks(lilypond_file)

        filename = os.path.splitext(bname)[0]
        per_file[filename] = channel_info
    return per_file


def read_file_names_indices_order(folder):
    with open(folder + '/file_names_sorted.txt', 'r') as f:
        filenames = f.readlines()
    return list(map(lambda s: s.strip(), filenames))


folder = '/tmp/Kirnberger polonaise midinaamcorrectie/'
per_file = get_per_file_staffs(folder)
bars_order = read_file_names_indices_order(folder)
instrument_names = ['Sopran', 'Alt', 'Tenor', 'Ba']
file_renames = ['violin_1', 'violin_2', 'piano_1', 'piano_2']

output_lists = {instr: [] for instr in instrument_names}

for ind, bar_name in enumerate(bars_order):
    for instrument in instrument_names:
        output_lists[instrument].append(per_file[bar_name][instrument])

for instrument_name, bars in output_lists.items():
    output_name = folder + '/' + instrument_name

    with open(output_name, 'w') as f:
        for ind, bar in enumerate(bars):
            f.write('"{}"'.format(ind + 1))

            if isinstance(bar, dict):
                for b in bar.values():
                    f.write(',"{}"'.format(b))
            else:
                f.write(',"{}"'.format(bar))
            f.write('\n')


for ind, instr in enumerate(instrument_names):
    print(folder + '/' + file_renames[ind] + '.txt')
    os.rename(folder + '/' + instr, folder + '/' + file_renames[ind] + '.txt')
