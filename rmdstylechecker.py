#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
  Norman's little Rmarkdown style checker

  MAIN

  (C)opyleft in 2018 by Norman Markgraf (nmarkgraf@hotmail.com)

  Release:
  ========
  0.1   - 29.04.2018 (nm) - Erste Version


  WICHTIG:
  ========
    Benoetigt python3 !
    -> https://www.howtogeek.com/197947/how-to-install-python-on-windows/
    oder
    -> https://www.youtube.com/watch?v=dX2-V2BocqQ
    Bei *nix und macOS Systemen muss diese Datei als "executable" markiert
    sein!
    Also bitte ein
      > chmod a+x rmdstylechecker.py
   ausfuehren!

  PEP8? better use pycodestyle
  ============================

    > pycodestyle decorator.py

  Lizenz:
  =======
  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''
import argparse
from scanner import *


def main():
    scn = Scanner()

    parser = argparse.ArgumentParser()
    parser.add_argument("rmdfile",  help="Rmarkdown file to scan")

    args = parser.parse_args()

    inputfile = args.rmdfile
    
    if inputfile != "":
        scn.scan(inputfile)


if __name__ == "__main__":
    main()
