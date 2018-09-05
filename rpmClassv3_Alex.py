import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as cl
from matplotlib.ticker import MaxNLocator
#from matplotlib.colors import Normalize
import copy
import os


class ASI_RPM():
    def __init__(self, unit_cells_x, unit_cells_y, lattice = None, \
        bar_length = 220e-9, vertex_gap = 1e-7, bar_thickness = 25e-9, \
        bar_width = 80e-9, magnetisation = 800e3):
        self.lattice = lattice
        self.type = None
        self.previous = None
        self.unit_cells_x = unit_cells_x
        self.unit_cells_y = unit_cells_y
        self.side_len_x = None      #The side length is now defined in the 
        self.side_len_y = None
        self.bar_length = bar_length
        self.vertex_gap = vertex_gap
        self.bar_width = bar_width
        self.bar_thickness = bar_thickness
        self.width = bar_width
        self.magnetisation = magnetisation
        self.unit_cell_len = (bar_length+vertex_gap)/2

    def save(self, file, folder = os.getcwd()):
        '''
        Save existing arrays
        To Do
        '''
        file = file.replace('.','p')
        parameters = np.array([self.unit_cells_x,self.unit_cells_y,\
            self.bar_length,self.vertex_gap,self.bar_width,\
            self.bar_thickness,self.magnetisation, self.side_len_x, self.side_len_y])
        np.savez(os.path.join(folder,file), self.lattice, parameters)

    def load(self, file):
        '''
        load in existing arrays
        To Do
        '''
        npzfile = np.load(file)
        parameters = npzfile['arr_1']
        self.unit_cells_x = np.int(parameters[0])
        self.unit_cells_y = np.int(parameters[1])
        self.bar_length = parameters[2]
        self.vertex_gap = parameters[3]
        self.bar_width = parameters[4]
        self.bar_thickness = parameters[5]
        self.magnetisation = parameters[6]
        self.side_len_x = np.int(parameters[7])
        self.side_len_y = np.int(parameters[8])
        self.lattice = npzfile['arr_0']
        
    def square(self, Hc_mean = 0.03, Hc_std = 0.05):
        '''
        Defines the lattice positions, magnetisation directions and coercive fields of an array of 
        square ASI
        Takes the unit cell from the initial defined parameters
        Generates a normally distributed range of coercive fields of the bars using Hc_mean and Hc_std as a percentage
        One thing to potentially change is to have the positions in nanometers
        '''
        self.type = 'square'
        self.side_len_x = 2*self.unit_cells_x+1
        self.side_len_y = 2*self.unit_cells_y+1
        grid = np.zeros((2*self.unit_cells_x+1, 2*self.unit_cells_y+1, 9))        
        for x in range(0, 2*self.unit_cells_x+1):
            for y in range(0, 2*self.unit_cells_y+1):
                if (x+y)%2 != 0:
                    if y%2 == 0:
                        xpos = x*(self.bar_length+self.vertex_gap)/2
                        ypos = y*(self.bar_length+self.vertex_gap)/2
                        grid[x,y] = np.array([x*self.unit_cell_len,y*self.unit_cell_len,0.,1.,0.,0., np.random.normal(loc=Hc_mean, scale=Hc_std*Hc_mean, size=None),0,None])
                    else:
                        grid[x,y] = np.array([x*self.unit_cell_len,y*self.unit_cell_len,0.,0.,1.,0.,np.random.normal(loc=Hc_mean, scale=Hc_std*Hc_mean, size=None),0,None])
                else:
                    if x%2 ==0:
                        grid[x,y] = np.array([x*self.unit_cell_len,y*self.unit_cell_len,0.,0.,0.,0.,0,0,0])
                    else:
                        grid[x,y] = np.array([x*self.unit_cell_len,y*self.unit_cell_len,0.,0.,0.,0.,0,0,None])
        self.lattice = grid

    def kagome(self, Hc_mean = 0.03, Hc_std = 0.05):
        '''
        Creates an array of Kagome ASI
        Takes the unit cell from the initial defined parameters
        Generates a normally distributed range of coercive fields of the bars using Hc_mean and Hc_std
        '''
        self.type = 'kagome'
        xfactor = 2*np.cos(np.pi/6)
        yfactor = 2*np.sin(np.pi/6)
        self.side_len_x = 2*self.unit_cells_x+1
        self.side_len_y = 4*self.unit_cells_y+1
        grid = np.zeros((2*self.unit_cells_x+1, 4*self.unit_cells_y+1,9))
        xfactor = 2*np.cos(np.pi/6)
        yfactor = 2*np.sin(np.pi/6)
        test= 0.7071
        for x in range(0, self.side_len_x):
            for y in range(0, self.side_len_y):
                if x%2!=0 and y%2==0:
                    if (x-1)%4==0 and (y-2)%4==0:
                        if y%(self.side_len_y-1)!=0:
                            grid[x+1,y] = np.array([xfactor*(x+1)*self.unit_cell_len,(y)*self.unit_cell_len,0.,0.,0.,0.,0.,0, 0])
                            grid[x-1,y] = np.array([xfactor*(x-1)*self.unit_cell_len,(y)*self.unit_cell_len,0.,0.,0.,0.,0.,0, 0])
                        grid[x,y] = np.array([xfactor*x*self.unit_cell_len,(y)*self.unit_cell_len,0.,1.,0.,0.,np.random.normal(loc=Hc_mean, scale=Hc_std*Hc_mean, size=None),0, None])
                    elif (x-3)%4==0 and (y)%4==0:
                        if y%(self.side_len_y-1)!=0:
                            grid[x+1,y] = np.array([xfactor*(x+1)*self.unit_cell_len,(y)*self.unit_cell_len,0.,0.,0.,0.,0.,0, 0])
                            grid[x-1,y] = np.array([xfactor*(x-1)*self.unit_cell_len,(y)*self.unit_cell_len,0.,0.,0.,0.,0.,0, 0])
                        grid[x,y] = np.array([xfactor*x*self.unit_cell_len,y*self.unit_cell_len,0.,1.,0.,0.,np.random.normal(loc=Hc_mean, scale=Hc_std*Hc_mean, size=None),0,None])
                    else:
                        grid[x,y] = np.array([xfactor*x*self.unit_cell_len,y*self.unit_cell_len,0.,0,0,0,0,0,None])
                elif x%2 ==0 and (y-1)%4==0:
                    if x%4==0:
                        grid[x,y] = np.array([xfactor*x*self.unit_cell_len,yfactor*y*self.unit_cell_len,0.,0.5,(3**0.5/2),0.,np.random.normal(loc=Hc_mean, scale=Hc_std*Hc_mean, size=None),0,None])
                    else:
                        grid[x,y] = np.array([xfactor*x*self.unit_cell_len,yfactor*y*self.unit_cell_len,0.,-0.5,(3**0.5/2),0.,np.random.normal(loc=Hc_mean, scale=Hc_std*Hc_mean, size=None),0,None])
                elif x%2 ==0 and (y-3)%4==0:
                    if x%4==0:
                        grid[x,y] = np.array([xfactor*x*self.unit_cell_len,yfactor*y*self.unit_cell_len,0.,-0.5,(3**0.5/2),0.,np.random.normal(loc=Hc_mean, scale=Hc_std*Hc_mean, size=None),0,None])
                    else:
                        grid[x,y] = np.array([xfactor*x*self.unit_cell_len,yfactor*y*self.unit_cell_len,0.,0.5,(3**0.5/2),0.,np.random.normal(loc=Hc_mean, scale=Hc_std*Hc_mean, size=None),0,None])
                else:
                    if np.array_equal(grid[x,y,0:2], [0., 0.]):
                        grid[x,y] = np.array([xfactor*x*self.unit_cell_len,y*self.unit_cell_len,0.,0,0,0,0,0,None])
        self.lattice = grid


    def short_shakti(self, Hc_mean = 0.03, Hc_std = 0.05):
        self.side_len_x = 4*self.unit_cells_x+1
        self.side_len_y = 4*self.unit_cells_y+1
        grid = np.zeros((self.side_len_x, self.side_len_y, 9))        
        for x in range(0, self.side_len_x):
            for y in range(0, self.side_len_y):
                if (x+y)%2 != 0:
                    if y%2 == 0:
                        grid[x,y] = np.array([x*self.unit_cell_len,y*self.unit_cell_len,0.,1.,0.,0., np.random.normal(loc=Hc_mean, scale=Hc_std*Hc_mean, size=None),0,None])
                    else:
                        grid[x,y] = np.array([x*self.unit_cell_len,y*self.unit_cell_len,0.,0.,1.,0.,np.random.normal(loc=Hc_mean, scale=Hc_std*Hc_mean, size=None),0,None])
                else:
                    if x%2 ==0:     # and y%(self.side_len_y-1)!=0 and x%(self.side_len_x-1)!=0
                        grid[x,y] = np.array([x*self.unit_cell_len,y*self.unit_cell_len,0.,0.,0.,0.,0,0,0])
                    else:
                        grid[x,y] = np.array([x*self.unit_cell_len,y*self.unit_cell_len,0.,0.,0.,0.,0,0,None])
        for x in range(0, self.side_len_x):
            for y in range(0, self.side_len_y):
                if (y-2)%8==0:
                    if (x-1)%8==0 or (x-3)%8==0:
                        grid[x,y] = np.array([x*self.unit_cell_len,y*self.unit_cell_len,0.,0.,0.,0.,0,0,None])
                if (y-6)%8==0:
                    if (x-5)%8==0 or (x-7)%8==0:
                        grid[x,y] = np.array([x*self.unit_cell_len,y*self.unit_cell_len,0.,0.,0.,0.,0,0,None])
                if (x-2)%8==0:
                    if (y-5)%8==0 or (y-7)%8==0:
                        grid[x,y] = np.array([x*self.unit_cell_len,y*self.unit_cell_len,0.,0.,0.,0.,0,0,None])
                if (x-6)%8==0:
                    if (y-1)%8==0 or (y-3)%8==0:
                        grid[x,y] = np.array([x*self.unit_cell_len,y*self.unit_cell_len,0.,0.,0.,0.,0,0,None])
        self.lattice = grid

    def tetris(self, Hc_mean = 0.03, Hc_std = 0.05):
        #Working on it
        self.side_len_x = 16*self.unit_cells_x+1
        self.side_len_y = 16*self.unit_cells_y+1
        grid = np.zeros((self.side_len_x, self.side_len_y, 9))        
        for x in range(0, self.side_len_x):
            for y in range(0, self.side_len_y):
                if (x+y)%2 != 0:
                    if y%2 == 0:
                        grid[x,y] = np.array([x*self.unit_cell_len,y*self.unit_cell_len,0.,1.,0.,0., np.random.normal(loc=Hc_mean, scale=Hc_std*Hc_mean, size=None),0,None])
                    else:
                        grid[x,y] = np.array([x*self.unit_cell_len,y*self.unit_cell_len,0.,0.,1.,0.,np.random.normal(loc=Hc_mean, scale=Hc_std*Hc_mean, size=None),0,None])
                else:
                    if x%2 ==0:     # and y%(self.side_len_y-1)!=0 and x%(self.side_len_x-1)!=0:
                        grid[x,y] = np.array([x*self.unit_cell_len,y*self.unit_cell_len,0.,0.,0.,0.,0,0,0])
                    else:
                        grid[x,y] = np.array([x*self.unit_cell_len,y*self.unit_cell_len,0.,0.,0.,0.,0,0,None])
        for x in range(0, self.side_len_x):
            for y in range(0, self.side_len_y):
                if (x)%16==0 and (y-5)%8==0:
                    grid[x,y] = np.array([x*self.unit_cell_len,y*self.unit_cell_len,0.,0.,0.,0.,0,0,None])
                if (x)%16==0 and (y-1)%8==0:
                    grid[x,y] = np.array([x*self.unit_cell_len,y*self.unit_cell_len,0.,0.,0.,0.,0,0,None])
                if (x-1)%16==0 and (y-2)%8==0:
                    grid[x,y] = np.array([(x+1)*self.unit_cell_len,(y+1)*self.unit_cell_len,0.,0.,0.,0.,0,0,None])
                    grid[x+1,y-1] = np.array([(x+2)*self.unit_cell_len,y*self.unit_cell_len,0.,0.,0.,0.,0,0,None])
                if (x-2)%16==0 and (y-7)%8==0:
                    grid[x,y] = np.array([x*self.unit_cell_len,y*self.unit_cell_len,0.,0.,0.,0.,0,0,None])
                    grid[x+1,y-1] = np.array([(x+1)*self.unit_cell_len,(y-1)*self.unit_cell_len,0.,0.,0.,0.,0,0,None])
                    grid[x+2,y] = np.array([(x+2)*self.unit_cell_len,y*self.unit_cell_len,0.,0.,0.,0.,0,0,None])
                if (x-4)%16==0 and (y-3)%8==0:
                    grid[x,y] = np.array([x*self.unit_cell_len,y*self.unit_cell_len,0.,0.,0.,0.,0,0,None])
                    grid[x+1,y+1] = np.array([(x+1)*self.unit_cell_len,(y+1)*self.unit_cell_len,0.,0.,0.,0.,0,0,None])
                    grid[x+2,y] = np.array([(x+2)*self.unit_cell_len,y*self.unit_cell_len,0.,0.,0.,0.,0,0,None])
                if (x-7)%16==0 and (y)%8==0:
                    grid[x,y] = np.array([x*self.unit_cell_len,y*self.unit_cell_len,0.,0.,0.,0.,0,0,None])    
                if (x-6)%16==0 and (y-1)%8==0:
                    grid[x,y] = np.array([x*self.unit_cell_len,y*self.unit_cell_len,0.,0.,0.,0.,0,0,None])
                    grid[x+2,y] = np.array([(x+2)*self.unit_cell_len,y*self.unit_cell_len,0.,0.,0.,0.,0,0,None])
                if (x-9)%16==0 and (y-6)%8==0:
                    grid[x,y] = np.array([x*self.unit_cell_len,y*self.unit_cell_len,0.,0.,0.,0.,0,0,None])
                    grid[x-1,y-1] = np.array([x*self.unit_cell_len,(y-1)*self.unit_cell_len,0.,0.,0.,0.,0,0,None])
                    grid[x+1,y-1] = np.array([(x+1)*self.unit_cell_len,(y-1)*self.unit_cell_len,0.,0.,0.,0.,0,0,None])
                if (x-11)%16==0 and (y-2)%8==0:
                    grid[x,y] = np.array([x*self.unit_cell_len,y*self.unit_cell_len,0.,0.,0.,0.,0,0,None])
                    grid[x-1,y+1] = np.array([x*self.unit_cell_len,(y+1)*self.unit_cell_len,0.,0.,0.,0.,0,0,None])
                    grid[x+1,y+1] = np.array([(x+1)*self.unit_cell_len,(y+1)*self.unit_cell_len,0.,0.,0.,0.,0,0,None])
                if (x-13)%16==0 and (y)%8==0:
                    grid[x,y] = np.array([x*self.unit_cell_len,y*self.unit_cell_len,0.,0.,0.,0.,0,0,None])
                    grid[x-1,y-1] = np.array([x*self.unit_cell_len,(y-1)*self.unit_cell_len,0.,0.,0.,0.,0,0,None])
                    grid[x+1,y-1] = np.array([(x+1)*self.unit_cell_len,(y-1)*self.unit_cell_len,0.,0.,0.,0.,0,0,None])
                if (x-14)%16==0 and (y-5)%8==0:
                    grid[x,y] = np.array([x*self.unit_cell_len,y*self.unit_cell_len,0.,0.,0.,0.,0,0,None])
                    grid[x+1,y-1] = np.array([(x+1)*self.unit_cell_len,(y-1)*self.unit_cell_len,0.,0.,0.,0.,0,0,None])
        self.lattice = grid
    '''
    def kagome2(self, , Hc_mean = 0.03, Hc_std = 0.05):
        self.type = 'kagome'
        self.side_len_x = 4*self.unit_cells_x+3
        self.side_len_y = 4*self.unit_cells_y+1
        grid = np.zeros((self.side_len_x, self.side_len_y,8))
        for x in range(0, self.side_len_x):
            for y in range(0, self.side_len_y):
                if x%2!=0 and y%4==0:
                    if (x-1)%4==0:
                        grid[x,y] = np.array([x*self.unit_cell_len,(y+2)*self.unit_cell_len,0.,1.,0.,0.,np.random.normal(loc=Hc_mean, scale=Hc_std*Hc_mean, size=None),0])
                    else:
                        grid[x,y] = np.array([x*self.unit_cell_len,y*self.unit_cell_len,0.,1.,0.,0.,np.random.normal(loc=Hc_mean, scale=Hc_std*Hc_mean, size=None),0])
                elif x%2 ==0 and (y-1)%4==0:
                    if x%4==0:
                        grid[x,y] = np.array([x*self.unit_cell_len,y*self.unit_cell_len,0.,0.5,(3**0.5/2),0.,np.random.normal(loc=Hc_mean, scale=Hc_std*Hc_mean, size=None),0])
                    else:
                        grid[x,y] = np.array([x*self.unit_cell_len,y*self.unit_cell_len,0.,-0.5,(3**0.5/2),0.,np.random.normal(loc=Hc_mean, scale=Hc_std*Hc_mean, size=None),0])
                elif x%2 ==0 and (y-3)%4==0:
                    if x%4==0:
                        grid[x,y] = np.array([x*self.unit_cell_len,y*self.unit_cell_len,0.,-0.5,(3**0.5/2),0.,np.random.normal(loc=Hc_mean, scale=Hc_std*Hc_mean, size=None),0])
                    else:
                        grid[x,y] = np.array([x*self.unit_cell_len,y*self.unit_cell_len,0.,0.5,(3**0.5/2),0.,np.random.normal(loc=Hc_mean, scale=Hc_std*Hc_mean, size=None),0])
                else:
                    grid[x,y] = np.array([x*self.unit_cell_len,y*self.unit_cell_len,0.,0,0,0,0,0])
        self.lattice = grid
    '''
    
    def graph(self):
        '''
        Plots the positions and directions of the bar magnetisations as a quiver graph
        '''
        grid = self.lattice
        X = grid[:,:,0].flatten()
        Y = grid[:,:,1].flatten()
        z = grid[:,:,2].flatten()
        Mx = grid[:,:,3].flatten()
        My = grid[:,:,4].flatten()
        Mz = grid[:,:,5].flatten()
        Hc = grid[:,:,6].flatten()
        C = grid[:,:,7].flatten()
        fig, ax =plt.subplots(ncols = 2,sharex=True, sharey=True)
        plt.set_cmap(cm.jet)
        graph = ax[0].quiver(X, Y, Mx, My, Hc, angles='xy', scale_units='xy',  pivot = 'mid')
        ax[0].set_xlim([-1*self.unit_cell_len, self.side_len_x*self.unit_cell_len])
        ax[0].set_ylim([-1*self.unit_cell_len, self.side_len_y*self.unit_cell_len])
        ax[0].set_title('Coercive Field')
        cb1 = fig.colorbar(graph, fraction=0.046, pad=0.04, ax = ax[0], format='%.2e',boundaries = np.linspace(np.min(Hc[np.nonzero(Hc)]), max(Hc),1000))
        cb1.locator = MaxNLocator( nbins = 7)
        cb1.update_ticks()
        graph = ax[1].quiver(X, Y, Mx, My, C, angles='xy', scale_units='xy',  pivot = 'mid')
        ax[1].set_xlim([-1*self.unit_cell_len, self.side_len_x*self.unit_cell_len])
        ax[1].set_ylim([-1*self.unit_cell_len, self.side_len_y*self.unit_cell_len])
        ax[1].set_title('Counts')
        cb2 = fig.colorbar(graph, fraction=0.046, pad=0.04, ax = ax[1])
        cb2.locator = MaxNLocator( nbins = 5)
        cb2.update_ticks()
        for axes in ax:
            axes.plot([1, 2, 3], [1, 2, 3])
            axes.set(adjustable='box-forced', aspect='equal')
            plt.gca().xaxis.set_major_locator( MaxNLocator(nbins = 7, prune = 'lower') )
            plt.gca().yaxis.set_major_locator( MaxNLocator(nbins = 6) )
        plt.ticklabel_format(style='sci', scilimits=(0,0))
        plt.tight_layout()
        plt.draw()
        plt.show()
        

    def resetCount(self):
        '''
        Resets the count parameter in the lattice
        '''
        for x in range(0, self.side_len_x):
            for y in range(0, self.side_len_y):
                self.lattice[x,y,7] = 0
    
    def subtractCount(self, lattice1, lattice2):
        '''
        Haven't actually tested yet.
        Should take two instances of the ASI_RPM class and then return the difference between the number of spins flipped
        '''
        l1 = lattice1.returnLattice()
        l2 = lattice2.returnLattice()
        diff = l2[:,:,7] - l1[:,:,7]
        #print(diff)
        l1[:,:,7] = diff
        return(self(self.unit_cells_x, self.unit_cells_y,lattice = diff))

    
    def relax(self, Happlied = np.array([0.,0.,0.]), n=10):
        '''
        Steps through all the the positions in the lattice and if the field applied along the direction
        of the bar is negative and greater than the coercive field then it switches the magnetisation
        of the bar
        '''
        grid = copy.deepcopy(self.lattice)
        unrelaxed = True
        Happlied[Happlied == -0.] = 0.
        print(Happlied)
        while unrelaxed == True:
            flipcount = 0
            for x in range(0, self.side_len_x):
                for y in range(0, self.side_len_y):
                    if abs(grid[x,y,6]) != 0:
                        unit_vector = grid[x,y,3:6]/np.linalg.norm(grid[x,y,3:6])
                        field = np.dot(np.array(Happlied+self.Hlocal2(x,y, n=n)), unit_vector)
                        #print(field)
                        if field < -grid[x,y,6]:
                            #print(grid[x,y,3:5])
                            grid[x,y,3:5] = np.negative(grid[x,y,3:5])
                            #print(grid[x,y,3:5])
                            grid[x,y,:][grid[x,y,:]==0.] = 0.
                            grid[x,y,7] += 1
                            flipcount += 1
                            #print(grid[x,y,3:5])
            print("no of flipped spins in relax", flipcount)
            grid[grid==-0.] = 0.
            if flipcount > 0:
                unrelaxed = True
            else:
                unrelaxed = False
            self.lattice = grid
    
    
    def fieldsweep(self, Hmax, steps, Htheta, n=10, loops=1, folder = None):
        '''
        Sweeps through field up to a maximum field of Hmax in 
        '''
        M0 = copy.deepcopy(self)
        Htheta = np.pi*Htheta/180
        q = []
        mag = []
        monopole = []
        fieldloops = []
        field_steps = np.linspace(0,Hmax,steps+1)
        field_steps = np.append(field_steps, np.linspace(Hmax,-Hmax,2*steps+1))
        field_steps = np.append(field_steps, np.linspace(-Hmax,0,steps+1))
        counter = 0
        for i in range(0, loops):
            self.previous = copy.deepcopy(self)
            for j in field_steps:
                Happlied = j*np.array([np.cos(Htheta),np.sin(Htheta), 0.])
                print('Happlied: ', Happlied)
                self.relax(Happlied,n)
                fieldloops.append(np.array([i, j]))
                mag.append(self.netMagnetisation())
                monopole.append(self.monopoleDensity())
                q.append(self.correlation(self.previous,self))
                if folder ==None:
                    self.save('Lattice_'+'Loop'+str(i)+'_FieldStrength'+str(np.round(j*1000,2))+'mT_Angle'+str(np.round(Htheta, 2)))
                else:
                    if not os.path.exists(folder):
                        os.makedirs(folder)
                    self.save('Lattice_'+str(counter)+'Loop'+str(i)+'_FieldStrength'+str(np.round(j*1000,2))+'mT_Angle'+str(np.round(Htheta, 2)), folder = folder)
                counter+=1
        return(np.array(fieldloops),np.array(q), np.array(mag), np.array(monopole))
    
    #for Hx, Hy in np.meshgrid(Hx_list, Hy_list, sparse = True):
    #np.meshgrid(Hx_list, Hy_list, sparse = True):
    
    
    def dipole(self, m, r, r0):
        """Calculate a field in point r created by a dipole moment m located in r0.
        Spatial components are the outermost axis of r and returned B.
        """
        m = np.array(m)
        r = np.array(r)
        r0 = np.array(r0)
        m = self.magnetisation*self.bar_length*self.bar_width*self.bar_thickness*m
        #print(r,r0)
        #r = (self.vertex_gap+self.bar_length/2)*r
        #r0 = (self.vertex_gap+self.bar_length/2)*r0
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

    def dumbbell(self, m, r, r0):
        m = np.array(m)
        r = np.array(r)
        r0 = np.array(r0)
        m = self.magnetisation*self.bar_length*self.bar_width*self.bar_thickness*m
        R = np.subtract(np.transpose(r), r0).T

        

    def fieldreturn(self, n=5):
        grid = self.lattice
        field = np.zeros((self.side_len_x,self.side_len_y,3))
        for x in range(0, self.side_len_x):
            for y in range(0, self.side_len_y):
                field[x,y,:] = self.Hlocal2(x, y, n=n)
        X = grid[:,:,0].flatten()
        Y = grid[:,:,1].flatten()
        Hx = field[:,:, 0].flatten()
        Hy = field[:,:, 1].flatten()
        Hz = field[:,:, 2].flatten()
        return(X,Y,Hx,Hy,Hz)
    
    def fieldplot(self, n=5):
        grid = self.lattice
        field = np.zeros((self.side_len_x,self.side_len_y,3))
        for x in range(0, self.side_len_x):
            for y in range(0, self.side_len_y):
                field[x,y,:] = self.Hlocal2(x, y, n=n)
        X = grid[:,:,0].flatten()
        Y = grid[:,:,1].flatten()
        Hx = field[:,:, 0].flatten()
        Hy = field[:,:, 1].flatten()
        Hz = field[:,:, 2].flatten()
        fig, ax =plt.subplots(ncols = 2,sharex=True, sharey=True)
        plt.set_cmap(cm.plasma)
        graph = ax[0].quiver(X, Y, Hx, Hy, angles='xy', scale_units='xy',  pivot = 'mid')
        #qk = ax[0].quiverkey(graph, 0.45, 0.9, 10, r'$mT$', labelpos='E',
        #           coordinates='figure')
        ax[0].set_xlim([-1*self.unit_cell_len, self.side_len_x*self.unit_cell_len])
        ax[0].set_ylim([-1*self.unit_cell_len, self.side_len_y*self.unit_cell_len])
        ax[0].set_title('In Plane Field')
        #fig.colorbar(graph, ax = ax[0],boundaries = np.linspace(np.min(Hc[np.nonzero(Hc)]), max(Hc),1000))
        graph = ax[1].scatter(X, Y, Hz, marker='o', )
        ax[1].set_xlim([-1*self.unit_cell_len, self.side_len_x*self.unit_cell_len])
        ax[1].set_ylim([-1*self.unit_cell_len, self.side_len_y*self.unit_cell_len])
        ax[1].set_title('Out of Plane Field')
        for axes in ax:
            axes.plot([1, 2, 3], [1, 2, 3])
            axes.set(adjustable='box-forced', aspect='equal')
        plt.ticklabel_format(style='sci', scilimits=(0,0))
        plt.tight_layout()
        print(Hz)
        #fig.colorbar(graph, ax = ax[0],boundaries = np.linspace(np.min(Hz), max(Hz),1000))
        plt.draw()
        plt.show()


    
    def vertexCharge(self):
        '''
        Working on it
        '''
        grid = self.lattice
        #print("unit cells x = ",self.unit_cells_x)
        #print("unit cells y = ",self.unit_cells_y)
        chargeGrid = np.zeros(((self.unit_cells_x-1)*(self.unit_cells_y-1), 3))     
        #print("charge grid initial =",chargeGrid)
        #Hl = []
        #x1 = col - 1
        #x2 = col 
        #y1 = row
        #y2 = row
        i = 0
        for y in range(2, self.side_len_y-2,2):
            for x in range(2, self.side_len_x-2,2):
                if grid[x,y,6] == 0:
                    m1 = grid[x-1,y,3]
                    m2 = grid[x+1,y,3]
                    m3 = grid[x,y+1,4]
                    m4 = grid[x,y-1,4]
                    #print("m1 =",m1)
                    #print("m2 =",m2)
                    #print("m3 =",m3)
                    #print("m4 =",m4)
                    charge = m1-m2-m3+m4
                    #print("charge = ",x ,y, charge)
                    #grid[x,y,8] = charge
                    #print("i =", i)
                    chargeGrid[i] = np.array([grid[x,y,0],grid[x,y,1],charge])
                    #print("charge grid =",chargeGrid)
                    i = i+1
                    #x+=x
            #y=y+1
        #self.lattice = grid
        return(chargeGrid)
                    
    
    def graphCharge(self):
            '''
            Plots the positions and directions of the bar magnetisations as a quiver graph
            '''
            grid = self.lattice
            chargeGrid = self.vertexCharge()
            print("vertex charge tech yields =",chargeGrid)
            X1 = grid[:,:,0].flatten()
            Y1 = grid[:,:,1].flatten()
            z = grid[:,:,2].flatten()
            Mx = grid[:,:,3].flatten()
            My = grid[:,:,4].flatten()
            Mz = grid[:,:,5].flatten()
            Hc = grid[:,:,6].flatten()
            C = grid[:,:,7].flatten()
            X2 = chargeGrid[:,0]
            Y2 = chargeGrid[:,1]
            MagCharge = chargeGrid[:,2]
            #print("x2 =",X2)
            #print("y2 =",Y2)
            #print("MagCharge =",MagCharge)
            
            fig = plt.figure(figsize=(6,6))
            ax = fig.add_subplot(111)
            ax.set_xlim([-1*self.unit_cell_len, self.side_len_x*self.unit_cell_len])
            ax.set_ylim([-1*self.unit_cell_len, self.side_len_y*self.unit_cell_len])
            ax.set_title("Vertex Magnetic Charge Map",fontsize=14)
            #ax.set_xlabel("XAVG",fontsize=12)
            #ax.set_ylabel("YAVG",fontsize=12)
            #ax.grid(True,linestyle='-',color='0.75')

            ax.quiver(X1, Y1, Mx, My, angles='xy', scale_units='xy',  pivot = 'mid', zorder=1)
            # scatter with colormap mapping to z value
            ax.scatter(X2,Y2,s=80,c=MagCharge, marker = 'o', cmap = cm.seismic, zorder=2, edgecolor='k' );
            
            #Y2 = grid[:,:,1].flatten()
            #Charge = grid[:,:,8].flatten()
            #Charge = np.array(Charge, dtype = np.double)
            #Charge[ Charge == 0] = np.nan
            #cmap = matplotlib.cm.get_cmap('viridis')
            #normalize = matplotlib.colors.Normalize(vmin=min(MagCharge), vmax=max(MagCharge))
            #colors = [cmap(normalize(value)) for value in MagCharge]
            #ax = plt.gca()
            #fig, ax =plt.subplots(ncols = 2,sharex=True, sharey=True)
            #plt.set_cmap(cm.jet)
            
            #ax.scatter(X2,Y2,color=colors)
            #ax.set_xlim([-1*self.unit_cell_len, self.side_len_x*self.unit_cell_len])
            #ax.set_ylim([-1*self.unit_cell_len, self.side_len_y*self.unit_cell_len])
            #ax.set_title('Vertex Charge Map')
            
            
            
            
                        
            #cb1 = ax.colorbar(graph, fraction=0.046, pad=0.04, ax = ax, format='%.2e',boundaries = np.linspace(np.min(Hc[np.nonzero(Hc)]), max(Hc),1000))
            #cb1.locator = MaxNLocator( nbins = 7)
            #cb1.update_ticks()
            plt.ticklabel_format(style='sci', scilimits=(0,0))
            plt.tight_layout()
            #plt.draw()
            #plt.show()


    
    def Hlocal2(self, x,y,n =1):
        Hl = []
        x1 = x - 2*n
        x2 = x + 2*n
        y1 = y - 2*n
        y2 = y + 2*n

        if x1<0:
            x1 = 0
        if x2>self.side_len_x:
            x2 = self.side_len_x -1
        if y1<0:
            y1 = 0
        if y2>self.side_len_y-1:
            y2 = self.side_len_y-1

        grid = self.lattice[x1:x2+1,y1:y2+1,:]
        m = grid[:,:,3:6]
        m = m.reshape(-1, m.shape[-1])
        r = grid[:,:,0:3]
        r = r.reshape(-1, r.shape[-1])
        r0 = self.lattice[x,y,0:3]

        for pos, mag in zip(r, m):
            if np.linalg.norm(pos-r0)/(n+1)<=1.0 and np.array_equal(pos, r0)!=True:
                Hl.append(self.dipole(mag, r0, pos))
        return(sum(Hl))



    def randomMag(self, seed = None):
        State = np.random.RandomState(seed=seed)
        grid = self.lattice
        for x in range(0, self.side_len_x):
            for y in range(0, self.side_len_y):
                if grid[x,y,6] != 0:
                    if State.uniform(low=0.0, high=1.0)>0.5:
                        grid[x,y,3:5]=-1.*grid[x,y,3:5]
        self.lattice = grid

    def correlation(self, lattice1, lattice2):
        l1 = lattice1.returnLattice()
        l2 = lattice2.returnLattice()
        total = 0
        same = 0
        for x in range(0, self.side_len_x):
            for y in range(0, self.side_len_y):
                if l1[x,y,6]!=0:
                    if np.array_equal(l1[x,y, 3:5], l2[x,y,3:5]) ==True:
                        same+=1.0
                    total +=1.0
        print("Same total:",same)
        print("Absolute total:", total)
        print('Correlation factor:',same/total)
        return(same/total)
        
    """
    def correlation(self, lattice1, lattice2):
        l1 = lattice1.returnLattice()
        l2 = lattice2..returnLattice()
        total = 0
        same = 0
        for x in range(0, self.side_len_x):
            for y in range(0, self.side_len_y):
                if lattice1[x,y,4]!=0:
                    if np.array_equal(lattice1[x,y, 2:4], lattice2[x,y,2:4]) ==True:
                        same+=1.0
                        print("same running total",same)
                    total +=1.0
                    print("total running total",total)
        print("same total",same)
        print("absolute total", total)
        #q 
        return(same/total)
    """

    def netMagnetisation(self):
        grid = copy.deepcopy(self.lattice)
        #grid[grid[:,:,0] == 0] = np.nan
        grid[grid[:,:,6]==0] = np.nan
        mx = grid[:,:,3].flatten()
        my = grid[:,:,4].flatten()
        return(np.array([np.nanmean(mx),np.nanmean(my)]))
        
    def monopoleDensity(self):

		#4in/0out have a charge of 1
		#3in/1out have a charge of 0.5
		#The density is then calculated by dividing by the total area minus the edges

    	grid = self.lattice
    	chargeGrid = self.vertexCharge()
    	return(np.sum(np.absolute(chargeGrid[:,2]))/(4*(self.unit_cells_x-1)*(self.unit_cells_y-1)))

    def returnLattice(self):
        return(self.lattice)

    def switchBar(self, x,y):
        self.lattice[x,y, 2:4] *= -1

    def changeBarlen(self, newbar_length):
        self.bar_length = newbar_length

    def changeVertexgap(self, newvertex_gap):
        self.vertex_gap = newvertex_gap

    def changeMagnetisation(self, new_magnetisation):
        self.magnetisation = new_magnetisation



