import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as cl
#from matplotlib.colors import Normalize
import copy



class ASI_RPM():
    def __init__(self, unit_cells_x, unit_cells_y, lattice = None, bar_length = 220e-9, vertex_gap = 1e-8, bar_thickness = 25e-9, bar_width = 80e-9, magnetisation = 800e3):
        self.lattice = lattice
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

    def save(self, file):
        '''
        Save existing arrays
        To Do
        '''

    def load(self, file):
        '''
        load in existing arrays
        To Do
        '''
        
    def square(self, Hc_mean = 0.03, Hc_std = 0.05*0.03):
        '''
        Defines the lattice positions, magnetisation directions and coercive fields of an array of 
        square ASI
        Takes the unit cell from the initial defined parameters
        Generates a normally distributed range of coercive fields of the bars using Hc_mean and Hc_std
        One thing to potentially change is to have the positions in nanometers
        '''
        self.side_len_x = 2*self.unit_cells_x+1
        self.side_len_y = 2*self.unit_cells_y+1
        grid = np.zeros((2*self.unit_cells_x+1, 2*self.unit_cells_y+1, 6))        
        for x in range(0, 2*self.unit_cells_x+1):
            for y in range(0, 2*self.unit_cells_y+1):
                if (x+y)%2 != 0:
                    if y%2 == 0:
                        grid[x,y] = np.array([x,y,1,0, np.random.normal(loc=Hc_mean, scale=Hc_std, size=None),0])
                    else:
                        grid[x,y] = np.array([x,y,0,1,np.random.normal(loc=Hc_mean, scale=Hc_std, size=None),0])
        self.lattice = grid

    def kagome(self, Hc_mean = 0.03, Hc_std = 0.05*0.03):
        '''
        Creates an array of Kagome ASI
        Takes the unit cell from the initial defined parameters
        Generates a normally distributed range of coercive fields of the bars using Hc_mean and Hc_std
        '''
        self.side_len_x = 2*self.unit_cells_x+1
        self.side_len_y = 4*self.unit_cells_y+1
        grid = np.zeros((2*self.unit_cells_x+1, 4*self.unit_cells_y+1,6))
        for x in range(0, self.side_len_x):
            for y in range(0, self.side_len_y):
                if x%2!=0 and y%4==0:
                    if (x-1)%4==0:
                        grid[x,y] = np.array([x,y+2,1,0,np.random.normal(loc=Hc_mean, scale=Hc_std, size=None),0])
                    else:
                        grid[x,y] = np.array([x,y,1,0,np.random.normal(loc=Hc_mean, scale=Hc_std, size=None),0])
                if x%2 ==0 and (y-1)%4==0:
                    if x%4==0:
                        grid[x,y] = np.array([x,y,0.5,(3**0.5/2),np.random.normal(loc=Hc_mean, scale=Hc_std, size=None),0])
                    else:
                        grid[x,y] = np.array([x,y,-0.5,(3**0.5/2),np.random.normal(loc=Hc_mean, scale=Hc_std, size=None),0])
                if x%2 ==0 and (y-3)%4==0:
                    if x%4==0:
                        grid[x,y] = np.array([x,y,-0.5,(3**0.5/2),np.random.normal(loc=Hc_mean, scale=Hc_std, size=None),0])
                    else:
                        grid[x,y] = np.array([x,y,0.5,(3**0.5/2),np.random.normal(loc=Hc_mean, scale=Hc_std, size=None),0])
        self.lattice = grid


    def graph(self):
        '''
        Plots the positions and directions of the bar magnetisations as a quiver graph
        '''
        grid = self.lattice
        X = grid[:,:,0].flatten()
        Y = grid[:,:,1].flatten()
        Mx = grid[:,:,2].flatten()
        My = grid[:,:,3].flatten()
        Hc = grid[:,:,4].flatten()
        C = grid[:,:,5].flatten()
        norm = cl.Normalize()
        norm.autoscale(C)
        Hc = (Hc-np.mean(Hc))/(max(Hc)-min(Hc))
        
        
        fig =plt.figure()
        ax = plt.gca()
        graph = ax.quiver(X, Y, Mx, My, C, linewidth = Hc, angles='xy', scale_units='xy', scale=1, pivot = 'mid')
        ax.set_xlim([-1, self.side_len_x])
        ax.set_ylim([-1, self.side_len_y])
        plt.colorbar(graph)
        plt.set_cmap(cm.jet)
        plt.draw()
        plt.show()

    def resetCount(self):
        '''
        Resets the count parameter in the lattice
        '''
        for x in range(0, self.side_len_x):
            for y in range(0, self.side_len_y):
                self.lattice[x,y,5] = 0

    def graphCount(self):
        '''
        To do
        '''


    def subtractCount(self, lattice1, lattice2):
        '''
        Haven't actually tested yet.
        Should take two instances of the ASI_RPM class and then return the difference between the number of spins flipped
        
        '''
        l1 = lattice1.returnLattice()
        l2 = lattice2.returnLattice()
        diff = l2[:,:,5] - l1[:,:,5]
        return(self(self.unit_cells_x, self.unit_cells_y,lattice = diff))

    def relax(self, Happlied = np.array([0.,0.]), n=10):
        '''
        Steps through all the 
        '''
        print("relax thinks Happ is =", Happlied)
        grid = copy.deepcopy(self.lattice)
        #print grid
        unrelaxed = True
        while unrelaxed==True:
            flipcount = 0
            for x in range(0, self.side_len_x):
                for y in range(0, self.side_len_y):
                    if abs(grid[x,y,4]) != 0:
                        unit_vector = grid[x,y,2:4]/np.linalg.norm(grid[x,y,2:4])
                        field = np.dot(np.array(Happlied+self.Hlocal2(x,y, n=n)), unit_vector)
                        if field < -grid[x,y,4]:
                            grid[x,y,2:4]=np.negative(grid[x,y,2:4])
                            grid[x,y,5]+=1
                            flipcount +=1
                    #     if (Happlied[0]+self.Hlocal2(x,y, n=n)[0])>grid[x,y,2]*grid[x,y,4]:
                    #         print('local field and coercive field = ',np.absolute(Happlied[0]+self.Hlocal2(x,y, n=n)[0]), grid[x,y,4])
                    #         grid[x,y,2:4]=np.negative(grid[x,y,2:4])
                    #         flipcount +=1
                    # if abs(grid[x,y,3]) == 1:
                    #     if np.absolute(Happlied[1]+self.Hlocal2(x,y, n=n)[1])>grid[x,y,4]:
                    #         print('local field and coercive field = ',np.absolute(Happlied[0]+self.Hlocal2(x,y, n=n)[0]), grid[x,y,4])
                    #         grid[x,y,2:4]=np.negative(grid[x,y,2:4])
                    #         flipcount +=1
            print("no of flipped spins in relax", flipcount)
            if flipcount==0:
                unrelaxed = False
        self.lattice = grid
        
    def fieldsweep(self, Hmax, steps, Htheta, n=10, loops=1):
        #Hmax = np.mean(self.lattice[:,:,4].flatten())*Hmax
        M0 = copy.deepcopy(self)
        self.graph()
        Htheta = np.pi*Htheta/180
        q = []
        q_test = []
        #steps = Hmax/Hdelta
        #Hmax = [Hmax*np.cos(Htheta),Hmax*np.sin(Htheta)]
        print ("Hmax = ",Hmax)
        #Hdelta =np.array([Hdelta*np.cos(Htheta),Hdelta*np.sin(Htheta)])
        #Hx_list = np.linspace(0, Hmax[0], Hmax[0]/Hdelta[0])
        #Hy_list = np.linspace(0, Hmax[1], Hmax[1]/Hdelta[1])
        #print ("deltaH = ",Hdelta)
        for i in range(0, loops):
            print ("i = ",i)
            for j in np.linspace(-Hmax,Hmax,steps):
                print ("j = ", j)
                Happlied = j*np.array([np.cos(Htheta),np.sin(Htheta)])
                print('Happlied: ', Happlied)
                self.relax(Happlied,n)
                #self.relax([Hx, Hy],n)
            q_test.append(self.correlation(M0,self))
            self.graph()
            q.append(self.correlation(M0,self))
            print ("q =",q)
            #self.graph()
        return q, q_test
    
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
        
        r = (self.vertex_gap+self.bar_length/2)*r
        r0 = (self.vertex_gap+self.bar_length/2)*r0
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
        m = grid[:,:,2:4]
        m = m.reshape(-1, m.shape[-1])
        r = grid[:,:,0:2]
        r = r.reshape(-1, r.shape[-1])
        r0 = self.lattice[x,y,0:2]

        for pos, mag in zip(r, m):
            if np.linalg.norm(pos-r0)/(n+1)<=1.0 and np.array_equal(pos, r0)!=True:
                Hl.append(self.dipole(mag, r0, pos))
        return(sum(Hl))
     
    def Hlocal(self,x,y,n=1):
        grid = self.lattice
        Hl = self.dipole(grid[x+1][y+1][2:4], grid[x][y][0:2], grid[x+1][y+1][0:2])
        Hl += self.dipole(grid[x+1][y-1][2:4], grid[x][y][0:2], grid[x+1][y-1][0:2])
        Hl += self.dipole(grid[x-1][y+1][2:4], grid[x][y][0:2], grid[x-1][y+1][0:2])
        Hl += self.dipole(grid[x-1][y-1][2:4], grid[x][y][0:2], grid[x-1][y-1][0:2])
        if grid[x][y][2] == 0:
            Hl += self.dipole(grid[x][y+2][2:4], grid[x][y][0:2], grid[x][y+2][0:2])
            Hl += self.dipole(grid[x][y-2][2:4], grid[x][y][0:2], grid[x][y-2][0:2])
        else:
            Hl += self.dipole(grid[x+2][y][2:4], grid[x][y][0:2], grid[x+2][y][0:2])
            Hl += self.dipole(grid[x-2][y][2:4], grid[x][y][0:2], grid[x-2][y][0:2])
        return Hl


    def randomMag(self, seed = None):
        State = np.random.RandomState(seed=seed)
        grid = self.lattice
        for x in grid:
            for y in x:
                if State.uniform(low=0.0, high=1.0)>0.5:
                    y[2:4]=-1.*y[2:4]
        self.lattice = grid

    def correlation(self, lattice1, lattice2):
        l1 = lattice1.returnLattice()
        l2 = lattice2.returnLattice()
        total = 0
        same = 0
        for x in range(0, self.side_len_x):
            for y in range(0, self.side_len_y):
                if l1[x,y,4]!=0:
                    if np.array_equal(l1[x,y, 2:4], l2[x,y,2:4]) ==True:
                        same+=1.0
                        #print("same running total",same)
                    total +=1.0
                    #print("total running total",total)
        print("same total",same)
        print("absolute total", total)
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

    def returnLattice(self):
        return self.lattice

    def switchBar(self, x,y):
        self.lattice[x,y, 2:4] *= -1

    def changeBarlen(self, newbar_length):
        self.bar_length = newbar_length

    def changeVertexgap(self, newvertex_gap):
        self.vertex_gap = newvertex_gap

    def changeMagnetisation(self, new_magnetisation):
        self.magnetisation = new_magnetisation






