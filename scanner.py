#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
  Norman's little Rmarkdown style checker

  Scanner Class

  (C)opyleft in 2018 by Norman Markgraf (nmarkgraf@hotmail.com)

  Release:
  ========
  0.1   - 29.04.2018 (nm) - Initial commit
  0.2   - 01.05.2018 (nm) - Some tiny fixes.

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

import re as re
from counter import *
from flags import Flag


class Scanner:

    re_match_emptyLine = "^\s*$"
    re_match_tailingWhiteSpaces = "[\t\f\v ]$"
    re_match_header = "^#+ "
    re_match_codeblock = "^```"

    def __init__(self):
        self.lineNumberCounter = LineNumberCounter()
        self.emptyLineCounter = EmptyLineCounter()
        self.re_emptyLine = re.compile(self.re_match_emptyLine)
        self.re_tailingeWhiteSpaces = re.compile(
            self.re_match_tailingWhiteSpaces)
        self.re_header = re.compile(self.re_match_header)
        self.re_codeblock = re.compile(self.re_match_codeblock)

        self.codeblockFlag = Flag()

    def scan(self, file):
        with open(file, "r") as txt:
            for line in txt:
                self.lineNumberCounter.next()
                self.analyseLine(line)
        print("Scanned " + str(self.lineNumberCounter.get()) + " lines")

    def isEmptyLine(self, line):
        return self.re_emptyLine.search(line)

    def hasTailingWhiteSpaces(self, line):
        return self.re_tailingeWhiteSpaces.search(line)

    def isHeader(self, line):
        return self.re_header.search(line)

    def isCodeblock(self, line):
        return self.re_codeblock.search(line)

    def analyseLine(self, line):
        flagNonEmptyLine = False
        if self.isEmptyLine(line):
            self.emptyLineCounter.next()
        else:
            flagNonEmptyLine = True

        if self.hasTailingWhiteSpaces(line):
            print(str(self.lineNumberCounter) + "has tailing whitespaces!")

        if self.isCodeblock(line):
            self.codeblockFlag.toggle()

        if self.isHeader(line) and self.codeblockFlag.isNotSet():
            warningstr = ""
            if self.emptyLineCounter.get() < 2:
                if self.emptyLineCounter.get() < 1:
                    warningstr = "no" 
                else:
                    warningstr = "only one"
                warningstr = warningstr + " blank line"
            else:
                if self.emptyLineCounter.get() > 2:
                    warningstr = "more than two blank lines"
            if warningstr != "":
                warningstr =  "has " + warningstr + "before header, should be two!"
                print(str(self.lineNumberCounter) + warningstr)

        if flagNonEmptyLine:
            self.emptyLineCounter.reset()
