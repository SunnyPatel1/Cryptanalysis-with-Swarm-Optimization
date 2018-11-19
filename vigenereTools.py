import numpy as np
import pickle
from string import punctuation

def prepInput(toPrep):
    for char in punctuation:
        toPrep = toPrep.replace(char, '')
        toPrep = toPrep.replace(char, '')

    prepped = toPrep.replace("\n", '').replace(" ", '').upper()
    return prepped
    
def assignNumeric(alpha):
    return (ord(alpha) - (ord('@')+1))

def extendCipherText(arr, factor, length):

    return np.tile(arr, factor+1)[:length]

def assignAlpha(num):
    return chr(ord('@') + 1 + num)

def encrypt(plain, key):
    return np.asarray([encryptSingle(p,k) for p,k in zip(plain, key)])

def encryptSingle(m, k):
    return (m + k)%26

def toString(arr):
    return "".join([assignAlpha(num) for num in arr])

def toNumArray(string):
    return np.asarray([assignNumeric(alpha) for alpha in string])

def decryptSingle(c, k):
    return (c - k)%26

def decrypt(cipherText, key):
    return np.asarray([decryptSingle(c, k) for c, k in zip(cipherText, key)])

def getMonogram():
    return monogram

def getBigram():
    return bigram

def getObservedMonogram(decrypt):
    f = open('monogram.pckl', 'rb')
    monogram = pickle.load(f)
    f.close()
    observedMono = dict.fromkeys(monogram, 0.0)
    total = 0
    for x in range(0, len(decrypt)):
        observedMono[assignAlpha(decrypt[x])] += 1
        total += 1
    observedMono = { key: float(value/total) for key, value in observedMono.items() }
    return observedMono


def getObservedBigram(decrypt):
    f = open('bigram.pckl', 'rb')
    bigram = pickle.load(f)
    f.close()
    observedMono = dict.fromkeys(bigram, 0.0)
    total = 0
    for x in range(0, len(decrypt)-1):
        observedMono[""+
                     assignAlpha(decrypt[x])+
                     assignAlpha(decrypt[x+1])] += 1
        total += 1
    observedBi = { key: float(value/total) for key, value in observedMono.items() }
    return observedBi

def getFitness(decrypt):
    observedMono = getObservedMonogram(decrypt)
    observedBi = getObservedBigram(decrypt)
    f = open('monogram.pckl', 'rb')
    englishMono = pickle.load(f)
    f.close()
    f = open('bigram.pckl','rb')
    englishBi = pickle.load(f)
    f.close()

    diffMono = []
    for key, value in observedMono.items():
        diffMono.append( abs(englishMono[key] - value) )

    diffBi = []
    for key, value in observedBi.items():
        diffBi.append( abs(englishBi[key] - value) )
        
    fitness = 0.23*sum(diffMono) + 0.77*sum(diffBi)
    return fitness

#f = open('bigram.pckl', 'rb')
#bigram = pickle.load(f)
#f.close()
def testFitnessFunction():
    testFile = open('plain-text.txt', 'r')
    content = testFile.read()
    content = prepInput(content)
    numArray = toNumArray(content)
    fitness = getFitness(numArray)
    return fitness

if __name__ == "__main__":
    print(toString([17,8,5]))
    
