# Blockchain-In-Healthcare
This project demonstrates the use of blockchain technology in the healthcare sector. It implements two types of blockchain consensus mechanisms: Proof of Work (PoW) and Delegated Proof of Stake (DPoS). The project aims to securely store and manage patient health records using blockchain, ensuring data integrity, transparency, and security.

Introduction
The "Blockchain in Healthcare" project explores the potential of blockchain technology in enhancing the security and transparency of healthcare data management. By utilizing PoW and DPoS consensus mechanisms, this project ensures robust security through computational effort and efficient block validation through stakeholder trust.

FEATURES
- [ ] PROOF OF WORK (PoW) BLOCKHAIN : Ensures data security through computational efforts.
- [ ] DELEGATED PROOF OF STAKE (DPoS) BLOCKCHAIN : Provides an energy-efficient and faster alternative by leveraging stakeholder trust.
- [ ] WEB INTERFACES : Allows adding patient records, staking tokens, and viewing blockchain data.
PREREQUISITIES
- [ ] Python 3.x
- [ ] Flask
- [ ] hashlib
- [ ] time
- [ ] random

CLASSES AND METHODS
BLOCK
* Attributes:
    * index: Index of the block.
    * previous_hash: Hash of the previous block.
    * timestamp: Timestamp of the block creation.
    * data: Data stored in the block.
    * nonce: Nonce value used for PoW.
    * hash: Hash of the block.
* Methods:
    * calculate_hash(): Calculates the hash of the block.
Blockchain
* Attributes:
    * chain: List of blocks.
* Methods:
    * create_genesis_block(): Creates the genesis block.
    * get_latest_block(): Returns the latest block in the chain.
    * add_block(new_block): Adds a new block to the chain.
    * print_chain(): Returns the entire blockchain.
BlockchainWithPoW (inherits Blockchain)
* Attributes:
    * difficulty: Difficulty level for PoW.
* Methods:
    * mine_block(block): Mines a block by finding the appropriate nonce.
    * add_block(new_block): Mines and adds a block to the chain.
BlockchainWithDPoS (inherits Blockchain)
* Attributes:
    * stakers: Dictionary of stakers and their stakes.
    * delegates: List of selected delegates.
* Methods:
    * add_stake(address, amount): Adds stake for an address.
    * update_delegates(): Updates the list of delegates.
    * select_validator(): Selects a validator from the delegates.
    * add_block(new_block): Adds a block to the chain if a valid delegate is found.
HealthDataBlock (inherits Block)
* Attributes:
    * patient_data: Patient data stored in the block.

