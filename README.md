# Cryptanalysis-with-Swarm-Optimization
Using particle swarm optimization to find cipher keys in substitution ciphers (Vigenere, Ceaser)

# TODO:

* Refactor and comment
* Add a brute force approach for comparison purposes
* Utilize Kasiki method to determine key length
* Add dropout

## Vigenere Cipher

The Vigenere Cipher is a substitution based encryption cipher that uses a repeating key, and each letter is shifted based on the key, wrapping around a set of all capital letters in order. 

In an algebraic sense, the cipher text `C` can be found by using the encryption function `E(P, K)`, a function of the Plain Text to encode `P` and the extended key `K`, where:

```pseudocode
C = E(Pi, Ki) = (Ei + Ki)%26
```

The modulo 26 wraps the alphabet around such that A follows Z. 

The decryption algorithm is therefore:

```pseudocode
E = D(Ci, Ki) = (Ci - Ki)%26
```

## Particle Swarm Optimization

Particle Swarm Optimization is an optimization technique useful for finding global extrema. As such, a **loss function** needs to be defined. 

A swarm of particles in the solution space are assigned random velocities, but naturally gravitate towards the particle with the best solution, as well as the best solution it previously held. The best solution is defined as the one with the lowest cost function.

### Defining a Loss Function

Initially, I tried to define a fitness function equal to the total number of English words found in the key. This did not work very well.

We then changed approaches to matching the frequency of monograms and bigrams, and using that as our loss function.

### Defining a Solution Space

I defined a solution space that was n-dimensional, where n is the number of characters in the key. Each dimension can hold a value between 0 and 25, where 0 represents A and 25, Z.

Having a dimension per character would help because it relates each of them, whereas flattening a dimension (having a 1-dimensional representation of the solution space that is 26^n in cardinality) would result in locations that are abstractly related (AAA would be closer to AZZ than AAZ)

### Dropout

Similar to a convolutional neural network, we may want to drop some of the particles. This helps avoid  avoid local minima. The reason is because the local minima general surrounded the global minimum, and so particles often circled around it. A greater weight for the social factor may also accommodate for this. 

Further testing required.

### Finding the length of the Key

While the algorithm currently requires us to enter the length of the key, this does not translate well into the real world. We can, however use the Kasiki method for finding the length of the key.

Implementation still required.