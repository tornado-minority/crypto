import os
from subprocess import run
from random import randint
import matplotlib.pyplot as plt

ROOT = os.path.dirname(__file__)
MSIEVE_PATH = os.path.join(ROOT, 'msieve')
MSIEVE = os.path.join(MSIEVE_PATH, 'msieve153.exe')
WORKTODO = os.path.join(ROOT, 'worktodo.ini')
LOG = os.path.join(ROOT, 'msieve.log')


def factor(n):
    with open(WORKTODO, 'w') as f:
        f.write(f'-n {n}')
    with open(LOG, 'w') as f:
        pass

    run([MSIEVE])

    with open(LOG, 'r') as f:
        text = f.readlines()

    if 'time' in text[-1]:
        time = text[-1].split('time ')[1]
        time = int(time.split(':')[0]) * 3600 + int(time.split(':')[1]) * 60 + int(time.split(':')[2])

        text = ''.join(text[:-1])
    else:
        time = 0
        text = ''.join(text)

    primes = []
    for line in text.split('digits)\n')[1].split('\n'):
        if 'factor: ' in line:
            line.replace('\n', '')
            primes.append(int(line.split('factor: ')[1]))

    return primes, time


if __name__ == '__main__':
    # time_number = {}
    #
    # get_n = lambda x: randint(10 ** (x - 1), 10 ** x)
    # for i in range(5, 100, 5):
    #     n = get_n(i)
    #     time_number[i] = factor(n)[1]
    #     print(n, time_number[i])
    #
    # print(time_number)

    print(factor(1415606447884291776606783262139201189953436249643759632827004228713595295320953939))
