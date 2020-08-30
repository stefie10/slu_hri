from logfile_util import *

if __name__=="__main__":
    if(len(argv) == 3):
        lf = logfile_du(argv[1], argv[2])
        
        print "number of images:", len(lf.timestamp_to_image.keys())
        print "number of readings:", len(lf.timestamp_to_fread)
        
        for i in range(1000):
            vals, types = lf.next_reading()
            print types
            if(types[0] == "image"):
                print lf.get_image(vals[0])
            
        print lf.get_readings([0,0])
    else:
        print "usage\n\tpython load_logfile.py log_fn image_dir"
