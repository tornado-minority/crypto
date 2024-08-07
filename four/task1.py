from math import gcd


def func(x):
    return x ** 2 + x + 1


def pollard(x0, n):
    x = [x0]
    while True:
        x.append(func(x[-1]))
        cur_x = x[-1]
        for prev_x in x[:-1]:
            if gcd(cur_x - prev_x, n) != 1:
                return gcd(cur_x - prev_x, n), n / gcd(cur_x - prev_x, n)


if __name__ == '__main__':
    print(pollard(2, 151 * 59))
