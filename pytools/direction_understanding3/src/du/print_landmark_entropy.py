import dir_util
import pylab as mpl
import numpy as na
import cPickle as pickle
def save_entropy():
    from sys import argv
    
    m4du = dir_util.load(argv[1])

    
    data = []
    print m4du.mynames
    for i, kw in enumerate(m4du.mynames):
        lmat = m4du.get_prob_landmark_given_sdc_modifiers({"landmarks":[kw]})
        print i, kw
        entropy = dir_util.entropy(lmat)
        print kw, entropy
        data.append((kw, entropy))

    data.sort(key=lambda x: x[-1])
    with open("entropy_d1.pck", "wb") as f:
        pickle.dump(data, f, protocol=2)

def main():
    plot(pickle.load(open("entropy_d1.pck")))
    #save_entropy()

def plot(data):
    words = set()
    new_data = []
    for kw, entropy in data:
        if not kw in words:
            words.add(kw)
            new_data.append((kw, entropy))
        
    data = new_data
    X = na.arange(len(data))
    Y = [data[i][1] for i in X]
    print "least sure", [data[i][0] for i in X[-10:]]
    print "most sure", [data[i][0] for i in X[0:10]]
    print Y[-1]
    mpl.plot(X, Y)
    mpl.xticks(X, [name for name, value in data])
    mpl.show()
                    

if __name__=="__main__":
    main()

