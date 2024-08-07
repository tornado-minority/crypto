def extended_gcd(a, b):
    if b == 0:
        return 1, 0
    else:
        x1, y1 = extended_gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
    return x, y


if __name__ == '__main__':
    # e = 15, n = 82
    # 15 * d mod 82  = 1
    e = 15
    n = 82
    print(max(extended_gcd(n, e)[1:]))


