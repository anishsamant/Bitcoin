from Blockchain.Backend.core.script import Script
from Blockchain.Backend.util.util import int_to_little_endian, bytes_needed, decode_base58, little_endian_to_int

ZERO_HASH = b'\0' * 32
REWARD = 50
PRIVATE_KEY = '6415168560025015419828792186365996364777874576344984328293555123949832143928'
MINER_ADDRESS = '1MaKZWUdKdo8qbLLYxYVmp1Thu7nXxL4xQ'

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

        return Tx(1, tx_inputs, tx_outputs, 0)

class Tx:
    def __init__(self, version, tx_inputs, tx_outputs, locktime):
        self.version = version
        self.tx_inputs = tx_inputs
        self.tx_outputs = tx_outputs
        self.locktime = locktime

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

class TxOutput:
    def __init__(self, amount, script_pubkey):
        self.amount = amount
        self.script_pubkey = script_pubkey  # to who we are sending