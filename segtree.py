from collections.abc import Callable

class SegmentTree:
    def __init__(self, arr: list[int], merge_function: Callable[[int, int], int]):
        self.N = len(arr)
        self.EMPTY = float("inf")

        self.tree: list[int] = [self.EMPTY] * (4 * self.N - 1)                 # Number of levels = ceil(log(N)) + 1 <= logN + 2; Number of nodes = 2^levels - 1 < 4N
        self.merge_function = merge_function
        self.build(arr, 0, self.N - 1)
    
    def build(self, arr: list[int], l: int, r: int, n=0) -> None:
        if l == r:
            self.tree[n] = arr[l]
        else:
            m = (l + r) // 2

            left = self.get_left_child(n)
            right = self.get_right_child(n)

            a = self.build(arr, l, m, left)
            b = self.build(arr, m + 1, r, right)

            self.tree[n] = self.merge_function(a, b)
            
        return self.tree[n]

    def get_interval(self, l: int, r: int) -> int:
        assert 0 <= l <= r <= self.N - 1

        def helper(l: int, r: int, n: int, cl: int, cr: int) -> int:
            if (l, r) == (cl, cr):
                return self.tree[n]
            
            m = (cl + cr) // 2

            if l >= m + 1:
                return helper(l, r, self.get_right_child(n), m + 1, cr)
            elif r <= m:
                return helper(l, r, self.get_left_child(n), cl, m)
            else:
                return self.merge_function(
                    helper(l, m, self.get_left_child(n), cl, m),
                    helper(m + 1, r, self.get_right_child(n), m + 1, cr)
                )

        return helper(l, r, 0, 0, self.N - 1)
    
    def update(self, i: int, new: int) -> None:
        def helper(n: int, cl: int, cr: int):
            if cl == cr == i:
                self.tree[n] = new
                return
            
            m = (cl + cr) // 2

            if i <= m:
                helper(self.get_left_child(n), cl, m)
            else:
                helper(self.get_right_child(n), m + 1, cr)
            
            self.tree[n] = self.merge_function(
                self.tree[self.get_left_child(n)],
                self.tree[self.get_right_child(n)]
            )

        helper(0, 0, self.N - 1)

    def get_left_child(self, n: int) -> int:
        return 2 * n + 1                        # 0-indexed

    def get_right_child(self, n: int) -> int:
        return 2 * n + 2
    
    def __str__(self, max_level: int = 8, spacing: int = 2) -> str:
        """
        >>> a = [1,2,3,4,5,6,7,8]
        >>> S = SegmentTree(a, lambda x, y: x + y)
        >>> print(S)

                                    36



                10                      26



            3           7           11          15



         1     2     3     4     5     6     7     8

        """

        from math import log2, ceil

        output = []
        levels = ceil(log2(self.N)) + 1

        exp = 0
        current_level = []

        for i in range(len(self.tree)):
            current_level.append(self.tree[i])

            if len(current_level) == 2 ** exp:
                output.append(current_level[:])
                current_level.clear()

                if exp + 1 == max(max_level, levels):
                    break
                else:
                    exp += 1

        output_str = ""

        max_point_width = max([len(str(el)) for el in self.tree])
        point_span = max_point_width * spacing

        line_width = point_span * (2 ** (levels - 1))
        line_space = 4

        for l in range(levels):
            temp = ""
            
            for n in output[l]:
                temp += str(n).center(line_width // len(output[l]))

            output_str += temp
            output_str += line_space * '\n'
        
        return output_str
    
import unittest
from random import randint

class TestSegmentTree(unittest.TestCase):
    def get_random_array(self, minimum: int = -1000, maximum: int = 1000, length: int = 100) -> list[int]:
        return [randint(minimum, maximum) for _ in range(length)]
    
    def get_prefix_sums(self, A: list[int]) -> list[int]:
        ps = []
        p = 0

        for n in A:
            p += n
            ps.append(p)
        
        return ps

    def test_build(self):
        A = self.get_random_array()
        P = self.get_prefix_sums(A)
        S = SegmentTree(A, lambda x, y: x + y)

        N = len(A)

        for i in range(N):
            for j in range(i, N):
                x = P[j] - (P[i - 1] if i - 1 >= 0 else 0)
                y = S.get_interval(i, j)

                self.assertEqual(x, y)

    def test_update(self):
        A = self.get_random_array()
        S = SegmentTree(A, lambda x, y: x + y)
        N = len(A)

        for _ in range(N):
            i = randint(0, N - 1)
            n = randint(-1000, 1000)

            S.update(i, n)
            A[i] = n

        P = self.get_prefix_sums(A)

        for i in range(N):
            for j in range(i, N):
                x = P[j] - (P[i - 1] if i - 1 >= 0 else 0)
                y = S.get_interval(i, j)

                self.assertEqual(x, y)


if __name__ == '__main__':
    unittest.main()