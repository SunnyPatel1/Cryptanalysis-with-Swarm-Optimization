
import random
import math
import vigenereTools as vt
import numpy as np
import matplotlib.pyplot as plt

def sigmoid(x):
    if (x >= 0):
        return 1/(1+math.exp(-x))
    else:
        return -1/(1+math.exp(-x))

class Particle:
    def __init__(self, bounds, startVel = 1, startPos = None):
        self.position_i=[]
        self.velocity_i=[]
        self.pos_best_i=[]
        self.err_best_i=-1
        self.err_i=-1

        for i in range(0, num_dimensions):
            self.velocity_i.append(random.uniform(-1,1)*startVel)
            if startPos == None:
                self.position_i.append(random.random()*26)
            else:
                self.position_i.append( startPos[i])

    def evaluate(self, costFunc, encrypted):
        
        self.err_i=costFunc(self.position_i, encrypted)

        if self.err_i < self.err_best_i or self.err_best_i == -1:
            self.pos_best_i=self.position_i
            self.err_best_i=self.err_i

    
    def update_velocity(self, pos_best_g):
        w=0.9
        c1=2.05
        c2=2.5

        for i in range(0, num_dimensions):
            r1 = random.random()
            r2 = random.random()

        vel_cognitive = c1*r1*(self.pos_best_i[i]-self.position_i[i])
        vel_social=c2*r2*(pos_best_g[i]-self.position_i[i])
        self.velocity_i[i]=sigmoid(w*self.velocity_i[i]+vel_cognitive+vel_social)

    def update_position(self, bounds):
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
    def __init__(self,costFunc,x0,bounds,encrypted,num_particles,maxiter):
        global num_dimensions

        num_dimensions=len(bounds)
        self.err_best_g=-1                   # best error for group
        self.pos_best_g=[]                   # best position for group
        self.err_deviation = -1
        
        # establish the swarm
        swarm=[]
        for i in range(0,num_particles):
            swarm.append(Particle(bounds))

        # begin optimization loop
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
                swarm[j].update_velocity(self.pos_best_g)
                swarm[j].update_position(bounds)
            xArr = [swarm[x].position_i[0] for x in range(0, len(swarm))]
            yArr = [swarm[x].position_i[1] for x in range(0, len(swarm))]

            scatter1 = plt.scatter(xArr, yArr, color='y')
            plt.pause(0.001)
            scatter1.remove()



            #add dropout
            '''for x in range(0, 15):

                toDel = int(random.random()*num_particles)
                errToDel = swarm[toDel].err_i
                oldPos = swarm[toDel].position_i
                posRand = [0 for x in range(0, len(oldPos))]

                for x in range(0, len(oldPos)):
                    possibleRandom = oldPos[x] + random.uniform(-2, 2)
                    while (possibleRandom < 0 or possibleRandom >= 26):
                        possibleRandom = self.pos_best_g[x] + random.uniform(-2,2)
                    posRand[x] = possibleRandom
                if lossFunc(posRand, encrypted) <= swarm[toDel].err_best_i:
                    del swarm[toDel]
                    swarm.append(Particle(bounds, 2, posRand))

                del swarm[ int(random.random()*num_particles) ]
                posRand = [0 for x in range(0, len(self.pos_best_g))]
                for x in range(0,len( self.pos_best_g)):
                    possibleRandom = self.pos_best_g[x] + random.uniform(-2,2)
                    while (possibleRandom < 0 or possibleRandom > 25):
                        possibleRandom = self.pos_best_g[x] + random.uniform(-2,2)
                    posRand[x] = possibleRandom
                swarm.append(Particle(bounds, 1.05, posRand))'''

            #check for error stopping changing:
            avgError = sum([swarm[x].err_best_i for x in range(0, len(swarm))])/len(swarm)
            stdDev = math.sqrt(sum([abs(swarm[x].err_best_i - self.err_best_g)**2 for x in range(0, len(swarm))])/len(swarm))

            print(stdDev)
            
            #if (stdDev <= 0.05 and stdDev >= 0):
               # break;
            i+=1
                


            print(vt.toString([int(x) for x in self.pos_best_g ]))

        # print final results
        #print('FINAL KEY:')
        #print(vt.toString([ int(x) for x in self.pos_best_g ]))
        #print(self.err_best_g)
    def getBestPos(self):
        return [int(x) for x in self.pos_best_g]
    def getBestErr(self):
        return self.err_best_g

def lossFunc(positions, encrypted):

    encryptedNums = encrypted
    key = [int(x) for x in positions]
    keyLong = vt.extendCipherText(key, int(len(encryptedNums)/len(key)), len(encryptedNums))
    decrypted = vt.decrypt(encryptedNums, keyLong)
    decryptedStr = vt.toString(decrypted)
    fitness = vt.getFitness(decrypted)
    return fitness

if __name__ == "__main__":
    #Will later do this with kasinski (or similar name) method
    size = int(input("Enter size of key: "))

    toRead = open('encrypted.txt', 'r')
    encrypted1 = toRead.read()
    toRead.close()


    bounds=np.tile([(0,25)], (size,1))
    PSO(lossFunc, size, bounds, vt.toNumArray(encrypted1), num_particles=100, maxiter=20000)

    plt.show()
