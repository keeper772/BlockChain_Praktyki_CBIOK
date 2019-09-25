#!/usr/bin/env python
import hashlib
import random
import json
import datetime
import sys
import string

#PYTHON FILE WHICH IS GOING TO BE RUN ON MINERS

#GENERATING SOME RANDOM DATA
def randomData(length):
	letters = string.ascii_lowercase
	return ''.join(random.choice(letters) for i in range(length))

#READING ARGUMENTS FROM STDIN CALLED FROM CONDOR SUBMIT FILE
previous_hash = sys.argv[1]
difficulty = int(sys.argv[2])
data = sys.argv[3]

#LOOKING FOR VALID SALT
prefix_of_zeros = ""
for i in range(difficulty):
	prefix_of_zeros += '0'
block_to_prove = hashlib.sha256()
salt = randomData(100)
data_to_prove = previous_hash + str(difficulty) + data + salt
block_to_prove.update(data_to_prove)
block_hash = block_to_prove.hexdigest()
while block_hash[:difficulty] != prefix_of_zeros:
	block_to_prove = hashlib.sha256()
	salt = randomData(100)
	data_to_prove = previous_hash + str(difficulty) + data + salt
	block_to_prove.update(data_to_prove)
	block_hash = block_to_prove.hexdigest()

#RETURN RESULT ON STDOUT
print salt

