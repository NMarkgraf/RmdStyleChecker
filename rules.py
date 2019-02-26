#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
  Norman's little Rmarkdown style checker

  Counter Classes

  (C)opyleft in 2018/19 by Norman Markgraf (nmarkgraf@hotmail.com)

  Release:
  ========
  0.1   - 29.04.2018 (nm) - Erste Version
  0.2   - 26.02.2019 (nm) - Kleine Schönheitsupdates

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

from collections import deque


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Rule:

    def __init__(self):
        self.errorLog = ErrorLogger()

    def handleLine(self, line):
        pass

    def hasError(self):
        return self.errorFlag

    def __str__(self):
        return self.errorLog

    def __repr__(self):
        return (
            "errorFlag:"
            + str(self.errorFlag)
            + " errorLog:"
            + str(self.errorLog)
        )

    def error(self):
        if self.hasError():
            return self.errorLog
        else:
            return ""

    def raiseError(self, newErrorMsg):
        self.setError(newErrorMsg)

    def setError(self, newErrorMsg):
        self.errorFlag = True
        self.errorLog.append(newErrorMsg)


class RegExMatchRule(Rule):

    def __init__(self,  rulepattern):
        super().__init__()
        self.re_comp = re.compile(rulepattern)

    def matchLine(self,  line):
        prg = self.re_comp
        result = prg.search(line)
        return(result)

    def handleLine(self,  line):
        pass


class TailingWhiteSpaceRule(RegExMatchRule):

    def __init__(self):
        super().__init__("[\t\f\v ]$")

    def handleLine(self,  line):
        mtch = self.matchLine(line)
        if mtch:
            self.raiseError("has tailing whitespaces!")
        return mtch


class LookBackQueue(metaclass=Singleton):
    
    __lookback = None
    
    def __init__(self):
        self.__lookback = deque([], 5)

    def __str__(self):
        return str(self.__lookback)

    def __repr__(self):
        return repr(self.__lookback)

    def __len__(self):
        return len(self.__lookback)
        
    def append(self, line):
        self.__lookback.append(line)
        
    def lookup(self, index):
        return self.__lookback[-1*(index+1)]
        

class LookBackRule(Rule):

    def __init__(self):
        super().__init__()
        self.lookback = LookBackQueue()

    def handleLine(self, line):
        pass


class CodeblockFlag(metaclass=Singleton):
    
    def __init__(self):
        self.__flag = False
        self.re_codeblock = re.compile("^```")
        
    def isCodeblock(self, line):
        return self.re_codeblock.search(line)

    def toggleInsideCodeblock(self):
        self.__flag = not self.__flag
        return self.__flag
        
    def handleLine(self, line):
        if self.isCodeblock(line):
            self.toggleInsideCodeblock()
            
    def flag(self):
        return self.__flag


class OneBlankLinesBeforeCodeblock(LookBackRule):

    def __init__(self):
        super().__init__()
        self.re_blankline = re.compile("^\s*$")
        self.__insideCodeblock = CodeblockFlag()
        self.re_codeblock = re.compile("^```")
        
    def isCodeblock(self, line):
        return self.re_codeblock.search(line)

    def isBlankLine(self, line):
        return self.re_blankline.search(line)

    def lastLineIsBlank(self):
        return self.isBlankLine(self.lookback.lookup(1))

    def handleLine(self, line):
        if self.isCodeblock(line):
           if self.__insideCodeblock.flag():
                if len(self.lookback) < 2:
                    self.raiseError("has no blank line before codeblock, should be one!")
                else:
                    if not self.lastLineIsBlank():
                        self.raiseError("has no blank line before codeblock, should be one!")


