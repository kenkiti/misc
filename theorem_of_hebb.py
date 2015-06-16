from numarray import *

class hebb:
    memory = []
    memory_size = 0
    
    def __init__(self, size):
        self.memory_size = size
        self.memory = reshape([0]*size**2, (size, size))
        
    def learn(self, neural_activity):
        if self.memory_size != len(neural_activity):
            return False

        for y in range(self.memory_size):
            for x in range(self.memory_size):
                if x == y:
                    self.memory[x,y] = 0
                elif neural_activity[x] == 1 and neural_activity[y] == 1:
                    self.memory[x,y] += 1
                elif neural_activity[x] == -1 and neural_activity[y] == -1:
                    pass
                else:
                    self.memory[x,y] -= 1
        return True

    def remember(self, neural_activity):
        if self.memory_size != len(neural_activity):
            return False

        neural_activity = reshape(neural_activity, (self.memory_size, 1))
        mind = dot(self.memory ,neural_activity)
        return reshape(mind / abs(mind), (1, self.memory_size))[0]

def learn(hebb, neural_activity):
    if hebb.learn(neural_activity):
        print neural_activity, "is memorized."
    else:
        print "I can't learn ", neural_activity
        

def remember(hebb, question):
    answer = hebb.remember(question)
    if any(answer):
        print "I remember %s from %s." % (answer ,question)
    else:
        print "I can't remember ", question

h = hebb(3) 
learn(h, [1,1,-1])
learn(h, [1,1,-1])
learn(h, [1,1,-1])
remember(h, [1,1,-1])
learn(h, [1,-1,1])
learn(h, [1,-1,1])
remember(h, [1,1,-1])
remember(h, [1,-1,1])
remember(h, [1,1,0])
