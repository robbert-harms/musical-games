from musical_games.dice_games.factory import DiceGameFactory

__author__ = 'Robbert Harms'
__date__ = "2015-10-16"
__maintainer__ = "Robbert Harms"
__email__ = "robbert.harms@maastrichtuniversity.nl"


class CompositionsCompleter(object):

    def __call__(self, prefix, parsed_args, **kwargs):
        composer = parsed_args.composer
        if composer:
            factory = DiceGameFactory()
            return factory.get_compositions(composer)
        return []


class InstrumentsCompleter(object):

    def __call__(self, prefix, parsed_args, **kwargs):
        composer = parsed_args.composer
        composition = parsed_args.composition

        if composer and composition:
            factory = DiceGameFactory()
            instruments = factory.get_instruments(composer, composition)

            l = []
            for instrument_list in instruments:
                l.extend(instrument_list)
            return list(set(l))

        return []
