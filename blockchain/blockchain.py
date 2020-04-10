import hashlib
import json
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(previous_hash=1, proof=1234)

    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain

        A block should have:
        * Index
        * Timestamp
        * List of current transactions
        * The proof used to mine this block
        * The hash of the previous block

        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """

        block = {
           "Index":len(self.chain) + 1,
           "Timestamp":time() ,
           "Current_transactions":self.current_transactions ,
           "Proof_of_work":proof ,
           "Previous_hash":previous_hash or self.hash(self.chain[-1])
        }

        # Reset the current list of transactions
        self.current_transactions = []
        # Append the chain to the block
        self.chain.append(block)
        # Return the new block
        return block

    def hash(self, block):
        """
        Creates a SHA-256 hash of a Block

        :param block": <dict> Block
        "return": <str>
        """

        # Use json.dumps to convert json into a string
        # Use hashlib.sha256 to create a hash
        # It requires a `bytes-like` object, which is what
        # .encode() does.
        # It converts the Python string into a byte string.
        # We must make sure that the Dictionary is Ordered,
        # or we'll have inconsistent hashes

        # TODO: Create the block_string
        string_block = json.dumps(block,sort_keys = True)
        # TODO: Hash this string using sha256
        raw_hash = hashlib.sha256(string_block.encode())
        # By itself, the sha256 function returns the hash in a raw string
        # that will likely include escaped characters.
        # This can be hard to read, but .hexdigest() converts the
        # hash to a string of hexadecimal characters, which is
        # easier to work with and understand
        hex_hash = raw_hash.hexdigest()

        # TODO: Return the hashed block string in hexadecimal format
        return hex_hash

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self):
        """
        Simple Proof of Work Algorithm
        Stringify the block and look for a proof.
        Loop through possibilities, checking each one against `valid_proof`
        in an effort to find a number that is a valid proof
        :return: A valid proof for the provided block
        """
        
        proof = 0
        while self.valid_proof(self.last_block, proof) is False:
            proof += 1
        return proof
    @staticmethod
    def valid_proof(block,proof):
        """
        Validates the Proof:  Does hash(block_string, proof) contain 3
        leading zeroes?  Return true if the proof is valid
        :param block_string: <string> The stringified block to use to
        check in combination with `proof`
        :param proof: <int?> The value that when combined with the
        stringified previous block results in a hash that has the
        correct number of leading zeroes.
        :return: True if the resulting hash is a valid proof, False otherwise
        """
        block_string = json.dumps(block,sort_keys = True)
        guess = f'{block_string}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        last_block_string = json.dumps(block, sort_keys=True)
        last_proof = block['Proof_of_work']
        last_block_guess = f'{block}{last_proof}'.encode()
        last_block_guess_hash = hashlib.sha256(last_block_guess).hexdigest()
        return guess_hash[:1] == last_block_guess_hash[:-1]


# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    # Run the proof of work algorithm to get the next proof
    new_proof = blockchain.proof_of_work()
    if blockchain.valid_proof(blockchain.last_block,new_proof):
        previous_hash = blockchain.hash(blockchain.last_block)
        new_block = blockchain.new_block(new_proof,previous_hash)
        response = {
            'new_block':new_block
        }

        return jsonify(response), 200
    else:
        response: {"message":"proof not valid"}
        return jsonify(response), 400


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
       'chain' : blockchain.chain,
       'length' : len(blockchain.chain)
    }
    return jsonify(response), 200
@app.route('/last_block', methods=['GET'])
def return_last_block():
    response = {
        'last_block' : blockchain.last_block
    }
    return jsonify(response), 200


# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)