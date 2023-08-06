import numpy as np
from simplex import LP
from visualize import simplex_visual
from style import polygon

# 2d choose basis
def test_2_1():
    A = np.array([[1,0], [1, 2]])
    b = np.array([[2],[4]])
    c = np.array([[1],[1]])
    lp = LP(A,b,c)
    simplex_visual(lp).show()
    #simplex_visual(lp,iter_lim=2,init_sol=np.array([[0],[0]]),rule='manual_select').show()

# 2d
def test_2_2():
    A = np.array([[2,1], [1, 1],[1,0],[1.5,1]])
    b = np.array([[10],[8],[4],[9]])
    c = np.array([[1],[1]])
    lp = LP(A,b,c)
    simplex_visual(lp).show()

# 2d "Sam Handout"
def test_2_3():
    A = np.array([[4,1], [1, 3],[3, 2]])
    b = np.array([[24],[24],[23]])
    c = np.array([[13],[5]])
    lp = LP(A,b,c)
    simplex_visual(lp).show()

# 3d Sam Ex
def test_3_1():
    A = np.array([[3,2,5],[2,1,1],[1,1,3],[5,2,4],[1,0,0]])
    b = np.array([[55],[26],[30],[57],[10]])
    c = np.array([[20],[10],[15]])
    lp = LP(A,b,c)
    simplex_visual(lp).show()

# 3d My Ex
def test_3_2():
    A = np.array([[1,1,1],[1,0,0],[0,1,0],[0,0,1],[1,0,1],[0,1,1],[3,3,1],[1,2,1]])
    b = np.array([[30],[15],[15],[15],[25],[25],[70],[45]])
    c = np.array([[1],[2],[1]])
    lp = LP(A,b,c)
    simplex_visual(lp,initial_solution=np.array([[5],[10],[15]])).show()

# 3d Klee-Minty Cube
def test_3_3():
    A = np.array([[1,0,0],[4,1,0],[8,4,1]])
    b = np.array([[5],[25],[125]])
    c = np.array([[4],[2],[1]])
    lp = LP(A,b,c)
    simplex_visual(lp,rule='dantzig').show()

def test_all():
    test_2_1()
    test_2_2()
    test_2_3()
    test_3_1()
    test_3_2()
    test_3_3()

#test_2_1()
#test_2_3()
#test_3_1()
test_3_2()
#test_3_3()
#test_all()

