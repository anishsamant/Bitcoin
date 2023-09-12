from Blockchain.Backend.core.script import Script
from Blockchain.Backend.util.util import int_to_little_endian, bytes_needed, decode_base58, little_endian_to_int, encode_varint, hash256

ZERO_HASH = b'\0' * 32
REWARD = 50
PRIVATE_KEY = '6415168560025015419828792186365996364777874576344984328293555123949832143928'
MINER_ADDRESS = '1MaKZWUdKdo8qbLLYxYVmp1Thu7nXxL4xQ'
SIGHASH_ALL = 1

class CoinbaseTx:
    def __init__(self, blockHeight):
        self.blockHeightInLittleEndian = int_to_little_endian(blockHeight, bytes_needed(blockHeight))

    def coinbaseTransaction(self):
        prev_tx = ZERO_HASH
        prev_index = 0xffffffff
        tx_inputs = []
        tx_inputs.append(TxInput(prev_tx, prev_index))
        tx_inputs[0].script_sig.cmds.append(self.blockHeightInLittleEndian)

        tx_outputs = []
        target_amount = REWARD * 100000000
        target_hash160 = decode_base58(MINER_ADDRESS)
        target_script = Script.p2pkh_script(target_hash160)
        tx_outputs.append(TxOutput(amount = target_amount, script_pubkey=target_script))
        coinbaseTx = Tx(1, tx_inputs, tx_outputs, 0)
        coinbaseTx.txId = coinbaseTx.id()
        
        return coinbaseTx

class Tx:
    def __init__(self, version, tx_inputs, tx_outputs, locktime):
        self.version = version
        self.tx_inputs = tx_inputs
        self.tx_outputs = tx_outputs
        self.locktime = locktime

    # function to generate human readable tx-id
    def id(self):
        return self.hash().hex()

    # function to generate binary hash of serialization
    def hash(self):
        return hash256(self.serialize())[::-1]

    # function to serialize our data
    def serialize(self):
        result = int_to_little_endian(self.version, 4)
        
        result += encode_varint(len(self.tx_inputs))
        for tx_in in self.tx_inputs:
            result += tx_in.serialize()

        result += encode_varint(len(self.tx_outputs))
        for tx_out in self.tx_outputs:
            result += tx_out.serialize()

        result += int_to_little_endian(self.locktime, 4)

        return result
    
    # function to generate signature hash of transaction input
    def sig_hash(self, input_index, script_pubkey):
        sigh = int_to_little_endian(self.version, 4)

        sigh += encode_varint(len(self.tx_inputs))
        for i, tx_in in enumerate(self.tx_inputs):
            if i == input_index:
                sigh += TxInput(tx_in.prev_tx, tx_in.prev_index, script_pubkey).serialize()
            else:
                sigh += TxInput(tx_in.prev_tx, tx_in.prev_index).serialize()

        sigh += encode_varint(len(self.tx_outputs))
        for tx_out in self.tx_outputs:
            sigh += tx_out.serialize()

        sigh += int_to_little_endian(self.locktime, 4)
        sigh += int_to_little_endian(SIGHASH_ALL, 4)

        h256 = hash256(sigh)
        return int.from_bytes(h256, 'big')
    
    # function to sign transaction input
    def sign_input(self, input_index, private_key, script_pubkey):
        signature_hash = self.sig_hash(input_index, script_pubkey)
        der = private_key.sign(signature_hash).der()
        sig = der + SIGHASH_ALL.to_bytes(1, 'big')
        sec = private_key.point.sec()   # gives compressed public key
        self.tx_inputs[input_index].script_sig = Script([sig, sec])

    # function to verify transaction input
    def verify_input(self, input_index, script_pubkey):
        txIn = self.tx_inputs[input_index]
        z = self.sig_hash(input_index, script_pubkey)
        combined = txIn.script_sig + script_pubkey
        return combined.evaluate(z)

    # function to check if transaction is a coinbase transaction or not
    def is_coinbase(self):
        """
        # Check if there us exactly 1 input
        # grab the first input and check if the prev_tx is b'\x00' * 32
        # check that the first input prev_index is 0xffffffff
        """

        if len(self.tx_inputs) != 1:
            return False

        first_input = self.tx_inputs[0]
        if first_input.prev_tx != b"\x00" * 32:
            return False

        if first_input.prev_index != 0xffffffff:
            return False

        return True

    # function to convert to dictionary type
    def to_dict(self):
        """
        Convert Transaction Input to dict
         # Convert prev_tx Hash in hex from bytes
         # Convert Blockheight in hex which is stored in Script signature
        """
        
        if self.is_coinbase():
            self.tx_inputs[0].prev_tx = self.tx_inputs[0].prev_tx.hex()
            self.tx_inputs[0].script_sig.cmds[0] = little_endian_to_int(self.tx_inputs[0].script_sig.cmds[0])
            self.tx_inputs[0].script_sig = self.tx_inputs[0].script_sig.__dict__   

        self.tx_inputs[0] = self.tx_inputs[0].__dict__ 

        """
         Convert Transaction Output to dict
          # If there are Numbers we don't need to do anything
          # If values is in bytes, convert it to hex
          # Loop through all the TxOut Objects and convert them into dict 
        """
        self.tx_outputs[0].script_pubkey.cmds[2] = self.tx_outputs[0].script_pubkey.cmds[2].hex()
        self.tx_outputs[0].script_pubkey = self.tx_outputs[0].script_pubkey.__dict__
        self.tx_outputs[0] = self.tx_outputs[0].__dict__

        return self.__dict__
        

class TxInput:
    def __init__(self, prev_tx, prev_index, script_sig = None, sequence = 0xffffffff):
        self.prev_tx = prev_tx
        self.prev_index = prev_index
        self.script_sig = Script() if script_sig == None else script_sig
        self.sequence = sequence

    # function to serialize tx_input object parameters
    def serialize(self):
        result = self.prev_tx[::-1]
        result += int_to_little_endian(self.prev_index, 4)
        result += self.script_sig.serialize()
        result += int_to_little_endian(self.sequence, 4)

        return result

class TxOutput:
    def __init__(self, amount, script_pubkey):
        self.amount = amount
        self.script_pubkey = script_pubkey  # to who we are sending

    def serialize(self):
        result = int_to_little_endian(self.amount, 8)
        result += self.script_pubkey.serialize()

        return result