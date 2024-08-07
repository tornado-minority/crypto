from decimal import Decimal, getcontext
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA
from task1 import extended_gcd
import requests
import re


def public_key_attack(n, e):
    response = requests.get(url=f'http://factordb.com/index.php?query={str(n)}')
    response_numbers = response.text.split('\n')[26].split(';')
    n = []
    for s in response_numbers[1:]:
        if 'href' in s:
            cur_n = re.sub(r"((<).*?(>))|(&.*)|(=)|(\s)", '', s)
            if cur_n != '':
                n.append(Decimal(cur_n))

    getcontext().prec = len(str(n)) + 1
    fi = (n[0] - 1) * (n[1] - 1)
    d = extended_gcd(fi, e)[1]
    return d


if __name__ == '__main__':
    with open('public.pem', 'r') as fp:
        public_key = RSA.import_key(fp.read())

    d = public_key_attack(public_key.n, public_key.e)

    with open('crypt', 'rb') as fp:
        data = fp.read()

    data = int.from_bytes(data)

    m = pow(data, int(d), public_key.n)

    b = m.to_bytes(32)
    print(b)
