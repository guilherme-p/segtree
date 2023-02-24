from collections.abc import Callable

class SegmentTree:
    def __init__(self, arr: list[int], merge_function: Callable[[int, int], int]):
        self.N = len(arr)
        self.tree: list[int] = [0] * 4 * self.N                 # Number of levels = ceil(log(N)) + 1 <= logN + 2; Number of nodes = 2^levels - 1 < 4N
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
    
    def print(self, )
        #    A
        #  A   B
        # A B C D