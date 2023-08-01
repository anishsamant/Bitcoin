class Block:
    def __init__(self, height, blockSize, blockHeader, txCount, txs):
        self.height = height
        self.blockSize = blockSize
        self.blockHeader = blockHeader
        self.txCount = txCount
        self.txs = txs