#testing code
                

test = ASI_RPM(15,15)
test.square()
test2 = ASI_RPM(10,10)
test2.kagome()
#grid= test.returnLattice()
#print grid
"""
test.graph()
"""
"""
#print(test.dipole(np.array([0.0,1.0]), np.array([1.0,1.0]),np.array([0.0,0.0])))
localfield = []
for num in np.arange(1, 20, 1):
    localfield.append(np.linalg.norm(test.Hlocal2(9,9, n = num)))
print(localfield)
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(np.arange(1, 20, 1), localfield)
plt.title('Local field Calculation')
plt.ylabel(r'Local Field Strength (T)')
plt.xlabel(r'Number of Unit Cells')
print()
"""

#test.randomMag()
#test.graph()
#localfield = []
#for num in np.arange(1, 20, 1):
#    localfield.append(np.linalg.norm(test.Hlocal2(9,9, n = num)))
#print(localfield)
#fig2 = plt.figure(2)
#ax2 = fig2.add_subplot(111)
#ax2.plot(np.arange(1, 20, 1), localfield)
#plt.title('Local field Calculation')
#plt.ylabel(r'Local Field Strength (T)')
#plt.xlabel(r'Number of Unit Cells')
#beforerelax = copy.deepcopy(test)
#beforerelax.graph()
#test.relax(Happlied = [-0.03,-0.03])
#print('test',test)
#after = copy.deepcopy(test)
#after.graph()
#print("before relax", beforerelax.returnLattice())
#print("after relax", after.returnLattice())
#beforerelax.graph()
#after.graph()
test.randomMag()

plt.show()
#print(test.correlation(after.returnLattice(), beforerelax.returnLattice()))
#print(test.correlation(after, beforerelax))

#test2 =Lattice(20,20)
#test2.kagome()
#test2.graph()
#print(test.dipole(np.array([0,1]), np.array([1,1]),np.array([0,0])))

#print(test.Hlocal(3,2))
#test.changeMagnetisation(800e7)
q,q_test = test.fieldsweep(0.0297/np.cos(np.pi/4),5,45, n = 5, loops = 3)
fig_q = plt.figure()
ax2 = fig_q.add_subplot(111)
ax2.plot(np.arange(0, len(q_test), 1), q_test,'o')
plt.title('Correlation Function')
plt.ylabel(r'Correlation')
plt.xlabel(r'Number of loops')
plt.show()

#test.relax(Happlied = [0.03,0.03])
#test.graph()