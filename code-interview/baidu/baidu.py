#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shitwidth=4 softtabstop=4

def matrix_has_element(matrix, k):
    """return true if k in matrix. else false. O(m*n)"""
    return k in [j for i in matrix for j in i]

def ordered_matrix_has_element(matrix, k):
    """return true if k in matrix, else false. O(logm+logn)

    matrix should in increasing order in each row and col
    """
    if not matrix:
        return False
    if not matrix[0]: # [[]] is true but [] is false
        return False
    def find_pos(r, start, end, k):
        if start == end:
            # if k == r[start], then we find it
            # if k > r[start], since the k < r[start+1], we should
            # return start
            # if k < r[start], then return start-1
            return start if k >= r[start] else start - 1
        m = (start + end)/2
        if k == r[m]:
            return m
        # it can be just in the m col, if currently is just find the
        # col index, but we still search the bigger, because if it
        # is less than the bigger, it will return m+1-1=m
        elif k > r[m]:
            return find_pos(r, m + 1, end, k)
        # k < r[m], search the lower bound
        else:
            return find_pos(r, start, m - 1, k)

    col = find_pos(matrix[0], 0, len(matrix[0]) - 1, k)
    if col < 0:
        return false
    col_list = [row[col] for row in matrix]
    row = find_pos(col_list, 0, len(matrix) - 1, k)
    return matrix[row][col] == k


if __name__ == '__main__':
    test()
