import numpy as np
import matplotlib.pyplot as plt 

n = 10
weights = np.eye(n,k=-1)
INITIAL = 0

timesteps = 5
v = np.zeros((n,timesteps))
spiketimes = []

El = -60 #mV
Ee = 0 #mV
Ei = -10 #mV
Vt = -40 #mV
epsilon = 0.01 #ratio of timestep to membrane time constant
g_gap = 1 #nS #equivalent coupling
g_e = .4 #nS 

#--initial conditions
v[:,INITIAL] = El +(Vt-El)*np.random.rand(n)

verbose = True
for t in xrange(1,timesteps):

	#first effect of gap junctions
#	v[:,t] += g_gap * (np.roll(v[:,t],-1)-v[:,t]) + g_gap * (np.roll(v[:,t],-1)-v[:,t])

	if verbose:
		print '----Starting voltage------------'
		print v[:,t-1]
		print '--------------------------------'
	
		print '----Leak change-----------------'
		print epsilon*(-v[:,t-1])
		print '--------------------------------'
	v[:,t] = v[:,t-1] + epsilon*(-v[:,t-1])

	#then synaptic effect
	idx = v[:,t] > Vt

	if verbose:
		print '----Spike effects --------------'
		those_that_spiked = map(str,np.nonzero(idx)[0])
		print 'Neurons %s spiked'%' '.join(those_that_spiked) if len(those_that_spiked) > 0 else 'No neurons spiked'
		print '--------------------------------'

	#Record spiketimes
	spiketimes.extend((t,np.nonzero(idx)[0]))
	#Propagate effect
	v[:,t][np.nonzero(idx)[0]] = El
	if verbose:
		print '----Ending voltage------------'
		print v[:,t]
		print '--------------------------------'

	for neuron in idx: #Propagate effect
		v[:,t] += g_e*weights[:,neuron]

print spiketimes

#--- raster
fig = plt.figure()
ax = fig.add_subplot(111)
for ith, (time,neurons) in enumerate(spiketimes):
	if len(neurons) > 0:
		ax.vlines(neurons, ith + .5, ith + 1.5, color='k')
ax.ylim(.5, len(event_times_list) + .5)
plt.show()