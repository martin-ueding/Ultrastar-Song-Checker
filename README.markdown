# Ultrastar Song Checker

Ultrastar is a karaoke software. It reads text files which contain the meta
data for the songs as well as the lyrics with timing information.

This tool can generate a SQLite database with all the metadata (using the
`gendb` subcommand). This database can then be queried (with the `query`
subcommand). See the help output (`-h` or `--help`) for the subcommands to
obtain more information.

## Usage

To run the program from this source checkout, run this:

    python3 -m songchecker

It will tell you which subcommands are available and which options are needed.
A more helpful output can be obtained with

    python3 -m songchecker -h

or with something like this:

    python3 -m songchecker gendb -h

## License (GPLv2 or later)

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 2 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
details.

You should have received a copy of the GNU General Public License along with
this program. If not, see http://www.gnu.org/licenses/.
