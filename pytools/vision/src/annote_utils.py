import re
from math import sqrt
from glob import glob
#from scipy import arange

class polygon:
    def __init__(self):
        self.X = []
        self.Y = []
        self.tag = None

    def add_segment(self, x, y):
        self.X.append(x)
        self.Y.append(y)
    def as_list_of_vertices(self):
        return [p for p in zip(self.X, self.Y)]
    def add_tag(self, str):
        #print "adding tag:", str
        self.tag = str

    def get_tag(self):
        return self.tag

    def is_finished(self):
        if(sqrt((self.X[-1]-self.X[0])**2.0+(self.Y[-1]-self.Y[0])**2.0) < 5):
            return True

    def num_segments(self):
        return len(self.X)
    
    def get_segment(self, i):
        return self.X[i], self.Y[i]

    def tostring(self):
        #print "tag", self.tag
        mystr = "";
        if(self.tag != None):
            mystr = "tag:"+self.tag 
        
        mystr += " polygon:"
        for i in range(len(self.X)):
            x, y = self.X[i], self.Y[i]
            mystr+= str(x) + "," + str(y)+":"
        mystr+="\n"
        return mystr

    def fromstring(self, mystr):
        tags = re.split("[ :]", mystr)
        doPoly=False
        for i in range(len(tags)):
            if(doPoly):
                #print "mystr", tags[i]
                vals = tags[i].split(",")
                if(len(vals) == 2):
                    v1, v2 = vals
                    v1 = float(v1)
                    v2 = float(v2)
                    self.add_segment(v1, v2)

            if(tags[i] == "tag"):
                i+=1
                self.add_tag(tags[i])
            elif(tags[i] == "polygon"):
                doPoly = True
        return doPoly

    def __cmp__(self, other):
        return cmp(self.tag, other.tag)

    def isempty(self):
        if(len(self.X) ==0):
            return True
        return False


class point:
    def __init__(self, x=None, y=None, tag=None):
        self.x = x
        self.y = y
        self.tag = tag

    def tostring(self):
        mystr = "";
        if(self.tag != None):
            mystr = "tag:"+self.tag 
        
        mystr += " point:"
        mystr+= str(self.x) + "," + str(self.y)+":"
        mystr+="\n"
        return mystr

    def fromstring(self, mystr):
        tags = re.split("[ :]", mystr)
        doPt=False
        for i in range(len(tags)):
            if(doPt):
                #print "mystr", tags[i]
                vals = tags[i].split(",")
                if(len(vals) == 2):
                    v1, v2 = vals
                    self.x = float(v1)
                    self.y = float(v2)
            if(tags[i] == "tag"):
                i+=1
                self.tag = tags[i]
            elif(tags[i] == "point"):
                doPt = True

        return doPt

    def __cmp__(self, other):
        return cmp(self.tag, other.tag)

    def isempty(self):
        if(self.x == None or self.y == None or self.tag == None):
            return True
        return False
    

def save_polygons(polygons, points, filename):
    myfile = open(filename, 'w')
    for pol in polygons:
        if(not pol.isempty()):
            #print pol.tostring()
            myfile.write(pol.tostring())

    for p in points:
        if(not p.isempty()):
            #print p.tostring()
            myfile.write(p.tostring())

    myfile.close()

def load_polygons(filename):
    myfile = open(filename, 'r')
    polygons = []
    pts = []
    for line in myfile:
        p = polygon()
        pt = point()        

        if(p.fromstring(line)):
            polygons.append(p)
        elif(pt.fromstring(line)):
            pts.append(pt)
            
    
    myfile.close()
    return polygons, pts




def load_classifiers(directory):
    myfilenames = glob(directory+"*dataset*.txt");
    
    #todo... fix label problem
    mylabelfile = open(directory+"labels.txt")
    
    objecthash = {}

    for line in mylabelfile:
        
        if(line[0] == "#"):
            print "continuing"
            continue

        line = line.strip()
        filename = line.split(" ")[0]

        if(len(line.split(" ")) >= 2):
            image_num = int(filename.split(".")[0])
            stuff = line.split(" ")[1:]
            #associate the image number to the stuff
            objecthash[image_num] = stuff

    results = {}
    class_name = ""
    
    for filename in myfilenames:
        
        myfile = open(filename, 'r');
        
        spl_file = filename.split("/")[-1];
        class_name = spl_file.split("_")[0]
        results[class_name] = []
        
        for line in myfile:
            line = line.strip()
            spl = line.split(" ")
            
            if(len(spl) == 2):
                myclass = spl[1]
                results[class_name].append(int(myclass))

            
    if(class_name == ""):
        return None

    return objecthash, results


if __name__=="__main__":
    true_hash, results = load_classifiers("/home/tkollar/local2/data/vision/log3_s3/classifier/")
    
    print true_hash.keys()
    mykeys = true_hash.keys()
    mykeys.sort()
    print mykeys

