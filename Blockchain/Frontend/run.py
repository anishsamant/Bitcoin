from flask import Flask, render_template, request
from Blockchain.client.sendBTC import sendBTC
from Blockchain.Backend.core.tx import Tx

app = Flask(__name__)

@app.route('/', methods = ["GET", "POST"])
def wallet():
    message = ''
    if request.method == "POST":
        fromAddress = request.form.get("fromAddress")
        toAddress = request.form.get("toAddress")
        amount = request.form.get("amount", type = int)
        sendCoin = sendBTC(fromAddress, toAddress, amount, UTXOs)
        txObj = sendCoin.prepareTransaction()
        script_pubkey = sendCoin.scriptPubkey(fromAddress)
        verified = True

        if not txObj:
            message = "Invalid Transaction"
            
        if isinstance(txObj, Tx):
            for index, tx in enumerate(txObj.tx_inputs):
                if not txObj.verify_input(index, script_pubkey):
                    verified = False

            if verified:
                MEMPOOL[txObj.txId] = txObj
                message = "Transaction added in memory pool"

    return render_template('wallet.html', message = message)

def main(utxos, mempool):
    global UTXOs
    global MEMPOOL
    UTXOs = utxos
    MEMPOOL = mempool
    app.run()