'''
    https://cryptobook.nakov.com/asymmetric-key-ciphers/elliptic-curve-cryptography-ecc

    Cryptography uses elliptic curves in a simplified form (Weierstras form), which is defined as:
    y2 = x3 + _a_x + b
    For example, the NIST curve secp256k1 (used in Bitcoin) is based on an elliptic curve in the form:
    y2 = x3 + 7 (the above elliptic curve equation, where a = 0 and b = 7)

'''

import sys
sys.path.append('/Legion_Files/Anish/Projects/MyProjects/Bitcoin')

from Blockchain.Backend.core.EllepticCurve.EllepticCurve import Sha256Point
from Blockchain.Backend.util.util import hash160, hash256
import secrets 

class Account:
    Pcurve = 2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 - 1
    Acurve = 0
    Bcurve = 7
    N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

    # function to create public private key pairs using elleptic curve cryptography
    def createKeys(self):  
        # compressed form
        Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
        Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
        G = Sha256Point(Gx, Gy)

        while True:
            privateKey = secrets.randbits(256)
            privateKeyHex = hex(privateKey)
            intN = int(self.N)
            if privateKey == 0 or privateKey >= intN:
                print("invalid private key. Generating another...")
            else:
                break
            
        uncompressedPublicKey = privateKey * G    
        xCordinate = uncompressedPublicKey.x
        yCordinate = uncompressedPublicKey.y

        if yCordinate.num % 2 == 0:
            compressedKey = b'\x02' + xCordinate.num.to_bytes(32, 'big')
        else:
            compressedKey = b'\x03' + xCordinate.num.to_bytes(32, 'big')

        hsh160 = hash160(compressedKey)
        # mainnet prefix
        mainnetPrefix = b'\x00'
        newAddress = mainnetPrefix + hsh160

        # check_sum
        checksum = hash256(newAddress)[:4]
        newAddress = newAddress + checksum

        # base58 
        BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

        # count leading zeros
        count = 0
        for val in newAddress:
            if val == 0:
                count += 1
            else:
                break

        # convert address to numeric form
        num = int.from_bytes(newAddress, 'big')
        prefix = '1' * count
        result = ''
        while num > 0:
            num, mod = divmod(num, 58)
            result = BASE58_ALPHABET[mod] + result

        publicAddress = prefix + result

        print(f"private key: {privateKey}")
        print(f"private key hex: {privateKeyHex}")
        print(f"uncompresed public key: {uncompressedPublicKey}")
        print(f"Public Address {publicAddress}")

if __name__ == '__main__':
    account = Account()
    account.createKeys()

