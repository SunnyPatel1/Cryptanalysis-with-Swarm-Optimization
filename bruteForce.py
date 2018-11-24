import vigenereTools as vt      # Import Vigenere Tools
import math                     #Import Math Library
import time                     #Import Time Library
import timeit                   #Import Timeit Library

# Initiate Variables: min fitness function, best decryption, and best key, key combinations
keys = []
min = -1
min_decrypt_arr = []
best_key = ''
count=0
percent_div=0
percent = 0
#Get Key length from user
inp = input("Enter key character length to test: ")
key_length = int(inp)

# Get cipher text from user
# inp = input("Enter cipher: ")
# cipher = inp

# OR
# Get cipher text from file
toRead = open('encrypted.txt', 'r')
cipher = toRead.read()
toRead.close()

# Assign cipher text to array
cipher_arr = vt.toNumArray(cipher)

#generates list of all possible key combinations
char_list = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
for current in range(key_length):
    a = [i for i in char_list]
    for y in range(current):
        a = [x+i for i in char_list for x in a]
    keys = keys+a

#progress calculations
percent_div = math.floor(len(keys)/100)
start = timeit.default_timer()

#loops through every key in list
for key in keys:

    #calculates approximate time to complete operation
    count = count + 1
    if count == percent_div:
        stop = timeit.default_timer()
        percent = percent + 1

        if percent == 1:
            print(str(percent) + '% ' + str(math.floor((stop-start)*100/60)) + ' Minutes remaining')
        else:
            print(str(percent) + '% ')
        count = 0
    # For each possible key combo...
    #   Decrypt using that key
    #   Get fitness function for that decrypted text
    #   Assign that fitness as new best if higher than all previous
    #   When done, best fitness test results are printed to user
    #       (i.e. best key, decrypted text and fitness function)

    key_arr = vt.toNumArray(key)
    keyLong = vt.extendCipherText(key_arr, int(len(cipher_arr)/len(key)), len(cipher_arr))
    decrypted = vt.decrypt(cipher_arr, keyLong)
    fitness = vt.getFitness(decrypted)
    if (min == -1 or min > fitness):
        min = fitness
        min_decrypt_arr = decrypted
        best_key = key

# Print results to user
print('\nOutput: ')
print(vt.toString(min_decrypt_arr))
print('KEY: ' + best_key)
