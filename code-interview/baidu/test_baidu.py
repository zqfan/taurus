#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shitwidth=4 softtabstop=4

import unittest

import baidu

class MatrixTest(unittest.TestCase):
    def test_ordered_matrix_has_element_empty_matrix(self):
        """ordered_matrix_has_element should return false for empty matrix"""
        self.assertEqual(False,
                         baidu.ordered_matrix_has_element([], 1))
        self.assertEqual(False,
                         baidu.ordered_matrix_has_element([[]], 1))
        self.assertEqual(False,
                         baidu.ordered_matrix_has_element(None, 1))
        self.assertEqual(False,
                         baidu.ordered_matrix_has_element([[],[]], 1))

    def test_ordered_matrix_has_element_valid_input(self):
        """ordered_matrix_has_element should return correct result"""
        m = [[1,2,3,4,5],[2,3,4,5,6]]
        r1 = baidu.matrix_has_element(m, 6)
        r2 = baidu.ordered_matrix_has_element(m, 6)
        self.assertEqual(r1, r2)


if __name__ == '__main__':
    unittest.main()
