from sys import argv
from tag_util import *

if __name__=="__main__":
    if(len(argv) == 5):
        st = tag_file(argv[2], argv[1])
        pts, polygons = st.scale_annotations(argv[3])
        save_polygons(polygons, pts, argv[4])
    else:
        print "usage:\n\tpython copy_tagfile.py start_map, start_tag, end_map, end_tag"
    
        
