from string import punctuation
import numpy as np
import vigenereTools as vt



plainTextFile = open('plain-text.txt', 'r')
keyTextFile = open('key.txt', 'r')

plainText = plainTextFile.read()
keyText = keyTextFile.read()

for char in punctuation:
    plainText = plainText.replace(char, '')
    keyText = keyText.replace(char, '')

plainText = plainText.replace("\n", '').replace(" ", '').upper()
keyText = keyText.replace("\n", '').replace(" ", '').upper()


numArrayPlain = vt.toNumArray(plainText)
print(numArrayPlain)

numArrayKey = vt.toNumArray(keyText)

#Extend cipher text to repeat untill same size as plain text
factor = int(len(numArrayPlain)/len(numArrayKey))

extendedKeyArr = vt.extendCipherText(numArrayKey, #pass array to extend
                                     factor, #pass how many times bigger
                                     len(numArrayPlain)) #pass target size

encryptedNums = vt.encrypt(numArrayPlain, extendedKeyArr)


encrypted = vt.toString(encryptedNums)
print(encrypted)

writeFile = open('encrypted.txt', 'w+')
writeFile.write(encrypted)
writeFile.close()

decrypt = vt.decrypt(encryptedNums, extendedKeyArr)
print(vt.toString(decrypt))

print(keyText)
