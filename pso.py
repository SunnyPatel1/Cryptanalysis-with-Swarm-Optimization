import random
import math
import vigenereTools as vt
import numpy as np

class Particle:
    def __init__(self, bounds):
        self.position_i=[]
        self.velocity_i=[]
        self.pos_best_i=[]
        self.err_best_i=-1
        self.err_i=-1

        for i in range(0, num_dimensions):
            self.velocity_i.append(random.uniform(-1,1))
            self.position_i.append(random.uniform(bounds[i][0], bounds[i][1]))

    def evaluate(self, costFunc):
        self.err_i=costFunc(self.position_i)

        if self.err_i < self.err_best_i or self.err_best_i == -1:
            self.pos_best_i=self.position_i
            self.err_best_i=self.err_i
    def update_velocity(self, pos_best_g):
        w=0.9
        c1=2.05
        c2=2.05

        for i in range(0, num_dimensions):
            r1 = random.random()
            r2 = random.random()

        vel_cognitive = c1*r1*(self.pos_best_i[i]-self.position_i[i])
        vel_social=c2*r2*(pos_best_g[i]-self.position_i[i])
        self.velocity_i[i]=w*self.velocity_i[i]+vel_cognitive+vel_social

    def update_position(self, bounds):
        for i in range(0,num_dimensions):
            self.position_i[i]=self.position_i[i]+self.velocity_i[i]

            # adjust maximum position if necessary
            if self.position_i[i]>bounds[i][1]:
                self.position_i[i]=bounds[i][1]

            # adjust minimum position if neseccary
            if self.position_i[i] < bounds[i][0]:
                self.position_i[i]=bounds[i][0]
class PSO():
    def __init__(self,costFunc,x0,bounds,num_particles,maxiter):
        global num_dimensions

        num_dimensions=size
        err_best_g=-1                   # best error for group
        pos_best_g=[]                   # best position for group

        # establish the swarm
        swarm=[]
        for i in range(0,num_particles):
            swarm.append(Particle(bounds))

        # begin optimization loop
        i=0
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

toRead = open('encrypted.txt', 'r')
encrypted = toRead.read()
toRead.close()


bounds=np.tile([(0,25)], (size,1))
PSO(lossFunc, size, bounds, num_particles=100, maxiter=100)


    
