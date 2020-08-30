import pylab as mpl
import numpy as na

def main():
    d1_data = na.array([(0, 0.53), (2, .60667), (3, .60667), (4, .61333), (8.98526419128, 0.60)])

    d8_data = na.array([(0, 0.55), (2, 0.72), (3, .70667), (4, 0.68667), (7.691467390779, 0.69333)])

    X1 ,Y1 = d1_data.transpose()
    mpl.plot(X1, Y1, label="d1")

    X8, Y8 = d8_data.transpose()
    mpl.plot(X8, Y8, label="d8")
    mpl.legend(loc="lower right")
    mpl.xlabel("Use spatial relations if landmark entropy less than X")
    mpl.ylabel("% correct")
    mpl.title("Performance when using spatial relations based on entropy")
    mpl.show()
    
    

    

if __name__=="__main__":
    main()

