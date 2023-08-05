from flask import Flask, render_template, request
from Blockchain.client.sendBTC import sendBTC

app = Flask(__name__)

@app.route('/', methods = ["GET", "POST"])
def wallet():
    message = ''
    if request.method == "POST":
        fromAddress = request.form.get("fromAddress")
        toAddress = request.form.get("toAddress")
        amount = request.form.get("amount", type = int)
        sendCoin = sendBTC(fromAddress, toAddress, amount, UTXOs)
        if not sendCoin.prepareTransaction():
            message = "Insufficient Balance"

    return render_template('wallet.html', message = message)

def main(utxos):
    global UTXOs
    UTXOs = utxos
    app.run()