'''
Hc = 0.062
Hc_std = 0.05
bar_length = 220e-9
vertex_gap = 1e-7
bar_thickness = 25e-9
bar_width = 80e-9
magnetisation = 800e3
'''
'''
#Graphing and save/load test
kagomeLattice = ASI_RPM(10, 10)
kagomeLattice.kagome()
filename = 'KagomeTest.npy'
kagomeLattice.save(os.path.join(os.getcwd(),filename))
kagomeLattice.randomMag()
kagomeLattice.graph()
#kagomeLattice.load(os.path.join(os.getcwd(),filename))
#kagomeLattice.graph()
kagomeLattice.fieldplot()
plt.show()
'''

#field sweep test, count different test
'''
angle = 45
Hamp = 1.3*Hc
squareLattice = ASI_RPM(6, 6, bar_length = bar_length,\
 vertex_gap = vertex_gap, bar_thickness = bar_thickness,\
 bar_width = bar_width, magnetisation = magnetisation)
squareLattice.square(Hc_mean=Hc, Hc_std=Hc_std)
print(squareLattice.monopoleDensity())
print(squareLattice.netMagnetisation())
squareLattice.randomMag()
print(squareLattice.monopoleDensity())
squareLattice.randomMag()
print(squareLattice.monopoleDensity())
'''
'''
print(squareLattice.netMagnetisation())
#squareLattice.randomMag()
#squareLattice.vertexCharge()
squareLattice.graphCharge()
squareLattice.graph()
#squareLattice.fieldplot()
#plt.show()
Hmax = Hamp/np.cos(np.pi*angle/180)
steps = 20
field_steps = np.linspace(0,Hmax,steps+1)
field_steps = np.append(field_steps, np.linspace(Hmax,-Hmax,2*steps+1))
field_steps = np.append(field_steps, np.linspace(-Hmax,0,steps+1))
q, Mag = squareLattice.fieldsweep(Hamp/np.cos(np.pi*angle/180),20,angle, n = 3, loops = 2)
fig = plt.figure()
plt.plot(np.tile(field_steps,2),Mag)
plt.show()
#squareLattice.graph()
#squareLattice.fieldplot()


#def makePlot(x,y):
#    fig, ax =plt.subplots()
#    ax.plot(x, y)

#makePlot(np.arange(1, len(q)+1), q)

plt.show()      #makes sure this is at the end of the code
'''