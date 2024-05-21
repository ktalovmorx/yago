import math
import inspect
from copy import deepcopy as copy
import primes, merge
import shutil
import linear_regression

from functools import total_ordering

@total_ordering
class WrapperStr(str):
    def __init__(self, s: str):
        self.str = s
    def __eq__(self, other):
            if len(self.str)!=1 or len(other)!=1:
                raise Exception(f'It is illegal to compare strings of lengh greater than 1: "{self.str}", "{other.str}"')
            return self.str==other
    def __le__(self, other):
            if len(self.str)!=1 or len(other)!=1:
                raise Exception(f'It is illegal to compare strings of lengh greater than 1: "{self.str}", "{other.str}"')
            return self.str<other

    def __contains__(self, item):
            raise Exception(f'Illegal call to "in"')
    def __getitem__(self, key):
        if not isinstance(key, int):
            raise Exception(f'Illegal call [{key}]')
        return self.str[key]

    def lower(self):
        raise Exception('Illegal call')

@total_ordering
class WrapperLst(list):
    def __init__(self, l: list):
        self.list = l

    def __eq__(self, other):
        raise Exception('It is illegal to compare lists')

    def __le__(self, other):
        raise Exception('It is illegal to compare lists')

    def __contains__(self, item):
            raise Exception(f'Illegal call to "in"')

    def __getitem__(self, key):
        if not isinstance(key, int):
            raise Exception(f'Illegal call [{key}]')
        return self.list[key]


import hashlib
fhs = open('MD5').read().split()
hs = hashlib.md5(open(fhs[1],'rb').read()).hexdigest()
assert hs == fhs[0].strip(), 'The testing file has been modified'

def runtests(tests, fun,
             equals=lambda x,y: x==y,
             keep_originals=False, is_proc=False):
    for test, ex_res in tests:
        print(f'"{test}", "{ex_res}"....', end='')
        if inspect.isclass(ex_res) and issubclass(ex_res, Exception):
            try:
                res = fun(*test)
            except ex_res:
                print('OK')
            else:
                assert False, 'The arguments are illegal and not detected'
        else:
            if keep_originals:
                test_ori = copy(test)
            if not is_proc:
                res = fun(*test)
                assert equals(res, ex_res), f'Error, the result is "{res}"'
                if keep_originals:
                    assert test == test_ori, \
                        f'The originals values has been modified: {test} {test_ori}'
            else:
                res = fun(*test)
                assert res is None, 'The function must not return a value'
                assert equals(test, ex_res), f'The modified vaule is {test}'
            print('OK.')


def test_isprime():
    tests = [((6, [2, 3, 5]), False),
             ((7, [2, 3, 5]), True),
             ((9, [2, 3, 5, 7]), False),
             ((15, [2, 3, 5, 7, 11, 13]), False),
             ((17, [2, 3, 5, 7, 11, 13]), True)]
    runtests(tests, primes.is_prime)


def test_next_prime():
    tests = [(([],), ([2],)),
             (([2, 3, 5],), ([2, 3, 5, 7], )),
             (([2, 3, 5, 7],), ([2, 3, 5, 7, 11], )),
             (([2, 3, 5, 7, 11, 13],), ([2, 3, 5, 7, 11, 13, 17], )),
             ]
    runtests(tests, primes.next_prime, is_proc=True)


def test_read_primes():
    tests = [
        (('prime_2.txt',), [2, 3]),
        (('prime_5.txt',), [2, 3, 5, 7, 11]),
        (('prime_vacio.txt', ), [])]
    runtests(tests, primes.read_primes)

def test_add_primes():
    def _test(filename, nprimes):
        tmp_file = f'{filename}_tmp'
        shutil.copy(filename, tmp_file)
        primes.add_primes(tmp_file, nprimes)
        return primes.read_primes(tmp_file)

    tests = [
        (('prime_2.txt', 3), [2, 3, 5, 7, 11]),
        (('prime_5.txt', 4), [2, 3, 5, 7, 11, 13, 17, 19, 23]),
        (('prime_vacio.txt', 3), [2, 3, 5])]
    runtests(tests, _test)


def test_merge_files():
    def read_file(filename):
        with open(filename) as f:
            return list(map(int, f))
    def _test(f1, f2):
        merge.merge(f1, f2, "tmp")
        lst1 = read_file(f1)
        lst1.extend(read_file(f2))
        res = read_file("tmp")
        lst1.sort()
        return res == lst1

    tests = [(('f1.txt', 'f2.txt'), True)]
    runtests(tests, _test)


def test_regression():
    filename = 'test_regression'
    linear_regression.gen_test_file(filename)
    a, b = linear_regression.linear_regression(filename)
    print(a, b)
    assert math.isclose(a, 2)
    assert math.isclose(b, 1)
    print('OK')
