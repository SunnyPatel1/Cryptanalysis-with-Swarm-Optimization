import numpy as np
import random
import math
import vigenereTools as vt
import pso as pso
import time

def generateKey(length):
    key = [random.randint(0, 25) for y in range(0, length)]

    return key

def checkSame(key, proposedKey, length):

    same = [1 if key[x] == proposedKey[x] else 0 for x in range(0, length)]
    return sum(same)


plainTextFile = open('plain-text.txt', 'r')
plainText = plainTextFile.read()
toEncode = vt.prepInput(plainText)
toEncodeArray = vt.toNumArray(toEncode)

csvFile = open('results.csv', 'w')
csvFile.write("Real Key, Generated Key, Loss, Total Correct, TimeTaken\n")
csvFile.close()

for key_size in range(5,26,5):
    for run in range(0, 10):
        key = generateKey(key_size)
        keyLong = vt.extendCipherText(key,
                                      int(len(toEncodeArray)/len(key)),
                                      len(toEncodeArray))
        print("ACTUAL KEY: ")
        print(vt.toString(key))
        cipher = vt.encrypt(keyLong, toEncodeArray)

        #print(vt.toString(vt.decrypt(cipher, keyLong)))

        bounds=np.tile([(0,25)], (key_size,1))

        startTime = time.time()

        psoIter = pso.PSO(pso.lossFunc, key_size, bounds, cipher, num_particles=100, maxiter=key_size*25)
        endTime = time.time()
        err_best = psoIter.getBestErr()
        pos_best = psoIter.getBestPos()

        numCorrect = checkSame(key, pos_best, key_size)

        print("The best key was: " + vt.toString(pos_best) + " with a loss value of " + str(err_best) + " and a total correct of " + str(numCorrect))
        csvFile = open('results.csv', 'a')
        csvFile.write(vt.toString(key) + "," + vt.toString(pos_best) + ", " + str(err_best) + "," + str(numCorrect) + "," + str(endTime - startTime)+"\n")
        csvFile.close()

    
