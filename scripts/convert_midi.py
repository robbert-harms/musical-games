import glob
import os
import re
import subprocess
import collections

__author__ = 'Robbert Harms'
__date__ = "2016-01-02"
__maintainer__ = "Robbert Harms"
__email__ = "robbert.harms@maastrichtuniversity.nl"


def extract_channel_name(lilypond_str):
    return re.findall(r'track\w+', lilypond_str)[0].strip()


def extract_track_key(channel_name):
    return channel_name[5:6]


def extract_instrument_name(lilypond_str):
    return re.search(r'instrumentName\s=\s\"(\w+)\"', lilypond_str).group(1).strip()


def extract_music_expression(lilypond_str):
    return re.search(r'{\s*([\s\w\'\.,\*\/\<\>]*)[\|\s\%\w]*}', lilypond_str).group(1).strip()


def extract_music_expression_with_voice(lilypond_str):
    match = re.search(r'{\s*\\voice(One|Two)\s*([\s\w\'\.,\*\/\<\>]*)[\|\s\%\w]*}', lilypond_str)
    voice = 1 if match.group(1).strip() == 'One' else 2
    expr = match.group(2).strip()
    return {voice: expr}


def autodict():
    return collections.defaultdict(autodict)


def extract_channels(lilypond_file):
    p = re.compile(r'track[\w\s=\\]*\s+\{\s+[\w\\\s\.\=\"\'\|\%,\*\/\<\>]*\s*\}')
    with open(lilypond_file, 'r') as f:
        info = f.read()
        channel_strings = re.findall(p, info)

    tracks = autodict()
    for channel in channel_strings:
        if not r'\time' in channel:

            track_key = extract_track_key(extract_channel_name(channel))

            if 'instrumentName' in channel:
                tracks[track_key]['instrument'] = extract_instrument_name(channel)
            elif 'voice' in channel:
                tracks[track_key]['music_expr'].update(extract_music_expression_with_voice(channel))
            else:
                tracks[track_key]['music_expr'] = extract_music_expression(channel)

    per_instrument = {}
    for info in tracks.values():
        per_instrument[info['instrument']] = info['music_expr']
    return per_instrument


def convert_to_ly(file_path):
    output_name = file_path + '.ly'
    if not os.path.isfile(output_name):
        print(['midi2ly', '-a', '-o', output_name, file_path])
        subprocess.call(['midi2ly', '-a', '-o', output_name, file_path])
        subprocess.call(['iconv', '-f', 'utf-8', '-t', 'utf-8', '-c', output_name, '-o', output_name])
    return output_name


def get_per_file_staffs(folder):
    per_file = {}
    for item in glob.glob(folder + '/*.mid'):
        bname = os.path.basename(item)
        print(bname)

        lilypond_file = convert_to_ly(item)
        channel_info = extract_channels(lilypond_file)

        filename = os.path.splitext(bname)[0]
        per_file[filename] = channel_info
    return per_file

folder = '/tmp/Kirnberger polonaise midinaamcorrectie/'
per_file = get_per_file_staffs(folder)
print(per_file)
