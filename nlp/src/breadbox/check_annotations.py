from environ_vars import TKLIB_HOME
import glob
import annotation_reader



def main():
    
    for f in glob.glob("%s/data/directions/breadbox/nouns_*.txt" % TKLIB_HOME):
        print "checking", f
        annotations = annotation_reader.from_file(f)
        print "got", len(annotations.words), "annotations"
    
    

    
if __name__ == "__main__":
    main()
