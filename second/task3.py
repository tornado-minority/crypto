from crypt_funcs import gen_prime, gcd_extended, hash_msg
from math import gcd


def get_keys(dig: 100):
    p, q = gen_prime(dig), gen_prime(dig)
    while p == q:
        q = gen_prime(dig)
    n = p * q
    fi = (p - 1)*(q - 1)
    d = gen_prime(dig)
    while not (1 < d < fi) or not gcd(d, fi) == 1:
        d = gen_prime()
    e = gcd_extended(fi, d)[2]
    return e, d, n, fi


def auth(m, s, e, n):
    m_signed = pow(s, e, n)
    assert m_signed == m
    print('Signature assertion complete')


def ds_rsa(m):
    e, d, n, fi = get_keys(2)
    M = hash_msg(m, n)
    S = pow(M, d, n)
    auth(M, S, e, n)


if __name__ == '__main__':
    ds_rsa(312)
