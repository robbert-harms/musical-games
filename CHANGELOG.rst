*********
Changelog
*********


Version 0.9.2 (2025-01-31)
==========================

Features
--------
- *(changelog)* Moved from gitchangelog to gitt-cliff

Other
-----
- Updated the Python requirement for travis.



Version 0.9.1 (2024-12-28)
===================
- Python version bump.


Version 0.9.0 (2024-08-07)
==========================

Added
-----
- Adds Calegari Aria.

Changed
-------
- Modified the random music generator to have a separate seed for each table.

Other
-----
- Storing centered text function.


Version 0.8.9 (2024-05-13)
==========================

Fixed
-----
- Fixed repeated bass clef in Gerlach compositions.


Version 0.8.7 (2024-05-13)
==========================

Added
-----
- Adds annotation data to the bars, enabling more information in the renderers.

Other
-----
- Increased volume of timidity conversion.


Version 0.8.6 (2024-05-11)
==========================

Changed
-------
- Changed the order of the midi converters to have timidity first. This because in fluidsynth 2.3.1 there is a strange pauze at the end of the tracks.


Version 0.8.5 (2024-05-11)
==========================

Fixed
-----
- Fixed midi generation in Gerlach.


Version 0.8.4 (2024-05-11)
==========================

Changed
-------
- Updated Gerlach bar 64 to be in the g-key.


Version 0.8.3 (2024-05-04)
==========================

Fixed
-----
- Fixed the max dice value property.


Version 0.8.2 (2024-05-04)
==========================

Changed
-------
- Updates the lilypond files to have split lines in the pdf output.

Other
-----
- In the Mozart parts, removed the left_hand_alternative as a separate staff and merged it with the left_hand staff. The processing happens now in the template. The reason for this is that it made Opus-Infinity easier to program.


Version 0.8.1 (2024-05-01)
==========================

Other
-----
- Improved the lilypond designs.
- In Gerlach, fixed some errors and made the clef change only local to the one specific bar.
- Removed stem position overwrites in the Gerlach bars.


Version 0.8.0 (2024-04-30)
==========================

Added
-----
- Adds Gerlach's Scottish Dance. Might need some more work concerning the clef changes.


Version 0.7.1 (2024-04-19)
==========================

Added
-----
- Adds functionality for rendering a single dice table element.
- Adds support for dice games selecting multiple measures per dice throw.


Version 0.7.0 (2024-04-16)
==========================

Added
-----
- Adds the contredanse from Mozart.


Version 0.6.2 (2024-04-13)
==========================

Added
-----
- Adds pip release to makefile.

Fixed
-----
- Fixed independent staff shuffling.


Version 0.6.1 (2024-04-13)
==========================
- Reduced dependencies.


Version 0.6.0 (2024-04-13)
==========================
- Updated the library to a new format, with a cleaner API design.
- Upgraded package to latest format with toml file.
- Added typehints to the external library calls.
- Updated the readme


Version 0.5.2 (2022-02-15)
==========================

Fixed
-----
- Fixed wrong order of bars in the Mozart dice game.


Version 0.5.1 (2022-02-14)
==========================
- Small refactoring of the lilypond render function.


Version 0.5.0 (2022-02-12)
==========================
- Refactored the dice games.


Version 0.4.1 (2021-11-27)
==========================
- Corrected the version numbers.


Version 0.4.0 (2021-11-27)
===========================
Large refactorings in the API.


Version 0.3.14 (2015-01-01)
===========================
Old version
