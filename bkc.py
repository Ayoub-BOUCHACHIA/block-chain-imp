import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

def calculate_hash(index, previous_hash, timestamp, data, nonce):
    return hashlib.sha256(f'{index}{previous_hash}{timestamp}{data}{nonce}'.encode('utf-8')).hexdigest()

def proof_of_work(block, difficulty):
    """Proof of Work: Calculate until the hash starts with leading zeros equal to difficulty."""
    nonce = 0
    computed_hash = calculate_hash(block.index, block.previous_hash, block.timestamp, block.data, nonce)
    while not computed_hash.startswith('0' * difficulty):
        nonce += 1
        computed_hash = calculate_hash(block.index, block.previous_hash, block.timestamp, block.data, nonce)
    return nonce, computed_hash

def create_genesis_block():
    return Block(0, '0', time.time(), 'Genesis Block', calculate_hash(0, '0', time.time(), 'Genesis Block', 0))

def create_new_block(prev_block, data, difficulty=4):
    index = prev_block.index + 1
    timestamp = time.time()
    new_block = Block(index, prev_block.hash, timestamp, data, '')
    nonce, hash = proof_of_work(new_block, difficulty)
    new_block.hash = hash
    return new_block

# Initialize the blockchain with the genesis block
blockchain = [create_genesis_block()]
previous_block = blockchain[0]

# Add blocks to the blockchain
def json_block_decoder(block_data):
    return Block(block_data['index'], block_data['previous_hash'], block_data['timestamp'], block_data['data'], block_data['hash'])

