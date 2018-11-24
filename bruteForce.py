import vigenereTools as vt
import itertools

min = -1
min_decrypt_arr = []
best_key = ''
inp = input("Enter key character length to test: ")
key_length = int(inp)
inp = input("Enter cipher: ")
cipher = inp
cipher_arr = vt.toNumArray(cipher)

for i in range(1, key_length + 1):
    generator=itertools.combinations_with_replacement('ABCDEFGHIJKLMNOPQRSTUVWXYZ', i )
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

print('\nOutput: ')
print(vt.toString(min_decrypt_arr))
print('KEY: ' + best_key)
