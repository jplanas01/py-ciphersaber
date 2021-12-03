#! /usr/bin/env python

import os

#key = "".join([chr(int(x,16)) for x in plaintext.split()])
#key += iv
#plaintext = "".join([chr(int(x,16)) for x in plaintext.split()])

S = [i for i in xrange(0,256)]
def init_ksa(num_rounds, key, keylength):
	for i in xrange(num_rounds):
		j = 0
		for i in xrange(0,256):
			j = (j + S[i] + ord(key[i % keylength])) % 256
			S[i], S[j] = S[j], S[i]
	return S

def process_string(input, S):
	i = 0
	j = 0
	output = ""
	for byte in input:
		i = (i + 1) % 256
		j = (j + S[i]) % 256
		S[i], S[j] = S[j], S[i]
		K = S[(S[i] + S[j]) % 256]
		output += chr(K ^ ord(byte))
	return output

def encrypt_file(filename, key):
	iv = os.urandom(10)
	key += iv
	file = open(filename, 'rb')
	output = open(filename + '.cs1', 'wb')
	output.write(iv)
	output.write(process_string(file.read(), init_ksa(20, key, len(key))))

def decrypt_file(filename, key):
	file = open(filename, 'rb')
	iv = file.read(10)
	key += iv
	output = open(os.path.splitext(filename)[0], 'wb')
	output.write(process_string(file.read(), init_ksa(20, key, len(key))))
