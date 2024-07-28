import hashlib
import time
import random
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

class Block:
    def __init__(self, index, previous_hash, timestamp, data, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        return hashlib.sha256(f"{self.index}{self.previous_hash}{self.timestamp}{self.data}{self.nonce}".encode()).hexdigest()

    def __repr__(self):
        return (f"Block(index={self.index}, previous_hash={self.previous_hash}, "
                f"timestamp={self.timestamp}, data={self.data}, nonce={self.nonce}, hash={self.hash})")

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "0", time.time(), "Genesis Block")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

    def print_chain(self):
        return [block for block in self.chain] if self.chain else []

class BlockchainWithPoW(Blockchain):
    difficulty = 4

    def mine_block(self, block):
        while block.hash[:self.difficulty] != "0" * self.difficulty:
            block.nonce += 1
            block.hash = block.calculate_hash()
        return block

    def add_block(self, new_block):
        new_block = self.mine_block(new_block)
        super().add_block(new_block)

class BlockchainWithDPoS(Blockchain):
    def __init__(self):
        super().__init__()
        self.stakers = {}
        self.delegates = []

    def add_stake(self, address, amount):
        if address in self.stakers:
            self.stakers[address] += amount
        else:
            self.stakers[address] = amount
        self.update_delegates()

    def update_delegates(self):
        self.delegates = sorted(self.stakers, key=self.stakers.get, reverse=True)[:5]

    def select_validator(self):
        if not self.delegates:
            return None
        return random.choice(self.delegates)

    def add_block(self, new_block):
        validator = self.select_validator()
        if validator in self.delegates:
            super().add_block(new_block)
            print(f"Block added to DPoS blockchain by validator: {validator}")
        else:
            print("No valid delegate found. Block not added to DPoS blockchain.")

class HealthDataBlock(Block):
    def __init__(self, index, previous_hash, timestamp, patient_data, nonce=0):
        self.patient_data = patient_data
        super().__init__(index, previous_hash, timestamp, str(patient_data), nonce)

# Initialize blockchains
blockchain_pow = BlockchainWithPoW()
blockchain_dpos = BlockchainWithDPoS()

# HTML and CSS Templates
index_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BLockchain in Healthcare</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            padding: 20px;
        }
        h1 {
            text-align: center;
        }
        .blockchain {
            margin-bottom: 40px;
        }
        .block {
            border: 1px solid #ccc;
            padding: 10px;
            margin-bottom: 10px;
        }
        .block p {
            margin: 5px 0;
        }
        .block span {
            font-weight: bold;
        }
        .form-group {
            margin-bottom: 15px;
        }
        .form-group label {
            display: block;
            margin-bottom: 5px;
        }
        .form-group input, .form-group textarea {
            width: 100%;
            padding: 8px;
            box-sizing: border-box;
        }
        .form-group button {
            padding: 10px 15px;
            background-color: #007bff;
            color: #fff;
            border: none;
            cursor: pointer;
        }
        .stakers {
            margin-bottom: 40px;
        }
    </style>
</head>
<body>
    <h1>Blockchain in Healthcare</h1>
    <div class="blockchain">
        <h2>Proof of Work Blockchain</h2>
        {% for block in pow_chain %}
        <div class="block">
            <p><span>Index:</span> {{ block.index }}</p>
            <p><span>Previous Hash:</span> {{ block.previous_hash }}</p>
            <p><span>Timestamp:</span> {{ block.timestamp }}</p>
            <p><span>Data:</span> {{ block.data }}</p>
            <p><span>Nonce:</span> {{ block.nonce }}</p>
            <p><span>Hash:</span> {{ block.hash }}</p>
        </div>
        {% endfor %}
    </div>
    <div class="blockchain">
        <h2>Delegated Proof of Stake Blockchain</h2>
        {% for block in dpos_chain %}
        <div class="block">
            <p><span>Index:</span> {{ block.index }}</p>
            <p><span>Previous Hash:</span> {{ block.previous_hash }}</p>
            <p><span>Timestamp:</span> {{ block.timestamp }}</p>
            <p><span>Data:</span> {{ block.data }}</p>
            <p><span>Nonce:</span> {{ block.nonce }}</p>
            <p><span>Hash:</span> {{ block.hash }}</p>
        </div>
        {% endfor %}
    </div>
    <div class="stakers">
        <h2>Stakers</h2>
        {% for address, amount in stakers.items() %}
        <p><span>Address:</span> {{ address }} <span>Stake:</span> {{ amount }}</p>
        {% endfor %}
    </div>
    <h2>Add Block</h2>
    <form method="POST" action="{{ url_for('add_block') }}">
        <div class="form-group">
            <label for="patient_id">Patient ID:</label>
            <input type="text" id="patient_id" name="patient_id" required>
        </div>
        <div class="form-group">
            <label for="record">Record:</label>
            <textarea id="record" name="record" required></textarea>
        </div>
        <div class="form-group">
            <button type="submit">Add Block</button>
        </div>
    </form>
    <h2>Add Stake</h2>
    <form method="POST" action="{{ url_for('stake') }}">
        <div class="form-group">
            <label for="address">Address:</label>
            <input type="text" id="address" name="address" required>
        </div>
        <div class="form-group">
            <label for="amount">Amount:</label>
            <input type="number" id="amount" name="amount" required>
        </div>
        <div class="form-group">
            <button type="submit">Add Stake</button>
        </div>
    </form>
</body>
</html>
"""

@app.route('/')
def index():
    pow_chain = blockchain_pow.print_chain() or []
    dpos_chain = blockchain_dpos.print_chain() or []
    stakers = blockchain_dpos.stakers or {}
    return render_template_string(index_html, pow_chain=pow_chain, dpos_chain=dpos_chain, stakers=stakers)

@app.route('/add_block', methods=['GET', 'POST'])
def add_block():
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        record = request.form['record']
        patient_data = {"patient_id": patient_id, "record": record}
        
        # Adding to PoW blockchain
        new_block_pow = HealthDataBlock(len(blockchain_pow.chain), blockchain_pow.get_latest_block().hash, time.time(), patient_data)
        blockchain_pow.add_block(new_block_pow)
        
        # Adding to DPoS blockchain
        new_block_dpos = HealthDataBlock(len(blockchain_dpos.chain), blockchain_dpos.get_latest_block().hash, time.time(), patient_data)
        validator = blockchain_dpos.select_validator()
        if validator:
            blockchain_dpos.add_block(new_block_dpos)
        
        return redirect(url_for('index'))
    return redirect(url_for('index'))

@app.route('/stake', methods=['GET', 'POST'])
def stake():
    if request.method == 'POST':
        address = request.form['address']
        amount = int(request.form['amount'])
        blockchain_dpos.add_stake(address, amount)
        return redirect(url_for('index'))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
