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

class Counter:

    def __init__(self):
        self.counter = 0
        
    def next(self):
        self.counter = self.counter + 1
            
    def get(self):
        return self.counter
    
    def __repr__(self):
        return repr(self.conter)
        
    def __str__(self):
        return str(self.counter)

    
class LineNumberCounter(Counter):
    
    def __repr__(self):
        return "Line "+repr(self.counter)+" "
        
    def __str__(self):
        return "Line "+str(self.counter)+" "


class EmptyLineCounter(Counter):
    
    def reset(self):
        self.counter = 0


def main():
    pass


if __name__ == "__main__":
    main()
