
import random
import math
import vigenereTools as vt
import numpy as np
import matplotlib.pyplot as plt

#Get signed sigmoid of value
def sigmoid(x):
    if (x >= 0):
        return 1/(1+math.exp(-x))
    else:
        return -1/(1+math.exp(-x))

#Get average of iterable
def avg(listA):
    return sum(listA)/len(listA)

class Particle:
    def __init__(self, num_dimensions, startVel = 1, startPos = None):
        self.position_i=[] #current position
        self.velocity_i=[] #current velocity
        self.pos_best_i=[] #current best position
        self.err_best_i=-1 #current best error
        self.err_i=-1      #current error

        #initialize particle with random position and velocity
        for i in range(0, num_dimensions):
            self.velocity_i.append(random.uniform(-1,1)*startVel)
            if startPos == None:
                self.position_i.append(random.random()*26)
            else:
                self.position_i.append( startPos[i])

    #evaluate with error function
    def evaluate(self, costFunc, encrypted):
        
        self.err_i=costFunc(self.position_i, encrypted)

        if self.err_i < self.err_best_i or self.err_best_i == -1:
            self.pos_best_i=self.position_i
            self.err_best_i=self.err_i

    #update velocity based on personal and global best positions
    def update_velocity(self, num_dimensions, pos_best_g):
        w=0.9
        c1=2.05
        c2=2.5

        for i in range(0, num_dimensions):
            r1 = random.random()
            r2 = random.random()

        vel_cognitive = c1*r1*(self.pos_best_i[i]-self.position_i[i])
        vel_social=c2*r2*(pos_best_g[i]-self.position_i[i])
        self.velocity_i[i]=sigmoid(w*self.velocity_i[i]+vel_cognitive+vel_social)

    #update position based on velocity
    def update_position(self, num_dimensions):
        for i in range(0,num_dimensions):
            self.position_i[i]=self.position_i[i]+self.velocity_i[i]

            # adjust maximum position if necessary
            if self.position_i[i]>26:
                self.position_i[i]=26
                self.velocity_i[i]= -0.6

            # adjust minimum position if neseccary
            if self.position_i[i] < 0:
                self.position_i[i]=0
                self.velocity_i[i]=0.6

class PSO():
    def __init__(self,costFunc,num_dimensions,encrypted,num_particles,maxiter):

        self.num_dimensions=num_dimensions
        self.err_best_g=-1                   # best error for group
        self.pos_best_g=[]                   # best position for group
        self.err_deviation = -1
        
        # establish the swarm
        swarm=[]
        for i in range(0,num_particles):
            swarm.append(Particle(num_dimensions))

        # begin optimization loop
        prevStdDev = [5 for x in range(0, 100)]
        prevFitness = [5 for x in range(0, 100)]
        i=0
        while (i < maxiter):
            

            print("On iteration " + str(i) + " of " + str(maxiter))
            #print i,err_best_g
            # cycle through particles in swarm and evaluate fitness
            for j in range(0,num_particles):
                swarm[j].evaluate(costFunc, encrypted)

                # determine if current particle is the best (globally)
                if swarm[j].err_i < self.err_best_g or self.err_best_g == -1:
                    self.pos_best_g=list(swarm[j].position_i)
                    self.err_best_g=float(swarm[j].err_i)

            # cycle through swarm and update velocities and position
            for j in range(0,num_particles):
                swarm[j].update_velocity(num_dimensions,self.pos_best_g)
                swarm[j].update_position(num_dimensions)
            xArr = [swarm[x].position_i[0] for x in range(0, len(swarm))]
            yArr = [swarm[x].position_i[1] for x in range(0, len(swarm))]
    


            #randomly reassign 10 particles to a location near their personal best position
            for x in range(0, 10):

                toChange = swarm[ int(random.random()*num_particles) ]
                posRand = [0 for x in range(0, len(self.pos_best_g))]
                for x in range(0,len( self.pos_best_g)):
                    possibleRandom = toChange.pos_best_i[x] + random.uniform(-6,6)
                    while (possibleRandom < 0 or possibleRandom > 25):
                        possibleRandom = toChange.pos_best_i[x] + random.uniform(-6,6)
                    posRand[x] = possibleRandom
                toChange.position_i = posRand
                toChange.velocity_i = [random.uniform(-1,1) for x in range(0,num_dimensions)]



            #check for changing error:
            stdDev = math.sqrt(sum([abs(particle.err_best_i - self.err_best_g)**2 for particle in swarm])/len(swarm))
            prevStdDev.append(stdDev)
            prevFitness.append(self.err_best_g)
            

            #Plot error function vs 
            #plt.scatter(i, stdDev, color='y')
            #plt.scatter(i, self.err_best_g, color='b')
            #plt.pause(0.001)

            #Termination criteria
            if (avg(prevStdDev[0:15]) - avg(prevStdDev[85:]) < (0.005)/(num_dimensions) and prevFitness[0] <= self.err_best_g and i > 101):
                break;
            prevStdDev.pop(0)
            prevFitness.pop(0)
            i+=1
                


            print(vt.toString([int(x) for x in self.pos_best_g ]))

        #print final results
        #print('FINAL KEY:')
        #print(vt.toString([ int(x) for x in self.pos_best_g ]))
        #print(self.err_best_g)
        #plt.show()
        
    def getBestPos(self):
        return [int(x) for x in self.pos_best_g]
    def getBestErr(self):
        return self.err_best_g
    def getNumIter(self):
        return i

def lossFunc(positions, encrypted):
    #Attempt decrypt with positional key
    encryptedNums = encrypted
    key = [int(x) for x in positions]
    keyLong = vt.extendCipherText(key, int(len(encryptedNums)/len(key)), len(encryptedNums))
    decrypted = vt.decrypt(encryptedNums, keyLong)
    decryptedStr = vt.toString(decrypted)

    #Test fitness of that decrypted text
    fitness = vt.getFitness(decrypted)
    return fitness

if __name__ == "__main__":
    #Get from Kasiski method
    size = int(input("Enter size of key: "))

    toRead = open('encrypted.txt', 'r')
    encrypted1 = toRead.read()
    toRead.close()

    
    PSO(lossFunc, size, vt.toNumArray(encrypted1), num_particles=100, maxiter=20000)

    plt.show()
