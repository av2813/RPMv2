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
        grid = np.zeros((2*self.unit_cells_x+1, 2*self.unit_cells_y+1))
        print(grid)
        grid = grid.tolist()
        for x in range(0, 2*self.unit_cells_x+1):
            for y in range(0, 2*self.unit_cells_y+1):
                #print(x,y)
                if (x+y)%2 != 0:
                    if y%2 == 0:
                        grid[x][y] = [x,y,1,0, np.random.normal(loc=self.Hc, scale=0.05*self.Hc, size=None)]
                        
                    else:
                        grid[x][y] = [x,y,0,1,np.random.normal(loc=self.Hc, scale=0.05*self.Hc, size=None)]
                else:
                    grid[x][y] = [x,y,0,0,0]
        self.lattice = grid
        
    def graph(self):
        grid = self.lattice
        grid = sum(grid, [])
        X, Y, U, V, Z = zip(*grid)
        #X = np.array(X)-0.5
        #Y = np.array(Y)-0.5
        plt.figure('Lattice')
        ax = plt.gca()
        ax.quiver(X, Y, U, V, angles='xy', scale_units='xy', scale=1, pivot = 'mid')
        ax.set_xlim([-1, self.side_len_x])
        ax.set_ylim([-1, self.side_len_y])
        plt.draw()
        plt.show()


    def relax(self):
    	grid = self.lattice()
    	while flipped:
    		for x in range(0, 2*self.unit_cells_x+1):
            	for y in range(0, 2*self.unit_cells_y+1):

                  
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
        print B
        return B
     
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
              
    def returnLattice(self):
        return self.lattice
                

test = Lattice(3,3)
test.square()
#grid= test.returnLattice()
#print grid
test.graph()

#print(test.dipole(np.array([0.0,1.0]), np.array([1.0,1.0]),np.array([0.0,0.0])))


#print(test.dipole(np.array([0,1]), np.array([1,1]),np.array([0,0])))

print(test.Hlocal(3,2))