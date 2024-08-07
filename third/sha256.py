import struct
from hashlib import sha256
try:
    import numpy as np
    from matplotlib import pyplot
except ModuleNotFoundError:
    print('Numpy is not found')


class SHA256Hash:

    def __init__(self, data):
        self.data = data
        self.h = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]
        self.k = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
                  0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
                  0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
                  0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
                  0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
                  0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
                  0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
                  0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]

    @staticmethod
    def rotate(n, b):
        return ((n >> b) | (n << (32 - b))) & 0xFFFFFFFF

    def padding(self):
        padding = b"\x80" + b"\x00" * (63 - (len(self.data) + 8) % 64)
        padded_data = self.data + padding + struct.pack(">Q", 8 * len(self.data))
        return padded_data

    def split_blocks(self):
        return [self.padded_data[i : i + 64] for i in range(0, len(self.padded_data), 64)]

    # @staticmethod
    def expand_block(self, block):
        w = list(struct.unpack(">16L", block)) + [0] * 48
        for i in range(16, 64):
            s0 = self.rotate(w[i - 15], 7) ^ self.rotate(w[i - 15], 18) ^ w[i - 15] >> 3
            s1 = self.rotate(w[i - 2], 17) ^ self.rotate(w[i - 2], 19) ^ w[i - 2] >> 10
            w[i] = (w[i-16] + s0 + w[i - 7] + s1) & 0xFFFFFFFF
        return w

    def final_hash(self):
        self.padded_data = self.padding()
        self.blocks = self.split_blocks()

        bit_changed = []
        for block in self.blocks:
            expanded_block = self.expand_block(block)
            a, b, c, d, e, f, g, h = self.h
            for i in range(64):
                s1 = self.rotate(e, 6) ^ self.rotate(e, 11) ^ self.rotate(e, 25)
                ch = (e & f) ^ (~e & g)
                temp1 = h + s1 + ch + self.k[i] + (expanded_block[i] & 0xFFFFFFFF)
                s0 = self.rotate(a, 2) ^ self.rotate(a, 13) ^ self.rotate(a, 22)
                maj = (a & b) ^ (a & c) ^ (b & c)
                temp2 = s0 + maj

                h = g
                g = f
                f = e
                e = (d + temp1) & 0xFFFFFFFF
                d = c
                c = b
                b = a
                a = (temp1 + temp2) & 0xFFFFFFFF

                bit_changed.append([0] * 32)
                for bits in [a, b, c, d, e, f, g, h]:
                    bits = bin(bits)[2:]
                    for j in range(len(bits)):
                        bit_changed[i][j] = int(bits[j])

            self.h = (
                self.h[0] + a & 0xFFFFFFFF,
                self.h[1] + b & 0xFFFFFFFF,
                self.h[2] + c & 0xFFFFFFFF,
                self.h[3] + d & 0xFFFFFFFF,
                self.h[4] + e & 0xFFFFFFFF,
                self.h[5] + f & 0xFFFFFFFF,
                self.h[6] + g & 0xFFFFFFFF,
                self.h[7] + h & 0xFFFFFFFF,
            )
        return ("{:08x}" * 8).format(*self.h), bit_changed


if __name__ == "__main__":
    hash_input = bytes('miet_crypto', "utf-8")
    print(SHA256Hash(hash_input).final_hash())
    print(sha256(hash_input).digest().hex())

    hash_input = b"\x01"
    c1 = np.array(SHA256Hash(hash_input).final_hash()[1])
    hash_input = b"\x00"
    c2 = np.array(SHA256Hash(hash_input).final_hash()[1])
    pyplot.plot(range(64), (c1 != c2).sum(axis=1))
    pyplot.show()

