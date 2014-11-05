import numpy as np
import matplotlib.pyplot as plt
import itertools


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return itertools.izip(a, b)

#--chose patterns
INITIAL = 0
n = 10
nMem = 10 
memories = np.random.randint(2,size=(n,nMem)) #sparsity is 0.5, can make this more rigorous later

connections = np.array([[sum(one[i]*two[j] for one,two in pairwise(memories.T)) for i in xrange(memories.shape[0])]
								for j in xrange(memories.shape[0])]).astype(float)

connections /= nMem


print connections
heaviside = lambda x: 1 if x>=0 else 0

duration = 1000
activity = np.zeros((n,duration))
noise = np.random.sample(size=activity.shape)
K=nMem #For now, don't know a better guess

#-- initial conditions
activity[:,INITIAL] = np.random.randint(2,size=(n,))
threshold = 0.6
for timestep in xrange(1,duration):

	Q = activity[:,timestep-1].sum()
	Q /= float(nMem)
	activity[:,timestep] = map(heaviside,connections.dot(activity[:,timestep-1]) - K*Q+noise[:,timestep-1]-threshold)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.imshow(activity,interpolation='nearest',aspect='auto',cmap=plt.cm.binary)
plt.show()