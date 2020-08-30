from classifier_util import *
from sys import argv
from glob import glob
import cPickle

def evaluate_model(gtruth_filename, dirname, logfile, model):
    mygtruth = associate_classifications(gtruth_filename, dirname, logfile)
    
    outfile = open("class_file", 'w')
    for elt in model.likelihood_map.keys():

        for i in range(len(model.likelihood_map[elt])):
            
            outfile.write("loc " + str(i) + " type " + elt + " prob " + str(model.likelihood_map[elt][i]) + " gtruth ")
            
            if(elt in mygtruth[i]):
                outfile.write(" 1 ")
            else:
                outfile.write(" 0 ")
                
            for mygt in mygtruth[i]:
                outfile.write(mygt + " ")

            outfile.write("\n")
    
    outfile.close()

def load_timestamps(dirname):
    ts_filenames = glob(dirname + "/*.txt")
    ts_filenames.sort()
    
    print "loading timestamps"
    image_timestamps = {}
    for fn in ts_filenames:
        fh = open(fn, 'r')
        ts_str = fh.readline().split(':')[1]
        ts = float(ts_str)
        imnum = int(fn.split("/")[-1].split(".")[0])
        image_timestamps[
imnum] = ts
        fh.close()

    return image_timestamps

        
def associate_classifications(gtruth_filename, dirname, logfile):
    #load the image timestamps
    image_timestamps = load_timestamps(dirname)
    gtruth_full = load_groundtruth(gtruth_filename)
    
    #create a detections list that indexes over path_pts_unique
    mygtruth = []
    for i in range(len(logfile.path_pts_unique[0])):
        mygtruth.append([])
    
    #associate the flaser data with the image data
    fread_i = 0
        
    #sort the classifications by their number
    mykeys = gtruth_full.keys()
    mykeys.sort()
    
    #iterate through all of the image numbers in the classificaitons
    for imnum in mykeys:
        im_ts = image_timestamps[imnum]
        
        if(fread_i >= len(logfile.flaser)):
            break
        
        while(im_ts/1000000.0 > logfile.flaser[fread_i].timestamp):
            fread_i += 1
            if(fread_i >= len(logfile.flaser)):
                break
            
        if(fread_i <= 0):
            continue;
            
        #myloc = self.flaser[fread_i-1].location.x, self.flaser[fread_i].location.y
        j = logfile.path_pts_unique_index[fread_i-1]
        print "fread_i", fread_i, " gridcell:", j

        mygtruth[j].extend(gtruth_full[imnum])
        
        #detections_pts_unique[j].extend(myclassifications[imnum])

    return mygtruth
    
if __name__=="__main__":
    if(len(argv) == 5):
        evaluate_model(argv[1], argv[2], cPickle.load(open(argv[3], 'r')), cPickle.load(open(argv[4], 'r')))        
    else:
        print "usage:\n\tpython evaluate_model.py gtruth_filename, im_dirname, logfile_filename model"

    
