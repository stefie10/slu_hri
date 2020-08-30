from pyTklib import *
from scipy import array

def kmeans_test():
    index = select_initial_cluster(array([[35.0], [24]]),array([[35], [24]]));
    
    print index

    

if __name__=="__main__":
    kmeans_test()
