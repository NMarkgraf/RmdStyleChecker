#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
  Norman's little Rmarkdown style checker

  Counter Classes

  (C)opyleft in 2018 by Norman Markgraf (nmarkgraf@hotmail.com)

  Release:
  ========
  0.1   - 29.04.2018 (nm) - Erste Version

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

class Rule:

    errorMsg = ""

    def __init__(self):
        pass

    def handleLine(self, line):
        pass
    
    def error(self):
        return(self.errorMsg)
    
class RegExMatchRule(Rule):
    
    def __init__(self,  rulepattern):
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
            self.errorMsg = "has tailing whitespaces!"
        return mtch

class LookBackRule(Rule):
    
    def __init__(self):
        self.lookback = deque([])
        
    def handleLine(self, line):
        self.handleLinePre(line)
        ret = self.handleLineWork(line)
        self.handleLinePost(line)
        return(ret)

    def handleLinePre(self, line):
        self.lookback.append(line)
        
    def handleLinePost(self, line):
        if len(self.lookback) > 3:
            self.lookback.popleft()

    def handleLineWord(self, line):
        pass
    
class TwoBlankLinesBeforeHeader(LookBackRule):
    
    def __init__(self):
        super().__init__()
        self.re_blankline = re.compile("^\s*$")
    
    def isBlankLine(self, line):
        return self.re_blankline.search(line)
    
    def handleLineWork(self, line):
        if len(self.lookback) < 3:
            self.errorMsg = "has no two blank lines before Header!"
            return False
        else:
            if not(self.isBlankLine(self.lookback[-2])) and not(self.isBlankLine(self.lookback[-3])):
                    self.errorMsg = "has no blank line before Header, should be two!"
                    return False
            if not self.isBlankLine(self.lookback[-2]):
                self.errorMsg = "has one blank line before Header, should be two!"
                return False
        return True
        
def main():
    rules = []
    rules.append(TailingWhiteSpaceRule())
    rules.append(TwoBlankLinesBeforeHeader())

    lines = ["Blubber", "Blubber ", "# Kopfzeile", "", "", "# Noch eine Kopfzeile", " ", "## Und noch eine Folie"]
    
    linecounter = 0
    
    for line in lines:
        linecounter = linecounter + 1
        for rule in rules:
            if rule.handleLine(line):
                print("Line "+ str(linecounter) +" " +rule.error())

if __name__ == "__main__":
    main()
