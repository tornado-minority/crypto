from random import randint


def pollard_discrete_logs(alpha, beta, n):
    turtle = (1, 0, 0)
    rabbit = (1, 0, 0)

    def calc_xab(x, a, b):
        r = x % 3
        if r == 0:
            x = x * x % n
            a, b = 2 * a % (n - 1), 2 * b % (n - 1)
        elif r == 1:
            x = x * alpha % n
            a = (a + 1) % (n - 1)
        else:
            x = x * beta % n
            b = (b + 1) % (n - 1)
        return x, a, b

    for _ in range(n):
        turtle = calc_xab(*turtle)
        rabbit = calc_xab(*rabbit)
        rabbit = calc_xab(*rabbit)
        if rabbit[0] == turtle[0]:
            return None

    return turtle, rabbit


if __name__ == '__main__':
    print(pollard_discrete_logs(2, 5, 1019))

