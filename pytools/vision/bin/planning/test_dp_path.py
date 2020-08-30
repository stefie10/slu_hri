from scipy import *
from find_dp_path import *

def test_dp_path():
    lmap = zeros([10,10])*1.0
    lmap[:,0]= ones(10)*1.0
    lmap[0,:]= ones(10)*1.0

    
    pd = path_finding_dp(lmap, steps=30, im=0, jm=0)
    dp_map, X, Y = pd.compute_optimal_path()
    
    title("search for exit")
    gray()
    #imshow(likelihood_map, origin=1)
    dp_map = transpose(dp_map)
    imshow(dp_map, origin=1)
    plot([pd.im],[pd.jm], 'ro');
    plot(X, Y)
    show()



if __name__ == "__main__":
    test_dp_path()
