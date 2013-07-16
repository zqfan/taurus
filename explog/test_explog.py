#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright (C) 2013 ZhiQiang Fan <aji.zqfan@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest
import pep8


class PEP8Test(unittest.TestCase):
    def test_pep8(self):
        explog_pep8 = pep8.Checker(u'explog.py')
        r = explog_pep8.check_all()
        explog_test_pep8 = pep8.Checker(__file__)
        r += explog_test_pep8.check_all()
        self.assertEqual(r, 0)


if __name__ == '__main__':
    unittest.main()
