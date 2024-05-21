import random
import sys

n = int(sys.argv[1])

lst = [random.randint(0, 3*n) for _ in range(n)]
lst.sort()
for n in lst:
    print(n)
