import tempfile
from musical_games.lib.utils import run_command, bash_function_exists, ensure_dir_exists, remove_file_if_exists

__author__ = 'Robbert Harms'
__date__ = "2015-09-22"
__maintainer__ = "Robbert Harms"
__email__ = "robbert.harms@maastrichtuniversity.nl"


def midi_to_wav(midi_fname, wav_fname, soundfont, gain=None):
    """Tries to autodetect the available midi converter and uses the best one found.

    Args:
        midi_fname (Path): the location of the midi file
        wav_fname (Path): where to place the output wav file.
        soundfont (Path): the path to the sound font file.
        gain (float): number between 0 and 1 to indicate the desired output gain.
    """
    converter = _get_first_available_converter([FluidSynth(soundfont, gain=gain),
                                                Timidity(soundfont, gain=gain)])
    converter.convert(midi_fname, wav_fname)


def wav_to_mp3(wav_fname, mp3_fname):
    """Tries to autodetect the available wav converter and uses the best one found.

    Args:
        wav_fname (Path): where to place the output wav file.
        mp3_fname (Path): the path to the output mp3 file
    """
    converter = _get_first_available_converter([FFMpeg(), AVConv()])
    converter.to_mp3(wav_fname, mp3_fname)


def wav_to_ogg(wav_fname, ogg_fname):
    """Tries to autodetect the available wav converter and uses the best one found.

    Args:
        wav_fname (Path): where to place the output wav file.
        ogg_fname (Path): the path to the output mp3 file
    """
    converter = _get_first_available_converter([FFMpeg(), AVConv()])
    converter.to_ogg(wav_fname, ogg_fname)


def _get_first_available_converter(converters):
    converters = [c for c in converters if c.is_available()]
    if not len(converters):
        raise RuntimeError('No suitable converter found.')
    return converters[0]


class MidiToWav(object):

    def __init__(self, soundfont, gain=None):
        """Create a new converter to convert midi to wav.

        Args:
            soundfont (Path): the path to the sound font to use.
            gain (float): number between 0 and 1 to indicate the desired output gain. May not be implemented.
        """
        self._soundfount = soundfont
        self.gain = gain or 0.1

    def convert(self, midi_fname, wav_fname):
        """Convert the given midi file to a wav file at the given location.

        Args:
            midi_fname (Path): the location of the midi file
            wav_fname (Path): where to place the output wav file.
        """

    def is_available(self):
        """Check if the implementing method is available.

        Returns:
            bool: if this method is available
        """


class FluidSynth(MidiToWav):

    def convert(self, midi_fname, wav_fname):
        ensure_dir_exists(wav_fname)
        run_command(['fluidsynth', '-g', str(self.gain*10), '-F', wav_fname, self._soundfount, midi_fname])

    def is_available(self):
        return bash_function_exists('fluidsynth')


class Timidity(MidiToWav):

    def convert(self, midi_fname, wav_fname):
        ensure_dir_exists(wav_fname)

        with tempfile.NamedTemporaryFile('w') as tmp_file:
            tmp_file.write('soundfont {}'.format(self._soundfount))
            tmp_file.flush()
            run_command(['timidity', '-c', tmp_file.name, '--output-24bit', '-A120', '-Ow', '-o',
                         wav_fname, midi_fname])

    def is_available(self):
        return bash_function_exists('timidity')


class WavConverter(object):
    """Converter for converting wav to any other media format."""

    def to_mp3(self, wav_fname, output_fname):
        """Convert the given wav file to an mp3 file.

        Args:
            wav_fname (Path): the wav filename
            output_fname (Path): the output file
        """

    def to_ogg(self, wav_fname, output_fname):
        """Convert the given wav file to an ogg file.

        Args:
            wav_fname (Path): the wav filename
            output_fname (Path): the output file
        """

    def is_available(self):
        """Check if the implementing method is available.

        Returns:
            bool: if this method is available
        """


class FFMpegLike(WavConverter):

    def __init__(self, command_name):
        self.command_name = command_name

    def to_mp3(self, wav_fname, output_fname):
        ensure_dir_exists(output_fname)
        remove_file_if_exists(output_fname)
        run_command([self.command_name, '-i', wav_fname, '-vn', '-ar', '44100',
                     '-ac', '2', '-ab', '192k', '-f', 'mp3', output_fname])

    def to_ogg(self, wav_fname, output_fname):
        ensure_dir_exists(output_fname)
        remove_file_if_exists(output_fname)
        run_command([self.command_name, '-i', wav_fname, '-acodec', 'libvorbis', output_fname])

    def is_available(self):
        return bash_function_exists(self.command_name)


class FFMpeg(FFMpegLike):

    def __init__(self):
        super(FFMpeg, self).__init__('ffmpeg')


class AVConv(FFMpegLike):

    def __init__(self):
        super(AVConv, self).__init__('avconv')
