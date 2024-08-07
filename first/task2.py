import random


def sieve(n):
    primes = [i for i in range(n + 1)]

    primes[1] = 0

    i = 2
    while i <= n:
        if primes[i] != 0:
            j = i + i
            while j <= n:
                primes[j] = 0
                j = j + i
        i += 1

    primes = [i for i in primes if i != 0]
    return primes


def fermat(a, n):
    return ((a ** (n - 1)) % n) == 1


def miller_rabin(n, k):
    if n == 2:
        return True

    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def gen_primes(n):
    primes = sieve(1600)
    while len(primes) < n:
        num = random.randint(0, primes[-1] + 2 ** 32) * 2 + 1
        if fermat(2, num) and miller_rabin(num, 40):
            primes.append(num)
    return primes


def gen_num(primes):
    num = 1
    m = 2 ** 128
    while num < m:
        rand_ind = random.randint(0, len(primes))
        num *= primes[rand_ind]
    return num


if __name__ == '__main__':
    primes = gen_primes(251)
    p, q = gen_num(primes), gen_num(primes)
    with open('p.txt', 'w') as fp:
        fp.write(f'{hex(p)}')

    with open('q.txt', 'w') as fp:
        fp.write(f'{hex(q)}')

