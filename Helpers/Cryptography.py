import clr
import os

pathDLL = os.getcwd() + "\\TweetNaCl.dll"

clr.AddReference(pathDLL)
from Supercell.Laser.Titan.Library import TweetNaCl
from hashlib import blake2b
import numpy as np

class LogicRandom:
    def __init__(self, seed=0):
        self.seed = np.int32(seed)

    def rand(self, max_val):
        if max_val > 0:
            self.seed = self.iterate_random_seed()
            tmp_val = self.seed if self.seed >= 0 else -self.seed
            #print(tmp_val, self.seed, tmp_val % max_val)
            return tmp_val % max_val
        return 0

    def iterate_random_seed(self):
        seed = self.seed
        if seed == 0:
            seed = -1
        tmp = seed ^ (seed << 13) ^ ((seed ^ (seed << 13)) >> 17)
        tmp2 = tmp ^ (32 * tmp)
        return tmp2

def get_nonce(client_pk, server_pk):
    hasher = blake2b(digest_size=24)

    hasher.update(client_pk)
    hasher.update(server_pk)

    return hasher.digest()

def get_keys(seed):
    client_sk = bytearray(32)
    rand = LogicRandom(seed)

    c = 0
    for i in range(12):
        c = rand.rand(256)

    for i in range(32):
        client_sk[i] = rand.rand(256) ^ c
    
    return bytes(client_sk), bytes(TweetNaCl.CryptoScalarmultBase(client_sk))

def encrypt(message, nonce, server_pk, client_sk):
    return bytes(TweetNaCl.CryptoBox(message, nonce, server_pk, client_sk))

def decrypt(encrypted, nonce, server_pk, client_sk):
    return bytes(TweetNaCl.CryptoBoxOpen(encrypted, nonce, server_pk, client_sk))

