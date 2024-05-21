import sys
import random
import math


def linear_regression(filename: str) -> tuple[float, float]:
    xsum = .0
    ysum = .0
    xysum = .0
    x2sum = .0
    total = .0
    with open(filename) as fl:
        for line in fl:
            data = line.strip().split()
            x = float(data[0])
            y = float(data[1])
            xsum += x
            ysum += y
            xysum += x * y
            x2sum += x ** 2
            total += 1
    sxy = xysum - (xsum * ysum) / total
    sxx = x2sum - (xsum ** 2) / total
    a = sxy / sxx
    b = ysum / total - a * xsum/total
    return a, b

def gen_test_file(filename):
    with open(filename, 'w') as f:
        for _ in range(10):
            x = random.random()*100
            y = 2*x + 1
            f.write(f'{x}\t{y}\n')


def main(filename: str) -> None:
    a, b = linear_regression(filename)
    print(a, b)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Usage: python {sys.argv[0]} filename')
        sys.exit(1)
    main(sys.argv[1])
