import random
import math
import vigenereTools as vt
import numpy as np

class Particle:
    def __init__(self, bounds):
        # Initalize particle variables
        self.position_i=[]      # particle position
        self.velocity_i=[]      # particle velocity
        self.pos_best_i=[]      # particle personal best
        self.err_best_i=-1      # particle error best
        self.err_i=-1           # particle error

        # For every dimension, add particle and initiate velocity and position
        for i in range(0, num_dimensions):
            self.velocity_i.append(random.uniform(-1,1))
            self.position_i.append(random.uniform(bounds[i][0], bounds[i][1]))

    # Evaluate position in comparison to personal best and global best
    def evaluate(self, costFunc):
        self.err_i=costFunc(self.position_i)
        
        # check particle error is less than error best or if error best is =-1
        if self.err_i < self.err_best_i or self.err_best_i == -1:
            self.pos_best_i=self.position_i     # set personal best to current position
            self.err_best_i=self.err_i          # set error best to particle current error
            
    # Update particle velocity
    def update_velocity(self, pos_best_g):
        w=0.9       # intertia weight
        c1=2.05     # self-confidence
        c2=2.05     # swarm-confidence

        # For each dimension
        for i in range(0, num_dimensions):
            r1 = random.random()    # uniformly generated random num range[0,1] 
            r2 = random.random()    # uniformly generated random num range[0,1]

        # Set Velocity using cognitive and social velocities. 
        vel_cognitive = c1*r1*(self.pos_best_i[i]-self.position_i[i])
        vel_social=c2*r2*(pos_best_g[i]-self.position_i[i])
        
        # Vi^(t+1) = ( w * Vi^(t) ) + [(C1 * r1) * (pBesti - X1^(t))] + [(C2 * r2) * (gBesti - Xi^(t))]
        self.velocity_i[i]=w*self.velocity_i[i]+vel_cognitive+vel_social

    # Update particle position
    def update_position(self, bounds):
        
        # For each dimension
        for i in range(0,num_dimensions):
            
            # Xi^)t+1) = Xi^(t) + Vi^(t+1)
            self.position_i[i]=self.position_i[i]+self.velocity_i[i]

            # adjust maximum position if necessary
            if self.position_i[i]>bounds[i][1]:
                self.position_i[i]=bounds[i][1]

            # adjust minimum position if neseccary
            if self.position_i[i] < bounds[i][0]:
                self.position_i[i]=bounds[i][0]
                                
class PSO():
    def __init__(self,costFunc,x0,bounds,num_particles,maxiter):
        global num_dimensions           # define global variable for number of positions

        num_dimensions=size             # set the number of positions to be the size of key
        err_best_g=-1                   # best error for group
        pos_best_g=[]                   # best position for group

        # establish the swarm
        swarm=[]
        for i in range(0,num_particles):
            swarm.append(Particle(bounds))

        # begin optimization loop
        i=0
        
        # while less than the maximum number of set iterations
        while i < maxiter:
            print("On iteration " + str(i) + " of " + str(maxiter))
            #print i,err_best_g
            # cycle through particles in swarm and evaluate fitness
            for j in range(0,num_particles):
                swarm[j].evaluate(costFunc)

                # determine if current particle is the best (globally)
                if swarm[j].err_i < err_best_g or err_best_g == -1:
                    pos_best_g=list(swarm[j].position_i)
                    err_best_g=float(swarm[j].err_i)

            # cycle through swarm and update velocities and position
            for j in range(0,num_particles):
                swarm[j].update_velocity(pos_best_g)
                swarm[j].update_position(bounds)
            i+=1

        # print final results
        print('FINAL KEY:')
        print(vt.toString([ int(x) for x in pos_best_g ]))
        print(err_best_g)

# define fitness function
def lossFunc(positions):
    encryptedNums = vt.toNumArray(encrypted)
    key = [int(x) for x in positions]
    keyLong = vt.extendCipherText(key, int(len(encryptedNums)/len(key)), len(encryptedNums))
    decrypted = vt.decrypt(encryptedNums, keyLong)
    decryptedStr = vt.toString(decrypted)
    fitness = vt.getFitness(decrypted)
    return fitness

#Will later do this with kasinski (or similar name) method
size = int(input("Enter size of key: "))

# open encrypted text from text file
toRead = open('encrypted.txt', 'r')
encrypted = toRead.read()
toRead.close()

# set bounds and decrypt.
bounds=np.tile([(0,25)], (size,1))
PSO(lossFunc, size, bounds, num_particles=100, maxiter=100)


    
