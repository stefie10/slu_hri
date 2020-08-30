from scipy import *
from scipy.linalg import svd
from sys import exit
import cPickle
from pyTklib import kNN_index
import tables

class pca_database:
    def __init__(self, pca_filename=None):
        self.filenames = []
        self.images = []
        self.pca_filename = pca_filename
        self.pca = None

    def save(self, filename):
        myh5file = tables.openFile(filename+".hd5",
                                   mode = "w", 
                                   title = "Flickr Database")
        
        root = myh5file.createGroup(myh5file.root, "Flickr", "Flickr 700k")
        myh5file.createArray(root, 'data', self.images, "Flickr 700k")
        myh5file.createArray(root, 'filenames', array(self.filenames), "Flickr 700k")
        myh5file.createArray(root, 'pca_filename', self.pca_filename, "Flickr 700k")
        #myh5file.createArray(root, 'pca', self.pca, "Flickr 700k")
        myh5file.close()
        
    def load(self, filename):
        h5file = tables.openFile(filename, 'r')
        dataObj = h5file.getNode('/Flickr', 'data')
        filenameObj = h5file.getNode('/Flickr', 'filenames')
        pcaObj = h5file.getNode('/Flickr', 'pca_filename')
        
        self.pca_filename = pcaObj.read()
        self.images = dataObj.read()
        self.filenames = filenameObj.read()
        

    def add_images(self, filenames, images):
        self.filenames = filenames
        self.images = images

    def get_pca(self):
        if(self.pca == None):
            self.pca = cPickle.load(open(self.pca_filename, 'r'))
        return self.pca

    def knn(self, image, k):
        print "loading pca"
        mypca = self.get_pca()
        print "flatten"
        flat_im = image.flatten()
        encIm = mypca.encode(transpose([flat_im]))
        
        print "kNN"
        I = kNN_index(encIm[:,0], self.images, k);
        return array(self.filenames).take(I)


class principal_components:
    def __init__(self, order, X=None, C=None, mean=None):
        if((X==None and C==None and mean==None) or (X==None and (C==None or mean==None))):
            print "cannot perform SVD with neither data nor covariance matrix"
            exit(0)
        
        self.mean = mean
        self.C = C

        if(self.C != None):
            self.evecs = self.pcaC(self.C)
        else:
            self.evecs = self.pca(X)
        
        self.order = order

    def pcaC(self, C):
        print "getting svd"
        #subtract the mean
        U, s, Vt = svd(C)
        #print "eigenvalues", s
        return U

    def encode(self, X):
        return dot(transpose(self.evecs[:,0:self.order]), X-transpose([self.mean]))

    def decode(self, A):
        return dot(self.evecs[:,0:self.order], A)+transpose([self.mean])
    
    def pca(self, X):
        print "get mean"
        #subtract the mean
        self.mean = sum(X,1)/(1.0*len(X[1]))

        print "computing covariance"
        Xpr = X - transpose([self.mean])
        Xpr = dot(Xpr, transpose(Xpr))

        print "running svd"
        U, s, Vt = svd(Xpr)
        return U


if __name__=="__main__":

    X = array([[1,2,3,9],
               [3,4,5,10],
               [5,4,3,5],
               [3,2,1,1]])
              
    pc = principal_components(1, X)
    print "*****************"
    print "encoding-->\n", pc.encode(X)
    print "*****************"
    print "decoding-->\n", pc.decode(pc.encode(X))
    print "mean", pc.mean
    print "evecs", pc.evecs
    
    
    

    

    
