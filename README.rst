#############
Musical Games
#############
This package features an implementation of various musical dice games by Mozart, Kirnberger and Stadler.
These dice games are also known as "Musikalisches Würfelspiel" (German for "musical dice game").

The earliest printed edition of a dice game is Johann Philipp Kirnberger's "Der allezeit fertige Menuetten- und Polonaisencomponist"
(The ever-ready minuet and polonaise composer"), published in 1757.
Afterwards, many composers, such as, for example, C.P.E. Bach, Hayden, and Mozart, published these so called
"Musikalische Würfelspiele" (musical dice games) all over Europe.
The music style varies roughly between Gregorian chants up to and including the salon pieces of the Romantic period. See [Reuter2013]_ for more details.

To play a dice game, one would need:

- two dice
- a tables sheet with the measure indices
- a measures sheet with all the numbered bars
- music paper to write down your composition

The measures and tables where composed by the composer of the dice game and were organized such,
that random compilations made a musical composition.
To play the game, you would have to throw the dice, and then look up the measure
corresponding to your dice throw and your bar index in the dice table.
Having found the right bar number, you then select that bar from the measures sheet provided.

This software package automizes the production of these musical pieces.
All pieces (tables sheets and measures) have been inserted into this software package and
suitable software has been created to allow production of the musical pieces.

For a use case of this library, and more information on these dice games, please visit http://opus-infinity.org,
a website by the same author.

For complete functionality, this package requires the following packages to be installed on the user's system:

- lilypond, to convert the compositions into midi and pdf files
- fluidsynth or timidity, for converting midi to wav
- ffmpeg, to convert wav to other audio formats
- imagemagick, to prepare the image outputs of the compositions

**********
Python API
**********
The major component of this library is the class "DiceGame". All dicegames implement this class and its funcions.
For use cases, please see the demo's in the `scripts` folder.


*****************
Technical details
*****************
All musical dice games are stored internally using Lilypond bars.
When composed into a musical piece, these bars are combined to form a complete piece.
The external package Lilypond is then called to convert the composition into a midi file and a pdf file.
Next, fluidsynth, or timidity is used to convert the midi to wav, either using a default soundfont, or a user provided soundfont.
Afterwards, the composition pdf can be transformed to png for display in, for example, a browser.


.. [Reuter2013] Reuter, Christoph. (2013), Der Würfel als Autor, Würfelmusik und Zufallstexte des 17. bis 19. Jahrhunderts. In: Herbert Bannert, Elisabeth Klecker (Hgg.), Autorschaft, Konzeptionen, Transformationen, Diskussionen. Wien, Praesens Verlag. p. 195-222.
