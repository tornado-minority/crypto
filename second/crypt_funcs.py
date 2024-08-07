from random import randint, randrange


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


def miller_rabin(m, k=40):
    """
    Пусть  — нечётное число большее 1. Число m - 1 однозначно представляется в виде m - 1 = 2^s * t, где t нечётно.
    Целое число a,1 < a < m , называется свидетелем простоты числа m, если выполняется одно из условий:
    1) a^t = 1 (modm)
    2) или существует целое число k, 0 <= k < s, такое, что a^(2^k * t) = 1
    :param m: Число
    :param k: Количество раундов проверки
    :return:
    """

    s, t = 0, m - 1
    while t % 2 == 0:
        s += 1
        t //= 2

    for _ in range(k):
        a = randrange(2, m - 1)
        x = pow(a, t, m)
        if x == 1 or x == m - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, m)
            if x == m - 1:
                break
        else:
            return False
    return True


def is_prime(num, simple_primes):
    if num not in simple_primes:
        for simple_prime in simple_primes:
            if num % simple_prime == 0:
                return False
    else:
        return True

    if miller_rabin(num):
        return True
    return False


def gen_prime(place=100):
    simple_primes = sieve(1500)
    num = randint(10 ** (place - 2), 10 ** place) * 2 + 1

    while not is_prime(num, simple_primes):
        num += 2
    return num


def gcd_extended(a, b):
    # Base Case
    if a == 0:
        return b, 0, 1

    gcd_, x1, y1 = gcd_extended(b % a, a)

    # Update x and y using results of recursive
    # call
    x = y1 - (b // a) * x1
    y = x1

    return gcd_, x, y


def hash_msg(m, n):
    h = 2
    for i in str(m):
        i = int(i)
        h = pow((i + h), 2, n)
    return h