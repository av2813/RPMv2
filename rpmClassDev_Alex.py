import numpy as np
import matplotlib as mpl
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
        self.Hc = None
        self.Hc_std = None
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
            self.bar_thickness,self.magnetisation, self.side_len_x,\
            self.side_len_y, self.type, self.Hc, self.Hc_std])
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
        self.bar_length = np.float(parameters[2])
        self.vertex_gap = np.float(parameters[3])
        self.bar_width = np.float(parameters[4])
        self.bar_thickness = np.float(parameters[5])
        self.magnetisation = np.float(parameters[6])
        self.side_len_x = np.int(parameters[7])
        self.side_len_y = np.int(parameters[8])
        self.type = parameters[9]
        self.Hc = np.float(parameters[10])
        self.Hc_std = np.float(parameters[11])
        self.lattice = npzfile['arr_0']

    def update(self, file, lattice_type, Hc, Hc_std):
        '''
        Still have some bugs to work out.
        Don't use this on any important data!!
        '''
        npzfile = np.load(file)
        parameters = npzfile['arr_1']
        print(parameters)
        print(len(parameters))
        if len(parameters)!=12:
            self.unit_cells_x = np.int(parameters[0])
            self.unit_cells_y = np.int(parameters[1])
            self.bar_length = np.float(parameters[2])
            self.vertex_gap = np.float(parameters[3])
            self.bar_width = np.float(parameters[4])
            self.bar_thickness = np.float(parameters[5])
            self.magnetisation = np.float(parameters[6])
            #self.side_len_x = np.int(parameters[7])
            #self.side_len_y = np.int(parameters[8])
            #self.lattice = npzfile['arr_0']
            grid1 = copy.deepcopy(npzfile['arr_0'])
            self.side_len_x = 2*self.unit_cells_x+1
            self.side_len_y = 2*self.unit_cells_y+1
            self.square()
            grid2 = copy.deepcopy(self.lattice)
            print(np.shape(grid1), np.shape(grid2))
            if lattice_type == 'square':
                grid3 = np.zeros((self.side_len_x,self.side_len_x,9))
                grid3[:,:,0:8] = copy.deepcopy(grid1[:,:,0:8])
                grid3[:,:,8] = copy.deepcopy(grid2[:,:,8])
            self.lattice = copy.deepcopy(grid3)
            self.type = lattice_type
            self.Hc = Hc
            self.Hc_std = Hc_std
            print(file.replace('.npz',''))
            self.save(file.replace('.npz','_new'))
        else:
            print('done')
            self.load(file)


    def updateFolder(self, folder,lattice_type, Hc, Hc_std):
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file[-4:] == '.npz':
                    self.update(os.path.join(root,file), lattice_type, Hc, Hc_std)

    def square(self, Hc_mean = 0.062, Hc_std = 0.05):
        '''
        Defines the lattice positions, magnetisation directions and coercive fields of an array of 
        square ASI
        Takes the unit cell from the initial defined parameters
        Generates a normally distributed range of coercive fields of the bars using Hc_mean and Hc_std as a percentage
        One thing to potentially change is to have the positions in nanometers
        '''
        self.type = 'square'
        self.Hc = Hc_mean
        self.Hc_std = Hc_std
        self.side_len_x = 2*self.unit_cells_x+1
        self.side_len_y = 2*self.unit_cells_y+1
        grid = np.zeros((self.side_len_x, self.side_len_y, 9))        
        for x in range(0, self.side_len_x):
            for y in range(0, self.side_len_y):
                if (x+y)%2 != 0:
                    if y%2 == 0:
                        grid[x,y] = np.array([x*self.unit_cell_len,y*self.unit_cell_len,0.,1.,0.,0., np.random.normal(loc=Hc_mean, scale=Hc_std*Hc_mean, size=None),0,None])
                    else:
                        grid[x,y] = np.array([x*self.unit_cell_len,y*self.unit_cell_len,0.,0.,1.,0.,np.random.normal(loc=Hc_mean, scale=Hc_std*Hc_mean, size=None),0,None])
                else:
                    if x%2 ==0 and x!=0 and y!=0 and x!=self.side_len_x-1 and y!=self.side_len_x-1:
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
        self.Hc = Hc_mean
        self.Hc_std = Hc_std
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
                            grid[x+1,y] = np.array([xfactor*(x+test)*self.unit_cell_len,(y)*self.unit_cell_len,0.,0.,0.,0.,0.,0, 0])
                            grid[x-1,y] = np.array([xfactor*(x-test)*self.unit_cell_len,(y)*self.unit_cell_len,0.,0.,0.,0.,0.,0, 0])
                        grid[x,y] = np.array([xfactor*x*self.unit_cell_len,(y)*self.unit_cell_len,0.,1.,0.,0.,np.random.normal(loc=Hc_mean, scale=Hc_std*Hc_mean, size=None),0, None])
                    elif (x-3)%4==0 and (y)%4==0:
                        if y%(self.side_len_y-1)!=0:
                            grid[x+1,y] = np.array([xfactor*(x+test)*self.unit_cell_len,(y)*self.unit_cell_len,0.,0.,0.,0.,0.,0, 0])
                            grid[x-1,y] = np.array([xfactor*(x-test)*self.unit_cell_len,(y)*self.unit_cell_len,0.,0.,0.,0.,0.,0, 0])
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
        self.type = 'long_shakti'
        self.Hc = Hc_mean
        self.Hc_std = Hc_std
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


        def long_shakti(self, Hc_mean = 0.062, Hc_std = 0.05):
            self.type = 'long_shakti'
            self.Hc = Hc_mean
            self.Hc_std = Hc_std
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
                        if x%2 ==0:     #and y%(self.side_len_y-1)!=0 and x%(self.side_len_x-1)!=0
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
            for x in range(0, self.side_len_x):
                for y in range(0, self.side_len_y):
                    if (y-2)%8==0:
                        if (x-5)%8==0 or (x-7)%8==0:
                            grid[x,y] = np.array([x*self.unit_cell_len,y*self.unit_cell_len,0.,0.,0.,0.,0,0,None])
                        if (x-6)%8==0:
                            grid[x,y] = np.array([(x)*self.unit_cell_len,y*self.unit_cell_len,0.,2.,0.,0.,np.random.normal(loc=Hc_mean, scale=Hc_std*Hc_mean, size=None),0,None])
                    if (y-6)%8==0:
                        if (x-1)%8==0 or (x-3)%8==0:
                            grid[x,y] = np.array([x*self.unit_cell_len,y*self.unit_cell_len,0.,0.,0.,0.,0,0,None])
                        if (x-2)%8==0:
                            grid[x,y] = np.array([(x)*self.unit_cell_len,y*self.unit_cell_len,0.,2.,0.,0.,np.random.normal(loc=Hc_mean, scale=Hc_std*Hc_mean, size=None),0,None])
                    if (x-2)%8==0:
                        if (y-1)%8==0 or (y-3)%8==0:
                            grid[x,y] = np.array([x*self.unit_cell_len,y*self.unit_cell_len,0.,0.,0.,0.,0,0,None])
                        if (y-2)%8==0:
                            grid[x,y] = np.array([(x)*self.unit_cell_len,y*self.unit_cell_len,0.,0.,2.,0.,np.random.normal(loc=Hc_mean, scale=Hc_std*Hc_mean, size=None),0,None])
                    if (x-6)%8==0:
                        if (y-5)%8==0 or (y-7)%8==0:
                            grid[x,y] = np.array([x*self.unit_cell_len,y*self.unit_cell_len,0.,0.,0.,0.,0,0,None])
                        if (y-6)%8==0:
                            grid[x,y] = np.array([(x)*self.unit_cell_len,y*self.unit_cell_len,0.,0.,2.,0.,np.random.normal(loc=Hc_mean, scale=Hc_std*Hc_mean, size=None),0,None])
            self.lattice = grid

    def tetris(self, Hc_mean = 0.03, Hc_std = 0.05):
        self.type = 'tetris'
        self.Hc = Hc_mean
        self.Hc_std = Hc_std
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
        Charge = grid[:,:,8].flatten()
        fig, ax =plt.subplots(ncols = 2,sharex=True, sharey=True)
        plt.set_cmap(cm.jet)
        graph = ax[0].quiver(X, Y, Mx, My, Hc, angles='xy', scale_units='xy',  pivot = 'mid')
        ax[0].set_xlim([-1*self.unit_cell_len, np.max(X)+self.unit_cell_len])
        ax[0].set_ylim([-1*self.unit_cell_len, np.max(X)+self.unit_cell_len])
        ax[0].set_title('Coercive Field')
        cb1 = fig.colorbar(graph, fraction=0.046, pad=0.04, ax = ax[0], format='%.2e',boundaries = np.linspace(np.min(Hc[np.nonzero(Hc)]), max(Hc),1000))
        cb1.locator = MaxNLocator( nbins = 7)
        cb1.update_ticks()
        graph = ax[1].quiver(X, Y, Mx, My, C, angles='xy', scale_units='xy',  pivot = 'mid')
        ax[1].set_xlim([-1*self.unit_cell_len, np.max(Y)+self.unit_cell_len])
        ax[1].set_ylim([-1*self.unit_cell_len, np.max(Y)+self.unit_cell_len])
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
        fig, ax =plt.subplots()
        plt.scatter(X, Y, c = Charge)
        plt.quiver(X, Y, Mx, My, Hc, angles='xy', scale_units='xy',  pivot = 'mid')
        ax.set_xlim([-1*self.unit_cell_len, np.max(X)+self.unit_cell_len])
        ax.set_ylim([-1*self.unit_cell_len, np.max(Y)+self.unit_cell_len])
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
        while unrelaxed == True:
            flipcount = 0
            for x in range(0, self.side_len_x):
                for y in range(0, self.side_len_y):
                    if abs(grid[x,y,6]) != 0:
                        unit_vector = grid[x,y,3:6]
                        field = np.dot(np.array(Happlied+self.Hlocal2(x,y, n=n)), unit_vector)
                        if field < -grid[x,y,6]:
                            grid[x,y,3:5] = np.negative(grid[x,y,3:5])
                            grid[x,y,:][grid[x,y,:]==0.] = 0.
                            grid[x,y,7] += 1
                            flipcount += 1
            print("no of flipped spins in relax", flipcount)
            grid[grid==-0.] = 0.
            if flipcount > 0:
                unrelaxed = True
            else:
                unrelaxed = False
            self.lattice = grid

    def relax2(self, Happlied = np.array([0., 0., 0.]), n=10):
        grid = copy.deepcopy(self.lattice)
        Happlied[Happlied == 0.] = 0.
    
    
    def fieldSweep(self, Hmax, steps, Htheta, n=10, loops=1, folder = None):
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
            self.localCorrelation()
            #self.vertexHistogram()
            #self.correlationHistogram()
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

    def fieldReturn(self, n=5):
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
    
    def fieldPlot(self, n=5):
        grid = self.lattice
        field = np.zeros((self.side_len_x,self.side_len_y,3))
        for x in range(0, self.side_len_x):
            for y in range(0, self.side_len_y):
                field[x,y,:] = self.Hlocal2(x, y, n=n)
        X = grid[:,:,0].flatten()
        Y = grid[:,:,1].flatten()
        Mx = grid[:,:,3].flatten()
        My = grid[:,:,4].flatten()
        Hx = field[:,:, 0].flatten()
        Hy = field[:,:, 1].flatten()
        Hz = field[:,:, 2].flatten()
        fig, ax =plt.subplots(ncols = 2,sharex=True, sharey=True)
        plt.set_cmap(cm.plasma)
        graph = ax[0].quiver(X, Y, Hx, Hy,(Hx**2+Hy**2)**0.5, angles='xy', scale_units='xy',  pivot = 'mid')
        cb1 = fig.colorbar(graph, fraction=0.046, pad=0.04, ax = ax[0])
        cb1.locator = MaxNLocator(nbins = 8)
        cb1.update_ticks()
        #qk = ax[0].quiverkey(graph, 0.45, 0.9, 10, r'$mT$', labelpos='E',
        #           coordinates='figure')
        ax[0].set_xlim([-1*self.unit_cell_len, np.max(X)+self.unit_cell_len])
        ax[0].set_ylim([-1*self.unit_cell_len, np.max(Y)+self.unit_cell_len])
        ax[0].set_title('In Plane Field')
        #fig.colorbar(graph, ax = ax[0],boundaries = np.linspace(np.min(Hc[np.nonzero(Hc)]), max(Hc),1000))
        graph = ax[1].scatter(X, Y,c = (Hx**2+Hy**2)**0.5, marker='o')
        ax[1].quiver(X,Y,Mx, My, angles='xy', scale_units='xy',  pivot = 'mid')
        ax[1].set_xlim([-1*self.unit_cell_len, np.max(X)+self.unit_cell_len])
        ax[1].set_ylim([-1*self.unit_cell_len, np.max(Y)+self.unit_cell_len])
        ax[1].set_title('Field Magnitude')
        cb2 = fig.colorbar(graph, fraction=0.046, pad=0.04, ax = ax[1])
        cb2.locator = MaxNLocator(nbins = 8)
        cb2.update_ticks()
        for axes in ax:
            axes.plot([1, 2, 3], [1, 2, 3])
            axes.set(adjustable='box-forced', aspect='equal')
        plt.ticklabel_format(style='sci', scilimits=(0,0))
        plt.tight_layout()
        #fig.colorbar(graph, ax = ax[0],boundaries = np.linspace(np.min(Hz), max(Hz),1000))
        plt.draw()
        plt.show()

    def vertexCharge(self):
        '''
        Old Vertex charge determining function
        '''
        grid = self.lattice
        chargeGrid = np.zeros(((self.unit_cells_x-1)*(self.unit_cells_y-1), 3))     
        i = 0
        for y in range(2, self.side_len_y-2,2):
            for x in range(2, self.side_len_x-2,2):
                if grid[x,y,6] == 0:
                    m1 = grid[x-1,y,3]
                    m2 = grid[x+1,y,3]
                    m3 = grid[x,y+1,4]
                    m4 = grid[x,y-1,4]
                    charge = m1-m2-m3+m4
                    chargeGrid[i] = np.array([grid[x,y,0],grid[x,y,1],charge])
                    i = i+1
        return(chargeGrid)

    def vertexCharge2(self):
        grid = copy.deepcopy(self.lattice)
        for x in np.arange(0, self.side_len_x):
            for y in np.arange(0, self.side_len_y):
                if np.isnan(grid[x,y,8])!=True:
                    x1 = x - 1
                    x2 = x + 2
                    y1 = y - 1
                    y2 = y + 2

                    if x1<0:
                        x1 = 0
                    if x2>self.side_len_x:
                        x2 = self.side_len_x
                    if y1<0:
                        y1 = 0
                    if y2>self.side_len_y:
                        y2 = self.side_len_y
                    local = grid[x1:x2,y1:y2]
                    charge = (np.sum(local[0:2,0:2, 3:6])-np.sum(local[1:3,1:3, 3:6]))/4.
                    if self.type == 'kagome':
                        if x==0:
                            charge = np.sum(local[0,:,3]) -np.sum(local[1,:,3])+np.sum(local[:,0,4]) -np.sum(local[:,2,4])
                        elif x==self.side_len_x-1:
                            charge = np.sum(local[:,:,3]) -np.sum(local[:,:,3])+np.sum(local[:,0,4]) -np.sum(local[:,2,4])
                        elif (x-2)%4:
                            if (y-2)%4:
                                charge = np.sum(local[0,:,3]) -np.sum(local[1,:,3])+np.sum(local[:,0,4]) -np.sum(local[:,2,4])
                            else:
                                charge = np.sum(local[1,:,3]) -np.sum(local[2,:,3])+np.sum(local[:,0,4]) -np.sum(local[:,2,4])
                        elif (x)%4:
                            if (y-2)%4:
                                charge = np.sum(local[1,:,3]) -np.sum(local[2,:,3])+np.sum(local[:,0,4]) -np.sum(local[:,2,4])
                            else:
                                charge = np.sum(local[0,:,3]) -np.sum(local[1,:,3])+np.sum(local[:,0,4]) -np.sum(local[:,2,4])
                        if charge>3:
                            charge = 1
                        elif charge<-3:
                            charge = -1
                        else:
                            charge = 0

                    grid[x,y, 8] = charge
                    #print(np.sum(np.multiply(local[:,:, 3:6]), np.array([[1,0],[0,-1]])))
                    #print(local)
                    
                    #local = grid[x-1:x+3,y-1:y+3,:]
                    #plt.quiver(grid[:,:,0].flatten(), grid[:,:,1].flatten(),grid[:,:,3].flatten(),grid[:,:,4].flatten(), angles='xy', scale_units='xy',  pivot = 'mid')
                    #plt.scatter(grid[:,:,0].flatten(), grid[:,:,0].flatten(), c = grid[:,:,8].flatten())
                    #plt.plot(grid[x,y,0],grid[x,y,1], 'o')
                    #plt.quiver(local[:,:,0].flatten(), local[:,:,1].flatten(),local[:,:,3].flatten(),local[:,:,4].flatten(), angles='xy', scale_units='xy',  pivot = 'mid')
                    #plt.show()
        self.lattice = grid
                    
    
    def graphCharge(self):
        '''
        Plots the positions and directions of the bar magnetisations as a quiver graph
        '''
        self.vertexCharge2()
        grid = self.lattice
        X = grid[:,:,0].flatten()
        Y = grid[:,:,1].flatten()
        z = grid[:,:,2].flatten()
        Mx = grid[:,:,3].flatten()
        My = grid[:,:,4].flatten()
        Mz = grid[:,:,5].flatten()
        Hc = grid[:,:,6].flatten()
        C = grid[:,:,7].flatten()
        MagCharge = grid[:,:,8].flatten()            
        fig = plt.figure(figsize=(6,6))
        ax = fig.add_subplot(111)
        ax.set_xlim([-1*self.unit_cell_len, np.max(X)+self.unit_cell_len])
        ax.set_ylim([-1*self.unit_cell_len, np.max(Y)+self.unit_cell_len])
        ax.set_title("Vertex Magnetic Charge Map",fontsize=14)
        #ax.set_xlabel("XAVG",fontsize=12)
        #ax.set_ylabel("YAVG",fontsize=12)
        #ax.grid(True,linestyle='-',color='0.75')
        ax.quiver(X, Y, Mx, My, angles='xy', scale_units='xy',  pivot = 'mid', zorder=1)
        # scatter with colormap mapping to z value
        ax.scatter(X,Y,s=80,c=MagCharge, marker = 'o', cmap = cm.seismic, zorder=2, edgecolor='k' )
        plt.show()
            


    
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
        grid[grid ==0]=0.
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
        self.vertexCharge2()
        grid = self.lattice
        #magcharge = grid[:,:,8].flatten()
        return(np.nanmean(np.absolute(grid[:,:,8])))

    def vertexEnergy(self):
        EnergyVertex = self.vertexType()
        EnergyVertex[EnergyVertex[:,:,4]==1] = 0.
        EnergyVertex[EnergyVertex[:,:,4]==2] = (2**0.5-1)/(2**0.5-0.5)
        EnergyVertex[EnergyVertex[:,:,4]==3] = 1.
        EnergyVertex[EnergyVertex[:,:,4]==4] = (4*2**0.5)/(2*2**0.5-1)
        print(np.nanmean(EnergyVertex))
        return(np.nanmean(EnergyVertex))
    
    def fieldTemperature(self, Hs, n=3, nangle=36):
        #Hs = (Beta - 9.12)/0.201
        Hc = self.Hc
        Hmax = (1.5*self.Hc+ 4.*self.Hc_std*self.Hc+Hs)
        Happlied = Hmax
        while np.absolute(Happlied) > (Hc-4.*self.Hc_std*self.Hc):
            for angle in 2*np.pi*np.random.random(nangle):
                print(angle, Happlied)
                H = Happlied*np.array([np.cos(angle), np.sin(angle), 0.])
                self.relax(H, n = n)
            Happlied = -np.sign(Happlied)*(np.absolute(Happlied)-Hs)

    def vertexType(self):
        '''
        Only works for square
        Classifies the vertices into Type 1,2,3,4
        '''
        grid = copy.deepcopy(self.lattice)
        Vertex = np.zeros((self.side_len_x, self.side_len_y, 5))
        Type1 = np.array([-1,1,1,-1])
        Type21 = np.array([-1,-1,1,1])
        Type22 = np.array([1,1,1,1])
        Type3 = np.array([1,1,1,-1])
        Type3 = np.array([1,-1,1,1])
        Type3 = np.array([-1,1,1,1])
        Type3 = np.array([1,1,-1,1])
        Type4 = np.array([1,-1,1,-1])
        for x in np.arange(0, self.side_len_x):
            for y in np.arange(0, self.side_len_y):
                Corr_local = []
                if np.isnan(grid[x,y,8])!=True:
                    x1 = x - 3
                    x2 = x + 4
                    y1 = y - 3
                    y2 = y + 4

                    if x1<0:
                        x1 = 0
                    if x2>self.side_len_x:
                        x2 = self.side_len_x
                    if y1<0:
                        y1 = 0
                    if y2>self.side_len_y:
                        y2 = self.side_len_y
                    local = grid[x1:x2,y1:y2]
                    spin_code0 = np.array([grid[x+1,y,3],grid[x-1,y,3],grid[x,y+1,4],grid[x,y-1,4]])
                    Vertex[x,y,0:4] = spin_code0
                    if np.array_equal(Vertex[x,y,0:4],Type1) or np.array_equal(Vertex[x,y,0:4],-1.*Type1):
                        Vertex[x,y,4] = 1

                    elif np.array_equal(Vertex[x,y,0:4],Type4) or np.array_equal(Vertex[x,y,0:4], -1.*Type4):
                        Vertex[x,y,4] = 4
                    elif np.array_equal(Vertex[x,y,0:4], Type21) or np.array_equal(Vertex[x,y,0:4], -1.*Type21) or np.array_equal(Vertex[x,y,0:4],Type22) or np.array_equal(Vertex[x,y,0:4],-1.*Type22):
                        Vertex[x,y,4] = 2
                    else:
                        Vertex[x,y,4] = 3
                else:
                    Vertex[x,y,:] = np.array([np.nan, np.nan, np.nan, np.nan, np.nan])
        return(Vertex)

    def vertexTypeMap(self):
        '''
        Only works with square
        '''
        Vertex= self.vertexType()
        X = self.lattice[:,:,0].flatten()
        Y = self.lattice[:,:,1].flatten()
        z = self.lattice[:,:,2].flatten()
        Mx = self.lattice[:,:,3].flatten()
        My = self.lattice[:,:,4].flatten()
        Mz = self.lattice[:,:,5].flatten()
        Hc = self.lattice[:,:,6].flatten()
        C = self.lattice[:,:,7].flatten()
        charge = self.lattice[:,:,8].flatten()
        Type = Vertex[:,:,4].flatten()
        fig = plt.figure(figsize=(6,6))
        ax = fig.add_subplot(111)
        ax.set_xlim([-1*self.unit_cell_len, np.max(X)+self.unit_cell_len])
        ax.set_ylim([-1*self.unit_cell_len, np.max(Y)+self.unit_cell_len])
        graph = ax.scatter(X,Y,c = Vertex[:,:,4], marker = 'o', cmap = cm.plasma, zorder=2)
        cb2 = fig.colorbar(graph, fraction=0.046, pad=0.04, ax = ax)
        cb2.locator = MaxNLocator(nbins = 5)
        cb2.update_ticks()
        ax.quiver(X,Y,Mx,My,angles='xy', scale_units='xy',  pivot = 'mid')
        plt.show()

    def vertexTypePercentage(self):
        '''
        Only works with square
        '''
        Vertex= self.vertexType()
        Type1 = np.nansum(Vertex[:,:,4]==1.)
        Type2 = np.nansum(Vertex[:,:,4]==2.)
        Type3 = np.nansum(Vertex[:,:,4]==3.)
        Type4 = np.nansum(Vertex[:,:,4]==4.)
        total = np.sum([Type1, Type2, Type3, Type4])
        print(total, Type1,Type2,Type3,Type4)
        vertices = {'Type1': Type1/total,'Type2': Type2/total,'Type3': Type3/total,'Type4': Type4/total}
        print(vertices)
        return(vertices)

    def localCorrelation(self):
        '''
        Only works for square Lattice
        '''
        grid = copy.deepcopy(self.lattice)
        Correlation = np.zeros((self.side_len_x, self.side_len_y, 1))
        for x in np.arange(0, self.side_len_x):
            for y in np.arange(0, self.side_len_y):
                Corr_local = []
                if np.isnan(grid[x,y,8])!=True:
                    x1 = x - 3
                    x2 = x + 4
                    y1 = y - 3
                    y2 = y + 4

                    if x1<0:
                        x1 = 0
                    if x2>self.side_len_x:
                        x2 = self.side_len_x
                    if y1<0:
                        y1 = 0
                    if y2>self.side_len_y:
                        y2 = self.side_len_y
                    local = grid[x1:x2,y1:y2]
                    spin_code0 = np.array([grid[x+1,y,3],grid[x-1,y,3],grid[x,y+1,4],grid[x,y-1,4]])

                    #print(np.sum(np.multiply(local[:,:, 3:6]), np.array([[1,0],[0,-1]])))
                    #print(local)
                    for i in np.arange(x1,x2):
                        for j in np.arange(y1,y2):
                            if np.isnan(grid[i,j,8])!=True:
                                spin_code = np.array([grid[i+1,j,3],grid[i-1,j,3],grid[i,j+1,4],grid[i,j-1,4]])
                                Corr_local.append(np.sum(np.equal(spin_code,spin_code0))/np.size(spin_code))
                    Corr = (np.sum(np.array(Corr_local))-1.)/(np.size(Corr_local)-1.)
                    Correlation[x,y,0] = Corr
                else:
                    Correlation[x,y,0] = np.nan
                    #local = grid[x-1:x+3,y-1:y+3,:]
                    #plt.quiver(grid[:,:,0].flatten(), grid[:,:,1].flatten(),grid[:,:,3].flatten(),grid[:,:,4].flatten(), angles='xy', scale_units='xy',  pivot = 'mid')
                    #plt.scatter(grid[:,:,0].flatten(), grid[:,:,0].flatten(), c = grid[:,:,8].flatten())
                    #plt.plot(grid[x,y,0],grid[x,y,1], 'o')
                    #plt.quiver(local[:,:,0].flatten(), local[:,:,1].flatten(),local[:,:,3].flatten(),local[:,:,4].flatten(), angles='xy', scale_units='xy',  pivot = 'mid')
                    #plt.show()
        X = grid[:,:,0].flatten()
        Y = grid[:,:,1].flatten()
        z = grid[:,:,2].flatten()
        Mx = grid[:,:,3].flatten()
        My = grid[:,:,4].flatten()
        Mz = grid[:,:,5].flatten()
        Hc = grid[:,:,6].flatten()
        C = grid[:,:,7].flatten()
        charge = grid[:,:,8].flatten()
        fig = plt.figure(figsize=(6,6))
        ax = fig.add_subplot(111)
        ax.set_xlim([-1*self.unit_cell_len, np.max(X)+self.unit_cell_len])
        ax.set_ylim([-1*self.unit_cell_len, np.max(Y)+self.unit_cell_len])
        graph = ax.scatter(X,Y,c = Correlation[:,:,0], marker = 'o', cmap = cm.plasma, zorder=2)
        cb2 = fig.colorbar(graph, fraction=0.046, pad=0.04, ax = ax)
        cb2.locator = MaxNLocator(nbins = 5)
        cb2.update_ticks()
        ax.quiver(X,Y,Mx,My,angles='xy', scale_units='xy',  pivot = 'mid')
        plt.show()
        return(Correlation)

    def correlationHistogram(self):
        Correlation = self.localCorrelation()
        Corr = Correlation[:,:,0].flatten()
        Corr = Corr[np.logical_not(np.isnan(Corr))]
        fig, axs = plt.subplots(1, 1, figsize=(5, 15),tight_layout=True)
        axs.hist(Corr, bins = 10, density = True, facecolor = 'g', alpha = 0.75)
        plt.show()

    def vertexHistogram(self):
        Vertex = self.vertexType()
        Type = Vertex[:,:,4].flatten()
        Type = Type[np.logical_not(np.isnan(Type))]
        fig, axs = plt.subplots(1, 1, figsize=(5, 15),tight_layout=True)
        axs.hist(Type, bins = 4, density = True, facecolor = 'g', alpha = 0.75)
        plt.show()

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