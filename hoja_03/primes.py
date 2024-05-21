import sys

"""
Program that computes the firt primes and store them into a file
"""

def is_prime(num: int, primelst: list[int]) -> bool:
    """
    This function check if num is prime.

    Parameters
    ----------
    num > 1
    primelst contains the primes less than num
    """
    i = 0
    while i<len(primelst) and primelst[i]**2 < num and num % primelst[i] != 0:
        i += 1
    return i == len(primelst) or primelst[i]**2 > num


def next_prime(primelst: list[int]) -> None:
    """
    This function computes the next prime in the list

    Parameters
    ----------
    primelst contains all the first len(lst) primes
    """
    if len(primelst) == 0:
        primelst.append(2)
    else:
        num = primelst[-1] + 1
        while not is_prime(num, primelst):
            num += 1
        primelst.append(num)


def add_primes(filename: str, nprimes: int) -> None:
    """
    This function adds  n primes into the file

    Parameters
    ----------
    primelst list of the first pimes
    """

    primelst = read_primes(filename)
    with open(filename, "a") as flp:
        for _ in range(nprimes):
            next_prime(primelst)
            prime = primelst[-1]
            flp.write(f"{prime}\n")

def read_primes(filename: str) -> list[int]:
    """
    Read the primes form the list

    Parameters
    ----------
    filename contains a list of the first primes
    """
    primelst: list[int] = []
    with open(filename) as fl:
        for line in fl:
            primelst.append(int(line))
    return primelst

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f'Usage: {sys.argv[0]} filename nprimes')
        sys.exit(2)
    filename = sys.argv[1]
    nprimes = int(sys.argv[2])
    add_primes(filename, nprimes)
