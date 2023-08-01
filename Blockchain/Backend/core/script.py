class Script:
    def __init__(self, cmds = None):
        self.cmds = [] if cmds == None else cmds

    @classmethod
    def p2pkh_script(cls, h160):
        # takes hash160and returns the p2pkh script public key
        return Script([0x76, 0xa9, h160, 0x88, 0xac])