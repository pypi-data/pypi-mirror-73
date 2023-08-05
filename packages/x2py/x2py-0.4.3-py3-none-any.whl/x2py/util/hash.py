# Copyright (c) 2017, 2018 Jae-jun Kang
# See the file LICENSE for details.

HASH_SEED = 17

def hash_update(seed, value):
    return int(((seed << 5) + seed) ^ value)

class Hash(object):
    def __init__(self, code=HASH_SEED):
        self.code = code

    def update(self, value):
        self.code = hash_update(self.code, value)
