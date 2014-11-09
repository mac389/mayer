import numpy as np
import utils as tech
import matplotlib.pyplot as plt 


'''
  #Different distributions of gap junctions (masked arrays)

'''
n = 15
weights = np.eye(n,k=-1)
INITIAL = 0

timesteps = 150
conditions = 3
timesteps *= conditions
v = np.zeros((n,timesteps))
spiketimes = {neuron:[] for neuron in xrange(n)}

El = -60 #mV
Ee = 0 #mV
Ei = -10 #mV
Vt = -40 #mV
epsilon = 0.01 #ratio of timestep to membrane time constant
g_gap = 40 #nS #equivalent coupling
g_e = 20 #nS 

#--initial conditions
v[:,INITIAL] = El +(Vt-El)*np.random.rand(n)

verbose = True
for t in xrange(1,timesteps):

	#first effect of gap junctions
	left =  np.roll(v[:,t-1],-1)
	left[0]=v[:,t-1][0]

	right  = np.roll(v[:,t-1],1)
	right[-1] = v[:,t-1][-1]
	if verbose:
		print '----FX of gap junctions-----------'
		print g_gap * (left-v[:,t-1]) + g_gap * (right-v[:,t-1])
		print '----FX of gap junctions-----------'
 	v[:,t] += g_gap * (left-v[:,t-1]) + g_gap * (right-v[:,t-1])

	if verbose:
		print '----Starting voltage------------'
		print v[:,t-1]
		print '--------------------------------'
	
		print '----Leak change-----------------'
		print epsilon*(-v[:,t-1])
		print '--------------------------------'
	v[:,t] += (v[:,t-1] + epsilon*(-v[:,t-1]))

	#then synaptic effect
	idx = v[:,t] > Vt

	if verbose:
		print '----Spike effects --------------'
		those_that_spiked = map(str,np.nonzero(idx)[0])
		print 'Neurons %s spiked'%' '.join(those_that_spiked) if len(those_that_spiked) > 0 else 'No neurons spiked'
		print '--------------------------------'

	#Record spiketimes
	for neuron in np.nonzero(idx)[0]:
		times = spiketimes[neuron]
		times.append(t)
		spiketimes[neuron] = times
	#Propagate effect
	v[:,t][np.nonzero(idx)[0]] = El
	if verbose:
		print '----Ending voltage------------'
		print v[:,t]
		print '--------------------------------'

	for neuron in np.nonzero(idx)[0]: #Propagate effect
		v[:,t] += g_e*weights[:,neuron]


#--- raster
fig = plt.figure()
ax = fig.add_subplot(111)
for neuron in xrange(n):
	if neuron in spiketimes and len(spiketimes[neuron]) > 0:
		ax.vlines(spiketimes[neuron],  neuron+ .5, neuron + 1.5, color='k')
ax.set_ylim(-1, len(spiketimes))
tech.adjust_spines(ax)
ax.yaxis.grid()
ax.set_yticks(xrange(n))
ax.set_xlim(xmin=0,xmax=timesteps)
ax.set_xlabel('Time')
ax.set_ylabel('Neurons')
fig.tight_layout()
'''
#--- voltage
trace,panels = plt.subplots(nrows=n,ncols=1,sharex=True)
for neuron,panel in enumerate(panels):
	panel.plot(v[neuron,:])
	tech.adjust_spines(panel,['left'] if neuron < (n-1) else ['left','bottom'])
	panel.set_ylim(ymax=v.max(),ymin=v.min())
	panel.set_yticks([np.floor(v.min()),np.ceil(v.max())])
	panel.set_xticks(range(timesteps))
trace.tight_layout()
trace.subplots_adjust(hspace=0.5)
'''
plt.show()
