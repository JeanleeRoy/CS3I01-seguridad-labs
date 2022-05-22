from cryptography.hazmat.primitives import hashes
from tail_recursion import tail_recursive, recurse
#import matplotlib.pyplot as plt
import time
import random
import math

def hash(msg: str):
	digest = hashes.Hash(hashes.SHA1())
	digest.update(msg.encode("unicode_escape"))
	return digest.finalize().hex()

example = "1:20:1303030600:jpazos@utec.edu.pe::McMybZIhxKXu57jd:ckvi"

## RECURSIVE HASHCASH

def recursiveHashCash(ver: int, bits: int, resource: str, iv: str, ctr: int):
	baseStr = makeBaseStr(ver, bits, getRTime(), resource, iv, ctr)
	hashed = hash(baseStr)

	if checkBits(hashed, bits):
		return hashed
	else:
		return recursiveHashCash(ver, bits, resource, iv, ctr)

def makeBaseStr(*args):
	return ':'.join([str(s) for s in args])

def checkBits(hashed: str, bits: int):
	bitCheck = bits//4
	return hashed[:bitCheck] == "0"*bitCheck

def getRTime():
	return int(time.time())+int(random.random()*10**8)


## RECURSIVE HASHCASH
# Apply tail recursion

@tail_recursive
def tailRecursiveHashCash(ver: int, bits: int, resource: str, iv: str, ctr: int):
    curTime = str(int(time.time()) + int(random.random()*10**7))
    baseStr = str(ver) + ':' + str(bits) + ':' + curTime + ':' + resource + ':' + iv + ':' + str(ctr)
    hashed = hash(baseStr)

    if checkBits(hashed, bits):
        return hashed
    recurse(ver, bits, resource, iv, ctr)


## ITERATIVE HASHCASH

def iterativeHashCash(ver: int, bits: int, resource: str, iv: str, ctr: int):
	while True:
		curTime = getRTime()
		baseStr = makeBaseStr(ver, bits, curTime, resource, iv, ctr)
		hashed = hash(baseStr)
		if checkBits(hashed, bits):
			return hashed


## ITERATIVE HASHCASH PARTIAL

def iterativeHashCashPartial(ver: int, bits: int, resource: str, iv: str, ctr: int):
	while True:
		baseStr = makeBaseStr(ver, bits, getRTime(), resource, iv, ctr)
		hashed = hash(baseStr)
		if checkBitsPartial(hashed, bits):
			return hashed

def checkBitsPartial(hashed: str, bits: int):
	bHashed = hextobin(hashed)
	return bHashed[:bits] == "0"*bits

def hextobin(h):
    return bin(int(h, 16))[2:].zfill(len(h) * 4)

