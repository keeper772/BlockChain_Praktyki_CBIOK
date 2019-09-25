import hashlib
import random
import datetime
import subprocess
import time
import string
import signal
import sys
#---------------------------------------------------------------
#SIGNAL HANDLER FOR TERMINATING JOBS AND SAVE PROGRESS
#---------------------------------------------------------------
def signal_handler(sig, frame):
        print "Ctrl + C detected. Dumping blockchain to file"
        a.toFile()
        print "DONE"
        print "Terminating all miners"
        process = subprocess.Popen("condor_rm -all", shell=True, stdout=subprocess.PIPE)
        print "Waiting for all jobs termination"
		time.sleep(15)
        print "DONE"
        sys.exit(0)
        
signal.signal(signal.SIGINT, signal_handler)
#---------------------------------------------------------------
#---------------------------------------------------------------
#BLOCK CLASS FOR SINGLE BLOCK IN BLOCKCHAIN
#---------------------------------------------------------------
class Block:
	def __init__(this, previous_hash, difficulty):
		this.previous_hash = previous_hash
		this.data = ""
		this.difficulty = difficulty
		this.hash = ""
		this.salt = ""
		
	def addData(this, data):
		this.data += str(data)
		
	##CHECKS IF GIVEN SALT IS VALID FOR BLOCK
	def validateHash(this, salt):
		prefix_of_zeros = ""
		for i in range(this.difficulty):
			prefix_of_zeros += '0'
		block_to_prove = hashlib.sha256()
		this.salt = salt
		data_to_prove = this.previous_hash + str(this.difficulty) + this.data + this.salt
		block_to_prove.update(data_to_prove)
		hash = block_to_prove.hexdigest()
		print hash
		if hash[:this.difficulty] == prefix_of_zeros:
			this.hash = hash
			return True
		else:
			this.salt = ""
			return False
	
	def toString(this):
		print "Previous block hash: " + this.previous_hash
		print "Difficulty: " + str(this.difficulty)
		print "Data in block: " + this.data
		print "Salt: " + this.salt
		print "Block Hash: " + this.hash + "\n\n"

	def toFile(this, blockchain_file):
		blockchain_file.write(this.previous_hash + "\n")
		blockchain_file.write(str(this.difficulty) + "\n")
		blockchain_file.write(this.data + "\n")
		blockchain_file.write(this.salt + "\n")
		blockchain_file.write(this.hash + "\n")

#---------------------------------------------------------------
#---------------------------------------------------------------
#BLOCKCHAIN CLASS, CONTAINS LIST OF BLOCKS
#---------------------------------------------------------------	
class BlockChain():
	#THERE ARE TWO OPTIONS, IF ONE ARGUMENT GIVEN IT IS CONSIDERED AS PATH TO BLOCKAIN FILE
	#IF THERE IS NO ARGUMENT IT WILL CREATE NEW BLOCKCHAIN STARTING AT GENESIS BLOCK
	def __init__(this, *args):
		if len(args) == 1:
			with open(args[0], 'r') as blockchain_file:
				this.blockchain = []
				temp_previous_hash = blockchain_file.readline()[:-1]
				while temp_previous_hash:
					this.difficulty = int(blockchain_file.readline())
					this.blockchain.append(Block(temp_previous_hash, this.difficulty))
					this.blockchain[-1].data = blockchain_file.readline()[:-1]
					this.blockchain[-1].salt = blockchain_file.readline()[:-1]
					this.blockchain[-1].hash = blockchain_file.readline()[:-1]
					temp_previous_hash = blockchain_file.readline()[:-1]
			this.temporary_block = Block(this.blockchain[-1].hash, this.difficulty)
		else:
			#STARTING DIFFICULTY
			this.difficulty = 5
			#LIST OF BLOCKS IN BLOCKCHAIN
			this.blockchain = []
			#CREATING GENESIS BLOCK
			this.temporary_block(Block('0000000000000000000000000000000000000000000000000000000000000000', this.difficulty))
			this.temporary_block.addData("Genesis Block " + randomData(10))
			#MINING GENESIS BLOCK
			this.calculateAndAddCurrentBlock()
			#FIXING DIFFICULTY TO NORMAL LEVEL
			this.difficulty = 9
			this.temporary_block.difficulty = this.difficulty
	#MINING BLOCKS		
	def calculateAndAddCurrentBlock(this):
		print "Creating arguments for miners"
		arguments_for_miner = this.temporary_block.previous_hash + " " + str(this.difficulty) + " " + this.temporary_block.data
		with open('submit.sample', 'r') as file :
			filedata = file.read()
		
		filedata = filedata.replace('ARGS', arguments_for_miner)
		
		with open('miner.submit', 'w') as file:
			file.write(filedata)
		print "DONE"
		print "Starting mining script"
		#MINING SCRIPT CONTAINS CONDOR COMMANDS FOR SUBMIT JOB AND WAIT UNTIL AT LEAST ONE JOB IS DONE
		process = subprocess.Popen("./submit.sh", shell=True, stdout=subprocess.PIPE)
		process.wait()
		print "DONE"
		print "DONE"
		print "Verifying calculated hash"	
		with open('miner.out', 'r') as salt_result:
			calculated_salt = salt_result.readline()[:-1]
			if this.temporary_block.validateHash(calculated_salt):
				this.blockchain.append(this.temporary_block)
				print "Block is valid. Saving blockchain to file"
				a.toFile()
				print "DONE"
				#IF SALT RETURNED BY MINERS IS CORRECT, TERMINATES ALL JOBS
				print "Terminating all miners"
				process = subprocess.Popen("condor_rm -all", shell=True, stdout=subprocess.PIPE)
				print "Waiting for all jobs termination"
				time.sleep(20)
		print "DONE"
		this.temporary_block = Block(this.blockchain[-1].hash, this.difficulty)
	
	def showBlock(this, id):
		print "Block number: " + str(id)	
		this.blockchain[id].toString()
		
	def addDataToNewBlock(this, data):
		this.temporary_block.addData(data)
		
	def toString(this):
		for i in range(len(this.blockchain)):
			this.showBlock(i)
			
	def toStringWithTempraryBlock(this):
		this.toString()
		this.temporary_block.toString()

	def toFile(this):
		with open('blockchain', 'w') as blockchain_file:
			for block in this.blockchain:
				block.toFile(blockchain_file)
#--------------------------------------------------------------------
#RETURN SOME RANDOM GARBAGE DATA		
def randomData(length):
	letters = string.ascii_lowercase
	return ''.join(random.choice(letters) for i in range(length))

print "Simple blockchain calculating on HTCondor"
print "1 - Create new blockchain"
print "2 - Restore blockchain from file"
choice = raw_input(">")
if choice == '1':
	print "Creating blockchain"
	a = BlockChain()
elif choice == '2':
	blockchain_file_name = raw_input("Type blockchain file name: ")
	a = BlockChain(blockchain_file_name)
else:
	print "ERROR"
	exit()
#ENDLESSLY GENERATES NEW BLOCK UNTIL CTRL + C IS PRESSED
while True:
	some_random_data = randomData(200)
	#ADDING SOME RANDOM DATA TO SHOW CONCEPT OF BLOCKCHAIN
	#IT CAN BE ANYTHING WHAT MAKES IT USEFUL
	a.addDataToNewBlock(some_random_data)
	a.calculateAndAddCurrentBlock()
