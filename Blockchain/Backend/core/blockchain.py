import sys
sys.path.append('/Legion_Files/Anish/Projects/MyProjects/Bitcoin')

from Blockchain.Backend.core.block import Block
from Blockchain.Backend.core.blockheader import BlockHeader
from Blockchain.Backend.util.util import hash256
from Blockchain.Backend.core.database.database import BlockchainDB
from Blockchain.Backend.core.tx import CoinbaseTx
import time

ZERO_HASH = '0' * 64
VERSION = 1

class Blockchain:
    def __init__(self):
        self.genesisBlock()

    # function to write data to disk
    def writeToDisk(self, block):
        blockchainDB = BlockchainDB()
        blockchainDB.write(block)

    # function to fetch last block data from disk
    def fetchLastBlock(self):
        blockchainDB = BlockchainDB()
        return blockchainDB.lastBlock()

    # function to create genesis block
    def genesisBlock(self):
        blockHeight = 0
        prevBlockHash = ZERO_HASH
        self.addBlock(blockHeight, prevBlockHash)

    # function to add Block to blockchain
    def addBlock(self, blockHeight, prevBlockHash):
        timestamp = int(time.time())
        coinbaseInstance = CoinbaseTx(blockHeight)
        coinbaseTx = coinbaseInstance.coinbaseTransaction()
        
        merkleRoot = ''
        bits = 'ffff001f'
        blockHeader = BlockHeader(VERSION, prevBlockHash, merkleRoot, timestamp, bits)
        blockHeader.mine()
        self.writeToDisk([Block(blockHeight, 1, blockHeader.__dict__, 1, coinbaseTx.to_dict()).__dict__])

    # iterative function to create blocks
    def main(self):
        while True:
            lastBlock = self.fetchLastBlock()
            blockHeight = lastBlock['height'] + 1
            prevBlockHash = lastBlock['blockHeader']['blockHash']
            self.addBlock(blockHeight, prevBlockHash)

if __name__ == "__main__":
    blockchain = Blockchain()
    blockchain.main()
