from time import time
from task3 import ds_rsa
from task4 import elgamal


if __name__ == '__main__':
    t = time()
    ds_rsa(312)
    print(f"RSA signature work time: {time() - t}")

    t = time()
    elgamal(312)
    print(f"El Gamal signature work time: {time() - t}")
