
import numpy as np
import matplotlib.pyplot as plt
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as path
import matplotlib.animation as animation

import numpy as np
from matplotlib.pylab import *
import matplotlib.animation as animation


def square(Hc_mean = 0.062, Hc_std = 0.0):
    '''
    Defines the lattice positions, magnetisation directions and coercive fields of an array of 
    square ASI
    Takes the unit cell from the initial defined parameters
    Generates a normally distributed range of coercive fields of the bars using Hc_mean and Hc_std as a percentage
    One thing to potentially change is to have the positions in nanometers
    '''
    Hc = Hc_mean
    Hc_std = Hc_std
    side_len_x = 2*unit_cells_x+1
    side_len_y = 2*unit_cells_y+1
    grid = np.zeros((side_len_x, side_len_y, 9))        
    for x in range(0, side_len_x):
        for y in range(0, side_len_y):
            if (x+y)%2 != 0:
                if y%2 == 0:
                    grid[x,y] = np.array([x*unit_cell_len,y*unit_cell_len,0.,1.,0.,0., np.random.normal(loc=Hc_mean, scale=Hc_std*Hc_mean, size=None),0,None])
                else:
                    grid[x,y] = np.array([x*unit_cell_len,y*unit_cell_len,0.,0.,1.,0.,np.random.normal(loc=Hc_mean, scale=Hc_std*Hc_mean, size=None),0,None])
            else:
                if x%2 ==0 and x!=0 and y!=0 and x!=side_len_x-1 and y!=side_len_x-1:
                    grid[x,y] = np.array([x*unit_cell_len,y*unit_cell_len,0.,0.,0.,0.,0,0,0])
                else:
                    grid[x,y] = np.array([x*unit_cell_len,y*unit_cell_len,0.,0.,0.,0.,0,0,None])
    return(grid)
def dipole(m, r, r0):
	"""Calculate a field in point r created by a dipole moment m located in r0.
	Spatial components are the outermost axis of r and returned B.
	"""
	m = np.array(m)
	r = np.array(r)
	r0 = np.array(r0)
	m = m
	#print(r,r0)
	#r = (.vertex_gap+.bar_length/2)*r
	#r0 = (.vertex_gap+.bar_length/2)*r0
	# we use np.subtract to allow r and r0 to be a python lists, not only np.array
	R = np.subtract(np.transpose(r), r0).T
	# assume that the spatial components of r are the outermost axis
	norm_R = np.sqrt(np.einsum("i...,i...", R, R))
	# calculate the dot product only for the outermost axis,
	# that is the spatial components
	m_dot_R = np.tensordot(m, R, axes=1)
	# tensordot with axes=0 does a general outer product - we want no sum
	B = 3 * m_dot_R * R / norm_R**5 - np.tensordot(m, 1 / norm_R**3, axes=0)
	# include the physical constant
	B *= 1e-7
	return(B)

def Hlocal2(lattice,x,y,n =1):
    Hl = []
    x1 = x - n
    x2 = x + n+1
    y1 = y - n
    y2 = y + n+1
    side_len_x = 2*unit_cells_x+1
    side_len_y = 2*unit_cells_y+1
    if x1<0:
        x1 = 0
    if x2>side_len_x:
        x2 = side_len_x -1
    if y1<0:
        y1 = 0
    if y2>side_len_y-1:
        y2 = side_len_y-1

    local = lattice[x1:x2,y1:y2,:]
    m = local[:,:,3:6]
    m = m.reshape(-1, m.shape[-1])
    r = local[:,:,0:3]
    r = r.reshape(-1, r.shape[-1])
    r0 = lattice[x,y,0:3]

    for pos, mag in zip(r, m):
        if np.linalg.norm(pos-r0)/(n+1)<=1.0 and np.array_equal(pos, r0)!=True:
            Hl.append(dipole(mag, r0, pos))

    grid = lattice
    #plt.quiver(grid[:,:,0].flatten(), grid[:,:,1].flatten(),grid[:,:,3].flatten(),grid[:,:,4].flatten(), angles='xy', scale_units='xy',  pivot = 'mid')
    #plt.scatter(grid[:,:,0].flatten(), grid[:,:,1].flatten(), c = grid[:,:,8].flatten())
    #plt.plot(grid[x,y,0],grid[x,y,1], 'o')
    #plt.quiver(local[:,:,0].flatten(), local[:,:,1].flatten(),local[:,:,3].flatten(),local[:,:,4].flatten(), angles='xy', scale_units='xy',  pivot = 'mid')
    #plt.show()
    #print(sum(Hl))
    #print(np.sum(np.array(Hl), axis = 0))
    return(np.sum(np.array(Hl), axis = 0))
    

def randomMag(lattice,seed = None):
    State = np.random.RandomState(seed=seed)
    grid = lattice
    side_len_x = 2*unit_cells_x+1
    side_len_y = 2*unit_cells_y+1
    for x in range(0, side_len_x):
        for y in range(0, side_len_y):
            if grid[x,y,6] != 0:
                if State.uniform(low=0.0, high=1.0)>0.5:
                    grid[x,y,3:5]=-1.*grid[x,y,3:5]
    grid[grid ==0]=0.
    return(grid)

def localPlot(lattice, x,y,n):
	print('t')
    x1 = x - n
    x2 = x + n+1
    y1 = y - n
    y2 = y + n+1
    side_len_x = 2*unit_cells_x+1
    side_len_y = 2*unit_cells_y+1
    if x1<0:
        x1 = 0
    if x2>side_len_x:
        x2 = side_len_x -1
    if y1<0:
        y1 = 0
    if y2>side_len_y-1:
        y2 = side_len_y-1

    local = lattice[x1:x2,y1:y2,:]
	grid = lattice
    plt.quiver(grid[:,:,0].flatten(), grid[:,:,1].flatten(),grid[:,:,3].flatten(),grid[:,:,4].flatten(), angles='xy', scale_units='xy',  pivot = 'mid')
    plt.scatter(grid[:,:,0].flatten(), grid[:,:,1].flatten(), c = grid[:,:,8].flatten())
    plt.plot(grid[x,y,0],grid[x,y,1], 'o')
    plt.quiver(local[:,:,0].flatten(), local[:,:,1].flatten(),local[:,:,3].flatten(),local[:,:,4].flatten(), angles='xy', scale_units='xy',  pivot = 'mid')
    plt.show()
unit_cells_x=10
unit_cells_y =10
unit_cell_len = 1

lattice = kagome()
lattice = randomMag(lattice)



#print(field[1])



test = Hlocal2(lattice, 10,9,n=1)
print(test)
field = [test[1]]
for c in np.arange(0,10000):
	lattice = randomMag(lattice)
	test = Hlocal2(lattice,10,9,n=8)
	field.append(test[1])
print(field)
fig, ax1 = plt.subplots(1, 1)
ax1.hist(field, normed=True, bins=np.linspace(-5e-7,5e-7, num=101), alpha=1.)
ax1.set_ylabel('Count')
ax1.set_xlabel('Field Strength along axis (scaled units)')
ax1.set_title('Dipolar Field - n=8 nearest neighbours')
def updateData(curr):
    if curr <=2: return
    
    ax1.clear()
    ax1.hist(field[:curr], normed=True, bins=np.linspace(-1e-6,1e-6, num=50), alpha=0.5)


#simulation = animation.FuncAnimation(fig, updateData, interval=50, repeat=True)

plt.show()