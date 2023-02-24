class SegmentTree:
    def __init__(self, arr: list[int], merge_function: Callable[[int, int], int]):
        N = len(arr)
        self.tree = [0] * 4 * N                 # Number of levels = ceil(log(N)) + 1 <= logN + 2; Number of nodes = 2^levels - 1 < 4N
        self.merge_function = merge_function
        self.build(arr, 0, N - 1)
    
    def build(self, arr: list[int], l: int, r: int, n=0):
        if l == r:
            self.tree[n] = arr[l]
        else:
            m = (l + r) // 2

            left = get_left_child(n)
            right = get_right_child(n)

            a = self.build(arr, l, m, left)
            b = self.build(arr, m + 1, r, right)

            self.tree[n] = self.merge_function(a, b)
            
        return self.tree[n]

    
    def get_left_child(n: int) -> int:
        return 2 * n + 1                        # 0-indexed

    def get_right_child(n: int) -> int:
        return 2 * n + 2
    
