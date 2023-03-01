## Usage

### Range sum queries
```
>>> from segtree import *
>>> a = [1,2,3,4,5,6,7,8]
>>> S = SegmentTree(a, lambda x, y: x + y)
>>> print(S)

                    36



         10                       26



    3           7           11          15



 1     2     3     4     5     6     7     8

```

### Range min queries
```
>>> from segtree import *
>>> a = [1,2,3,4,5,6,7,8]
>>> S = SegmentTree(a, lambda x, y: min(x, y))
>>> print(S)
                       1



           1                       5



     1           3           5           7



  1     2     3     4     5     6     7     8
```
