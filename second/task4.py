from crypt_funcs import gen_prime, hash_msg, gcd_extended
from random import randint
from math import gcd
from decimal import *
import fractions
from hashlib import sha256


def gen_keys(key_len):
    p_len = len(str(2 ** 5))
    q_len = len(str(2 ** 4))
    p, q = gen_prime(p_len), gen_prime(q_len)
    x = randint(1, p - 2)
    y = pow(q, x, p)
    return p, q, x, y


def gen_sign(m, p, q, x):
    M = Decimal(hash_msg(m, p))

    k = randint(2, p - 1)
    while gcd(k, p - 1) != 1:
        k = randint(1, p - 1)

    a = Decimal(pow(q, k, p))
    e1 = M - Decimal(x) * Decimal(a)
    gcd_res = gcd_extended(k, p - 1)[1]
    e2 = gcd_res if gcd_res < 0 else p - 1 - gcd_res

    getcontext().prec = 1000
    b = abs(e1 * e2) % (Decimal(p) - 1)
    return (a, b), M


def auth(m, s, p, q, y):
    a, b = s

    getcontext().prec = 1000
    assert y ** a * a ** b % Decimal(p) == pow(q, m, p)
    print('Signature assertion complete')


def elgamal(m, key_len=10):
    p, q, x, y = gen_keys(key_len)
    S, M = gen_sign(m, p, q, x)
    auth(M, S, p, q, y)


if __name__ == '__main__':
    elgamal(312)
