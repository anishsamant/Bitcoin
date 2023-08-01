# Bitcoin Blockchain Replica
A Python-based blockchain replicating Bitcoin's core concepts. Features include a P2P network, broadcasting of transactions/blocks, block explorer, secure Bitcoin address creation via elliptic curve cryptography and more...

# Bitcoin Address Generation
Reference: https://cryptobook.nakov.com/asymmetric-key-ciphers/elliptic-curve-cryptography-ecc

1. Elleptic curve cryptography is used to generate the public private key pairs
2. NIST curve secp256k1 is used in Bitcoin

### Following are SECP256k1 domain parameters
T = (p, a, b, G, n, h) </br>
The cruve E: y<sup>2</sup> = x<sup>3</sup> + ax + b (mod p)
1. <b>p:</b> finite field with a finite number of elements, which is a prime number. Modulo p should be used in equation. </br>
p = FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFE FFFFFC2F </br>
p =  2<sup>256</sup> − 2<sup>32</sup> − 2<sup>9</sup> − 2<sup>8</sup> − 2<sup>7</sup> − 2<sup>4</sup> − 2<sup>4</sup> − 1

2. <b>a:</b> 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000
3. <b>b:</b> 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000007

4. <b>G:</b> The base point (predetermined point on elleptic curve that everyone uses to determine other points on the curve):
    - compressed form: </br>
    G = 02 79BE667E F9DCBBAC 55A06295 CE870B07 029BFCDB 2DCE28D9 59F2815B 16F81798
    - uncompressed form: </br>
    G = 04 79BE667E F9DCBBAC 55A06295 CE870B07 029BFCDB 2DCE28D9 59F2815B 16F81798 483ADA77 26A3C465 5DA4FBFC 0E1108A8 FD17B448 A6855419 9C47D08F FB10D4B8

5. <b>n:</b> determines what the maximum value is that can be turned into a private key. Any 256 bit number between [1, n-1] is a valid private key. </br>
n = FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFE BAAEDCE6 AF48A03B BFD25E8C D0364141

6. <b>h:</b>  01  

### Following steps are followed to generate human readable public address 
(refer [account.py](https://github.com/anishsamant/Bitcoin/blob/main/Blockchain/client/account.py) file for code)
1. <b>Private Key Generation:</b> First, a random private key (a large random number) is generated.
2. <b>Public Key Generation:</b> The private key is used to compute the corresponding public key using the elliptic curve multiplication.
3. <b>Encoding the Public Key:</b> The public key is then encoded in a specific format, usually in compressed form, to make it shorter and more efficient.
4. <b>Hashing the Public Key:</b> Next, the encoded compressed public key is hashed using the SHA-256 and RIPEMD-160 hash functions. This produces a 20-byte hash known as the "hash160."
5. <b>Adding Version Byte:</b> A version byte is added to the hash160. This byte helps to identify the network for which the address is valid (e.g., mainnet or testnet).
6. <b>Double Hashing:</b> The hash160 with the version byte is double-hashed using the SHA-256 hash function twice. The first 4 bytes of the resulting hash are taken as the "checksum".
7. <b>Base58 Encoding:</b> The version byte + hash160 + checksum are combined, and the resulting data is encoded in Base58 format. Base58 is used to avoid confusion between characters (excludes similar-looking characters like 0, O, l, I) and creates a human-readable Bitcoin address.
