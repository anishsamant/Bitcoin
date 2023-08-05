from Blockchain.Backend.util.util import decode_base58
from Blockchain.Backend.core.script import Script
from Blockchain.Backend.core.tx import TxInput, TxOutput, Tx
from Blockchain.Backend.core.database.database import AccountDB
from Blockchain.Backend.core.EllepticCurve.EllepticCurve import PrivateKey
import time

class sendBTC:
    def __init__(self, fromAccount, toAccount, amount, UTXOs):
        self.COINS = 100000000
        self.fromPublicAddress = fromAccount
        self.toAccount = toAccount
        self.amount = amount * self.COINS
        self.UTXOS = UTXOs

    def scriptPubkey(self, publicAddress):
        h160 = decode_base58(publicAddress)
        script_pubkey = Script().p2pkh_script(h160)

        return script_pubkey
    
    # function to retrieve private key of sender
    def getPrivateKey(self):
        allAcounts = AccountDB().read()
        for account in allAcounts:
            if account['publicAddress'] == self.fromPublicAddress:
                return account['privateKey']
    
    # furnction to create a transaction input
    def prepareTxIn(self):
        txIns = []
        self.total = 0

        # convert public address into public hash to find tx_outs that are locked to this hash
        self.from_script_pubkey = self.scriptPubkey(self.fromPublicAddress)
        self.fromPubkeyHash = self.from_script_pubkey.cmds[2]

        newutxos = {}

        try:
            while len(newutxos) < 1:
                newutxos = dict(self.UTXOS)
                time.sleep(2)
        except Exception as e:
            print(f"Error in converting managed dict to normal dict")

        for txByte in newutxos:
            if self.total < self.amount:
                txObj = newutxos[txByte]
                for index, txout in enumerate(txObj.tx_outputs):
                    if txout.script_pubkey.cmds[2] == self.fromPubkeyHash:
                        self.total += txout.amount
                        prev_tx = bytes.fromhex(txObj.id())
                        txIns.append(TxInput(prev_tx, index))
            else:
                break

        self.isBalanceEnough = True
        if self.total < self.amount:
            self.isBalanceEnough = False

        return txIns

    # function to create a transaction output
    def prepareTxOut(self):
        txOuts = []
        to_script_pubkey = self.scriptPubkey(self.toAccount)
        txOuts.append(TxOutput(self.amount, to_script_pubkey))

        # calculate fee that needs to be paid to miner to include transaction to block
        self.fee = self.COINS
        self.changeAmount = self.total - self.amount - self.fee
        txOuts.append(TxOutput(self.changeAmount, self.from_script_pubkey))

        return txOuts

    # function to sign transaction
    def signTx(self):
        secret = self.getPrivateKey()
        priv = PrivateKey(secret = secret)
        for index, input in enumerate(self.txIns):
            self.txObj.sign_input(index, priv, self.from_script_pubkey)

        return True
   
    # function to create a transaction
    def prepareTransaction(self):
        self.txIns = self.prepareTxIn()
        if self.isBalanceEnough:
            self.txOuts = self.prepareTxOut()
            self.txObj = Tx(1, self.txIns, self.txOuts, 0)
            self.signTx()
            return True
        
        return False