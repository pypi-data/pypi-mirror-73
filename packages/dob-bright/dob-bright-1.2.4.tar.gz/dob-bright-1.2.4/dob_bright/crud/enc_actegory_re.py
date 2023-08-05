# This file exists within 'dob-bright':
#
#   https://github.com/tallybark/dob-bright
#
# Copyright © 2019-2020 Landon Bouma. All rights reserved.
#
# This program is free software:  you can redistribute it  and/or  modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
# either version 3  of the License,  or  (at your option)  any later version  (GPLv3+).
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY;  without even the implied warranty of MERCHANTABILITY or  FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU  General  Public  License  for  more  details.
#
# If you lost the GNU General Public License that ships with this software
# repository (read the 'LICENSE' file), see <http://www.gnu.org/licenses/>.

"""``Act@Gory`` encoding and decoding using regular expressions."""

import re

__all__ = (
    'RegExpActegory',
)


class RegExpActegory(object):

    def __init__(self, sep):
        self.sep = sep

    @property
    def sep(self):
        return self._sep

    @sep.setter
    def sep(self, sep):
        self._sep = sep
        self.reset_re()

    # (lb): I considered supporting double-sep as another way to escape it,
    # e.g., `@@` could be same as `\@`. But you run into problems quickly,
    # e.g., 'a@@@b' would be interpreted as 'a\@@b' and never as 'a@\@b',
    # i.e., (act, cat) would be ('a@', 'b') and never ('a', '@b'). Also, the
    # regex is more cumbersome. So we'll just stick with backslash escapes only.

    def reset_re(self):
        self.re_unescaped_sep = re.compile(r'(?<!\\){}'.format(self.sep))
        self.esc_sep = r'\\{}'.format(self.sep)
        self.raw_sep = r'{}'.format(self.sep)

    def escape(self, text):
        escaped = re.sub(self.raw_sep, self.esc_sep, text)
        return escaped

    def unescape(self, text):
        unescaped = re.sub(self.esc_sep, self.raw_sep, text)
        return unescaped

    def split_parts(self, text):
        try:
            escaped_act, escaped_cat = self.re_unescaped_sep.split(text, 1)
        except ValueError:
            return self.unescape(text), None

        activity = self.unescape(escaped_act)
        category = self.unescape(escaped_cat)
        return activity, category

