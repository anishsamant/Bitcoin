import hashlib
from Crypto.Hash import RIPEMD160
from hashlib import sha256
from math import log
from Blockchain.Backend.core.EllepticCurve.EllepticCurve import BASE58_ALPHABET

def hash256(s):
    """Two rounds of sha 256"""
    # returns in byte format
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()      

def hash160(s):
    return RIPEMD160.new(sha256(s).digest()).digest()

def bytes_needed(num):
    if num == 0:
        return 1
    return int(log(num, 256)) + 1

def int_to_little_endian(n, length):
    return n.to_bytes(length, 'little')

# takes byte sequence and returns an integer
def little_endian_to_int(b):
    return int.from_bytes(b, 'little')

# function to decode base58 encoding
def decode_base58(address):
    num = 0
    for char in address:
        num *= 58
        num += BASE58_ALPHABET.index(char)

    combinedAddr = num.to_bytes(25, byteorder='big')
    checksum = combinedAddr[-4:]

    if hash256(combinedAddr[:-4])[:4] != checksum:
        raise ValueError(f"bad address {checksum} {hash256(combinedAddr[:-4][:4])}")
    
    return combinedAddr[1:-4]