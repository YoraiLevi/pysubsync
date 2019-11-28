import matplotlib.pyplot as plt
import numpy as np
import random
def gen_subs(length):
    sum = 0 
    sub = np.zeros(sum)    
    while(sum<length):
        nothing = np.zeros(random.randint(25,170))
        sub = np.concatenate([sub,nothing])
        sentences = random.randint(4,11)
        for i in range(sentences):
            on = np.ones(random.randint(2,11))
            off = np.zeros(random.randint(4,20))
            sum = sum+len(on)+len(off)
            sub = np.concatenate([sub,on,off])
    return sub
subs = gen_subs(300)
shifted_subs = np.append(np.zeros(150),subs)
correlation = np.correlate(shifted_subs,subs,'full')
peak = np.argmax(correlation)
shift = peak+1-len(subs)
corrected = shifted_subs[shift:]
plt.plot(subs)
plt.plot(shifted_subs)
plt.plot(corrected)