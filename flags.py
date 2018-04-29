#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
  Norman's little Rmarkdown style checker

  Flag Class

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


class Flag:

    def __init__(self):
        self.flag = False

    def toggle(self):
        self.flag = not self.flag

    def get(self):
        return self.flag

    def isSet(self):
        return self.get()

    def isNotSet(self):
        return not self.get()

    def set(self, bool):
        self.flag = bool


def main():
    pass


if __name__ == "__main__":
    main()
