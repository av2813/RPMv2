import numpy as np
import matplotlib.pyplot as plt


class Lattice():
    def __init__(self, unit_cells_x, unit_cells_y, bar_length = 1e-6, vertex_gap = 1e-7, Hc=0.03):
        self.lattice = None
        self.unit_cells_x = unit_cells_x
        self.unit_cells_y = unit_cells_y
        self.side_len_x = 2*unit_cells_x+1
        self.side_len_y = 2*unit_cells_y+1
        self.bar_length = bar_length
        self.vertex_gap = vertex_gap
        self.Hc = Hc
        
    def square(self):
        grid = np.zeros((2*self.unit_cells_x+1, 2*self.unit_cells_y+1, 5))        
        for x in range(0, 2*self.unit_cells_x+1):
            for y in range(0, 2*self.unit_cells_y+1):
                #print(x,y)
                if (x+y)%2 != 0:
                    if y%2 == 0:
                        grid[x,y] = np.array([x,y,1,0, np.random.normal(loc=self.Hc, scale=0.05*self.Hc, size=None)])
                    else:
                        grid[x,y] = np.array([x,y,0,1,np.random.normal(loc=self.Hc, scale=0.05*self.Hc, size=None)])
                else:
                    grid[x,y] = np.array([x,y,0,0,0])
        self.lattice = grid

    def kagome(self):
        grid = np.zeros((2*self.unit_cells_x+1, 4*self.unit_cells_y+1,5))
        for x in range(0, self.side_len_x):
            for y in range(0, self.side_len_y):
                if x%2!=0 and y%4==0:
                    if (x-1)%4==0:
                        grid[x,y] = np.array([x,y+2,1,0,np.random.normal(loc=self.Hc, scale=0.05*self.Hc, size=None)])
                    else:
                        grid[x,y] = np.array([x,y,1,0,np.random.normal(loc=self.Hc, scale=0.05*self.Hc, size=None)])
                if x%2 ==0 and (y-1)%4==0:
                    if x%4==0:
                        grid[x,y] = np.array([x,y,0.5,(3**0.5/2),np.random.normal(loc=self.Hc, scale=0.05*self.Hc, size=None)])
                    else:
                        grid[x,y] = np.array([x,y,-0.5,(3**0.5/2),np.random.normal(loc=self.Hc, scale=0.05*self.Hc, size=None)])
                if x%2 ==0 and (y-3)%4==0:
                    if x%4==0:
                        grid[x,y] = np.array([x,y,-0.5,(3**0.5/2),np.random.normal(loc=self.Hc, scale=0.05*self.Hc, size=None)])
                    else:
                        grid[x,y] = np.array([x,y,0.5,(3**0.5/2),np.random.normal(loc=self.Hc, scale=0.05*self.Hc, size=None)])

        self.lattice = grid


    def graph(self):
        grid = self.lattice
        X = grid[:,:,0].flatten()
        Y = grid[:,:,1].flatten()
        U = grid[:,:,2].flatten()
        V = grid[:,:,3].flatten()
        Z = grid[:,:,4].flatten()
        #X = np.array(X)-0.5
        #Y = np.array(Y)-0.5
        plt.figure('Lattice')
        ax = plt.gca()
        ax.quiver(X, Y, U, V, angles='xy', scale_units='xy', scale=1, pivot = 'mid')
        ax.set_xlim([-1, self.side_len_x])
        ax.set_ylim([-1, self.side_len_y])
        plt.draw()
        plt.show()


    def relax(self, Happlied = np.array([0.,0.])):
        grid = self.lattice
        unrelaxed = True
        while unrelaxed==True:
            flipcount = 0
            for x in range(0, self.side_len_x):
                for y in range(0, self.side_len_y):
                    if grid[x,y,2] == 1:
                        if abs(Happlied[1]+self.Hlocal2(x,y, n=10)[1])>grid[x,y,4]:
                            grid[x,y,2:4]=-1.*grid[x,y,2:4]
                            flipcount +=1
                    if grid[x,y,3] == 1:
                        if abs(Happlied[0]+self.Hlocal2(x,y, n=10)[0])>grid[x,y,4]:
                            grid[x,y,2:4]=-1.*grid[x,y,2:4]
                            flipcount +=1
            print(flipcount)
            if flipcount==0:
                unrelaxed = False
        self.lattice = grid
    	#while flipped:
    	#	for x in range(0, 2*self.unit_cells_x+1):
        #    	for y in range(0, 2*self.unit_cells_y+1):
              
    def dipole(self, m, r, r0):
        """Calculate a field in point r created by a dipole moment m located in r0.
        Spatial components are the outermost axis of r and returned B.
        """
        m = np.array(m)
        #print m
        r = np.array(r)
        #print r
        r0 = np.array(r0)
        #print r0
        m = 800e3*1e-7*10e-9*1e-6*m
        
        r = 1e-6*r
        r0 = 1e-6*r0
        
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
        #print(B)
        return(B)

    def Hlocal2(self, x,y,n =1):
        Hl = []
        x1 = x - 2*n
        x2 = x +2*n
        y1 = y-2*n
        y2 = y+2*n
        #print(x1<0)
        if x1<0:
            x1 = 0
        if x2>self.side_len_x:
            x2 = self.side_len_x -1
        if y1<0:
            y1 = 0
        if y2>self.side_len_y-1:
            y2 = self.side_len_y-1
        temp = self.lattice
        grid = np.array(self.lattice)[x1:x2+1,y1:y2+1,:]
        m = grid[:,:,2:4]
        m = m.reshape(-1, m.shape[-1])
        r = grid[:,:,0:2]
        r = r.reshape(-1, r.shape[-1])
        r0 = self.lattice[x,y,0:2]
        for pos, mag in zip(r, m):
            if np.linalg.norm(pos-r0)/(n+1)<=1.0 and np.array_equal(pos, r0)!=True:
                Hl.append(self.dipole(mag, r0, pos))
        return(sum(Hl))
        #print(np.array(grid))
     
    def Hlocal(self,x,y,n=1):
        grid = self.lattice
        Hl = self.dipole(grid[x+1][y+1][2:4], grid[x][y][0:2], grid[x+1][y+1][0:2])
        #print Hl
        #print grid[x+1][y+1][2:4], grid[x][y][0:2], grid[x+1][y+1][0:2]
        Hl += self.dipole(grid[x+1][y-1][2:4], grid[x][y][0:2], grid[x+1][y-1][0:2])
       # print Hl
        Hl += self.dipole(grid[x-1][y+1][2:4], grid[x][y][0:2], grid[x-1][y+1][0:2])
        Hl += self.dipole(grid[x-1][y-1][2:4], grid[x][y][0:2], grid[x-1][y-1][0:2])
        #print Hl
        if grid[x][y][2] == 0:
            Hl += self.dipole(grid[x][y+2][2:4], grid[x][y][0:2], grid[x][y+2][0:2])
            Hl += self.dipole(grid[x][y-2][2:4], grid[x][y][0:2], grid[x][y-2][0:2])
        else:
            Hl += self.dipole(grid[x+2][y][2:4], grid[x][y][0:2], grid[x+2][y][0:2])
            Hl += self.dipole(grid[x-2][y][2:4], grid[x][y][0:2], grid[x-2][y][0:2])
        return Hl


    def randomMag(self):
        grid = self.lattice
        for x in grid:
            for y in x:
                if np.random.rand()>0.5:
                    y[2:4]=-1.*y[2:4]
        self.lattice = grid

    def compare(self, Lattice1, Lattice2):
        total = 0
        same = 0
        for x in range(0, self.side_len_x):
            for y in range(0, self.side_len_y):
                if Lattice1[x,y,4]!=0:
                    if np.array_equal(Lattice1[x,y, 2:4], Lattice2[x,y,2:4]) ==True:
                        same+=1
                    total +=1
        print(same)
        print(total)
        return(same/total)

    def returnLattice(self):
        return self.lattice


                

test = Lattice(20,20)
test.square()
#grid= test.returnLattice()
#print grid
test.graph()

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

test.randomMag()
test.graph()
localfield = []
for num in np.arange(1, 20, 1):
    localfield.append(np.linalg.norm(test.Hlocal2(9,9, n = num)))
print(localfield)
fig2 = plt.figure(2)
ax2 = fig2.add_subplot(111)
ax2.plot(np.arange(1, 20, 1), localfield)
plt.title('Local field Calculation')
plt.ylabel(r'Local Field Strength (T)')
plt.xlabel(r'Number of Unit Cells')
beforerelax = test.returnLattice()
test.relax(Happlied = [-0.03,-0.03])
print('this graph')
test.graph()
after = test.returnLattice()
print(test.compare(after, beforerelax))

test2 =Lattice(20,20)
test2.kagome()
test2.graph()
#print(test.dipole(np.array([0,1]), np.array([1,1]),np.array([0,0])))

#print(test.Hlocal(3,2))