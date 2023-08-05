# memdump

```
pip install memdump
```

```py
import os
from memdump import memprint

data = os.urandom(100)
memprint(data)
```

```
0000000000000000 | 6b 35 e4 71 71 03 85 c7 | 50 26 ac 06 9b e3 a1 97 | k5.qq...P&......
0000000000000010 | bf 0e 43 8d 21 10 23 0f | e0 c2 36 e8 cf d7 74 5b | ..C.!.#...6...t[
0000000000000020 | 4a 65 21 03 b0 46 c9 b8 | 28 88 06 96 e5 90 18 30 | Je!..F..(......0
0000000000000030 | ca fd ca 10 cb 0a 27 d0 | 01 17 55 80 a7 87 60 3f | ......'...U...`?
0000000000000040 | f6 e3 cd 3f 52 cc 4f d8 | aa 67 95 5b 68 62 b2 b5 | ...?R.O..g.[hb..
0000000000000050 | be 16 d2 c8 02 5c 0c 79 | 28 ef 0d 12 ee 26 7d 53 | .....\.y(....&}S
0000000000000060 | 46 0a bc 1d             |                         | F...
```
