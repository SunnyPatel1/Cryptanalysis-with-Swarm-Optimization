import numpy as np
import vigenereTools as vt
import pickle

def getInputs(fileName):
    mono = open(fileName, 'r')

    totals = {}

    content = mono.read()
    lines = content.splitlines()

    total = 0

    for line in lines:
        totals[line.split(" ")[0]] = float(line.split(" ")[1])
        total += int(line.split(" ")[1])

    standard = {key: value/total for key, value in totals.items() }
    return standard


def main():
    monoHz = getInputs("monogram.txt")
    biHz = getInputs("bigram.txt")

    f = open('monogram.pckl', 'wb')
    pickle.dump(monoHz, f)
    f.close()

    f = open('bigram.pckl', 'wb')
    pickle.dump(biHz, f)
    f.close()


if __name__ == "__main__":
    main()