class OneBlankLinesAfterCodeblock(LookBackRule):

    def __init__(self):
        super().__init__()
        self.re_blankline = re.compile("^\s*$")
        self.re_codeblock = re.compile("^```")
        self.__insideCodeblock = CodeblockFlag()

    def isCodeblock(self, line):
        return self.re_codeblock.search(line)

    def isBlankline(self, line):
        return self.re_blankline.search(line)

    def lastLineWasCodeblock(self):
        return self.isCodeblock(self.lookback.lookup(1))

    def handleLine(self, line):
        if not self.__insideCodeblock.flag():
            print("***"+line)
            if len(self.lookback) > 1:
                if self.lastLineWasCodeblock():
                   if not self.isBlankline(line):
                      self.raiseError("has no blank line after codeblock, should be one!")


class TwoBlankLinesBeforeHeader(LookBackRule):

    def __init__(self):
        super().__init__()
        self.re_blankline = re.compile("^\s*$")
        self.re_header = re.compile("^#+")

    def isBlankLine(self, line):
        return self.re_blankline.search(line)

    def isNotABlankLine(self, line):
        return not self.isBlankLine(line)

    def lastTwoLinesAreNotBlankLines(self):
        return (self.isNotABlankLine(self.lookback.lookup(1))
                and self.isNotABlankLine(self.lookback.lookup(2)))

    def isHeader(self, line):
        return self.re_header.search(line)

    def handleLine(self, line):
        if self.isHeader(line):
            if len(self.lookback) < 3:
                self.raiseError("has no blank line before Header, should be two!")
            else:
                if self.lastTwoLinesAreNotBlankLines():
                    self.raiseError("has no blank line before Header, should be two!")
                else:
                    if self.isNotABlankLine(self.lookback.lookup(1)):
                        self.raiseError("has one blank line before Header, should be two!")


class ErrorLogger(metaclass=Singleton):

    __errors = []

    def __init__(self):
        self.__errors = []
        self.__lc = LineCounter()

    def __str__(self):
        fullError = "\n"
        for line in self.__errors:
            fullError = fullError + line + "\n"
        return fullError

    def __repr__(self):
        return repr(self.__errors)

    def append(self, msg):
        self.__errors.append("Line " + str(self.__lc) + " " + msg)

    def logError(self, msg):
        self.__append(msg)

    def hasErrors(self):
        return not self.__errors == []


class LineCounter(metaclass=Singleton):

    __counter = 0

    def __init__(self):
        self.__counter = 0

    def __str__(self):
        return str(self.__counter)

    def __repr__(self):
        return repr(self.__counter)

    def inc(self):
        self.__counter +=  1


class LineScanner(metaclass=Singleton):
    
    __matches = {
        "tailingwhitespaces" : "[\t\f\v ]$",
        "blankline" : "^\s*$",
        "ATXheader" : "#+",
        "codeblock" : "```"
    }

    def __init__(self):
        for key, value in self.__matches.iteritems():
            self.__recomp[key] = re.comile(value)

    def scan(self, patname, line):
        return self.__recomp[patname].search(line)


def main():

    lookBackQue = LookBackQueue()
    codeblockFlag = CodeblockFlag()
    errors = ErrorLogger()
    lineCounter = LineCounter()

    rules = []
    rules.append(TailingWhiteSpaceRule())
    rules.append(TwoBlankLinesBeforeHeader())
    rules.append(OneBlankLinesBeforeCodeblock())
    rules.append(OneBlankLinesAfterCodeblock())


    lines = [
        "Blubber",  # 1
        "Blubber ",  # 2
        "# Kopfzeile",  # 3
        "",  # 4
        "",  # 5
        "# Noch eine Kopfzeile",  # 6
        " ",  # 7
        "## Und noch eine Folie",  # 8
        "Blubber",  # 9
        "```",  # 10
        "Blubber ",  # 11
        "```",  # 12
        "Blubber",  # 13
        "",  # 14
        "```",  # 15
        "Blubber ",  # 16
        "```"  # 17
    ]

    for line in lines:
        lineCounter.inc()
        lookBackQue.append(line)
        codeblockFlag.handleLine(line)
        for rule in rules:
            rule.handleLine(line)

    if errors.hasErrors():
        print(errors)


if __name__ == "__main__":
    main()
