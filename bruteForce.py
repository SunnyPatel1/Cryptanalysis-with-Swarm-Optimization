import vigenereTools as vt      # Import Vigenere Tools
import itertools                # Import Itertools

# Initiate Variables: min fitness function, best decryption, and best key
min = -1
min_decrypt_arr = []    
best_key = ''

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

# For the length of the key
for i in range(1, key_length + 1):
    # Generate all combinations with replacement of given key length
    generator=itertools.combinations_with_replacement('ABCDEFGHIJKLMNOPQRSTUVWXYZ', i )
    
    # For each possible key combo...
    #   Decrypt using that key
    #   Get fitness function for that decrypted text
    #   Assign that fitness as new best if higher than all previous
    #   When done, best fitness test results are printed to user 
    #       (i.e. best key, decrypted text and fitness function)
    for password in generator:
        key = ''.join(password)
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
