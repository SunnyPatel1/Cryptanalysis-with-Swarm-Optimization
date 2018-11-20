import numpy as np
import pickle
from string import punctuation

#Remove punctuation, spaces and newlines from plain-text code, and convert to all caps
def prepInput(toPrep):
    for char in punctuation:
        toPrep = toPrep.replace(char, '')
        toPrep = toPrep.replace(char, '')

    prepped = toPrep.replace("\n", '').replace(" ", '').upper()
    return prepped

#Map each letter to an integer, range [0,25] for A through Z   
def assignNumeric(alpha):
    return (ord(alpha) - (ord('@')+1))

#Repeat cipher key untill same length as plain-text to encode
def extendCipherText(arr, factor, length):

    return np.tile(arr, factor+1)[:length]

#assign each number to a letter
def assignAlpha(num):
    return chr(ord('@') + 1 + num)

#Map the encryption function to each number (representing a character) to encrypt it
def encrypt(plain, key):
    return np.asarray([encryptSingle(p,k) for p,k in zip(plain, key)])

#Encrypt a single number (representing a letter)
def encryptSingle(m, k):
    return (m + k)%26

#Convert the array of characters to a string
def toString(arr):
    return "".join([assignAlpha(num) for num in arr])

#Map the assignNumeric function to each address of the char array
def toNumArray(string):
    return np.asarray([assignNumeric(alpha) for alpha in string])

#Decrypt a single numbe (representing the letter)
def decryptSingle(c, k):
    return (c - k)%26
#Decrypt entire number array (with each number representing a letter)
def decrypt(cipherText, key):
    return np.asarray([decryptSingle(c, k) for c, k in zip(cipherText, key)])

#Get dictionary of monogram frequencies from pickle file
def getMonogram():
    return monogram

#Get dictionary of digram frequnecies from the pickle file
def getBigram():
    return bigram

#Calculate the observed monogram frequncy, save in dictionary
def getObservedMonogram(decrypt):
    f = open('assets/monogram.pckl', 'rb')
    monogram = pickle.load(f)
    f.close()
    observedMono = dict.fromkeys(monogram, 0.0)
    total = 0
    for x in range(0, len(decrypt)):
        observedMono[assignAlpha(decrypt[x])] += 1
        total += 1
    observedMono = { key: float(value/total) for key, value in observedMono.items() }
    return observedMono


#Calculate the observed bigram frequncy, save in dictionary
def getObservedBigram(decrypt):
    f = open('assets/bigram.pckl', 'rb')
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

#Get the fitness of a single number-encoded key
#Fitness function is defined similar to the one in the article: https://pdfs.semanticscholar.org/6a1b/a7805583c0f2848b7ae325918a4243212ca3.pdf
def getFitness(decrypt):
    observedMono = getObservedMonogram(decrypt)
    observedBi = getObservedBigram(decrypt)
    f = open('assets/monogram.pckl', 'rb')
    englishMono = pickle.load(f)
    f.close()
    f = open('assets/bigram.pckl','rb')
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
    print(getFitness([1,2,3,4]))
    
