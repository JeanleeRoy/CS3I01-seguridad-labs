# GITHUB REPO: https://github.com/JeanleeRoy/CS3I01-seguridad-labs/blob/master/lab5a/lab5a.ipynb

from cryptography.hazmat.primitives import hashes
import time

def hash(msg: str):
	digest = hashes.Hash(hashes.SHA1())
	digest.update(msg.encode("unicode_escape"))
	return digest.finalize().hex()

## RECURSIVE HASHCASH

def recursiveHashCash(ver: int, bits: int, resource: str, iv: str, ctr: int):
    baseStr = makeBaseStr(ver, bits, getRTime(), resource, iv, ctr)
    
    if checkBits(baseStr, bits):
        return baseStr
    else:
        return recursiveHashCash(ver, bits, resource, iv, ctr+1)

def makeBaseStr(*args):
	return f"{args[0]}:{args[1]}:{args[2]}:{args[3]}::{args[4]}:{args[5]}"

def checkBits(baseString: str, bits: int):
	hashed = hash(baseString)
	bitCheck = bits//4
	return hashed[:bitCheck] == "0"*bitCheck

def getRTime():
	return int(time.time())


## RECURSIVE HASHCASH
# tail_recursion: code taken from https://chrispenner.ca/posts/python-tail-recursion
class Recurse(Exception):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

def recurse(*args, **kwargs):
    raise Recurse(*args, **kwargs)
        
def tail_recursive(f):
    def decorated(*args, **kwargs):
        while True:
            try:
                return f(*args, **kwargs)
            except Recurse as r:
                args = r.args
                kwargs = r.kwargs
                continue
    return decorated

# Apply tail recursion
@tail_recursive
def tailRecursiveHashCash(ver: int, bits: int, resource: str, iv: str, ctr: int):
    baseStr = makeBaseStr(ver, bits, getRTime(), resource, iv, ctr)

    if checkBits(baseStr, bits):
        return baseStr
    recurse(ver, bits, resource, iv, ctr+1)


## ITERATIVE HASHCASH

def iterativeHashCash(ver: int, bits: int, resource: str, iv: str, ctr: int):
    while True:
        baseStr = makeBaseStr(ver, bits, getRTime(), resource, iv, ctr)
        ctr+=1
        if checkBits(baseStr, bits):
            return baseStr


## ITERATIVE HASHCASH PARTIAL

def iterativeHashCashPartial(ver: int, bits: int, resource: str, iv: str, ctr: int):
    while True:
        baseStr = makeBaseStr(ver, bits, getRTime(), resource, iv, ctr)
        ctr += 1
        if checkBitsPartial(baseStr, bits):
            return baseStr

def checkBitsPartial(baseString: str, bits: int):
	hashed = hash(baseString)
	bHashed = hextobin(hashed)
	return bHashed[:bits] == "0"*bits

def hextobin(h):
    return bin(int(h, 16))[2:].zfill(len(h) * 4)

