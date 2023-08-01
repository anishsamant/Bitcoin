https://cryptobook.nakov.com/asymmetric-key-ciphers/elliptic-curve-cryptography-ecc

elleptic curve cryptography to generate public private key pairs
NIST curve secp256k1 is used in bitcoin
secp256k1 domain parameters T = (p, a, b, G, n, h)
p = FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFE FFFFFC2F
p =  2256 − 232 − 29 − 28 − 27 − 26 − 24 − 1
finite field with a finite number of elements, which is a prime number. Modulo p should be used in equation.

The cruve E: y2 = x3 + ax + b (mod p) over Fp is defined by:
a = 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000
b = 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000007

The base point G in compressed form is:
G = 02 79BE667E F9DCBBAC 55A06295 CE870B07 029BFCDB 2DCE28D9 59F2815B 16F81798
and in uncompressed form is:
G = 04 79BE667E F9DCBBAC 55A06295 CE870B07 029BFCDB 2DCE28D9 59F2815B 16F81798 483ADA77 26A3C465 5DA4FBFC 0E1108A8 FD17B448 A6855419 9C47D08F FB10D4B8
predetermined point on elleptic curve that everyone uses to determine other points on the curve

Finally the order n of G and the cofactor are:
n = FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFE BAAEDCE6 AF48A03B BFD25E8C D0364141
determines what the maximum value is that can be turned into a private key. ANy 256 number between [1, n-1] is a valid private key

h = 01  
cofactor


to generate human readable public address
1. Hashing the Public Key: Next, the encoded compressed public key is hashed using the SHA-256 and RIPEMD-160 hash functions. This produces a 20-byte hash known as the "hash160."

2. Adding Version Byte: A version byte is added to the hash160. This byte helps to identify the network for which the address is valid (e.g., mainnet or testnet).

3. Double Hashing: The hash160 with the version byte is double-hashed using the SHA-256 hash function twice. The first 4 bytes of the resulting hash are taken as the "checksum".

4. Base58 Encoding: The version byte + hash160 + checksum are combined, and the resulting data is encoded in Base58 format. Base58 is used to avoid confusion between characters (excludes similar-looking characters like 0, O, l, I) and creates a human-readable Bitcoin address.
