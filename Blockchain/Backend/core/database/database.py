import os
import json

class BaseDB:
    def __init__(self):
        self.basePath = 'data'
        self.filePath = '/'.join((self.basePath, self.filename))

    # function to read from file
    def read(self):
        if not os.path.exists(self.filePath):
            print(f"File {self.filePath} not available")
            return False

        with open (self.filePath, 'r') as file:
            lines = file.readline()

        if len(lines) > 0:
            data = json.loads(lines)
        else:
            data = []

        return data

    # function to write to file
    def write(self, item):
        data = self.read()
        if data:
            data = data + item
        else:
            data = item

        with open(self.filePath, 'w+') as file:
            file.write(json.dumps(data))


class BlockchainDB(BaseDB):
    def __init__(self):
        self.filename = 'blockchain'
        super().__init__()

    def lastBlock(self):
        data = self.read()
        if data:
            return data[-1]
        

class AccountDB(BaseDB):
    def __init__(self):
        self.filename = 'account'
        super().__init__()