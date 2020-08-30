import tag_util
import basewindow
import pathDescriberWindow

"""
Okay,

1.  come up with paths, somehow.  I'm not going ot draw them.
  * drawing lots of them
  * using the list of key vertices

2.  build a gui that takes a list of paths, runs all
classifiers on all landmarks on them. 

3.  Lets the user correct the classifier - valid/invalid

4.  saves the results in editor window format. 

5.  each result should be associated with a map file, and the
landmark should be associated with the original polygon.


File format:
  * tag file name
  * name of the editorwindow file name is the id of the landmark? 
  * engineName.polygon.id

"""



def main():
    tagFile = tag_util.tag_file("../data/directions/direction_floor_3/log4_s3.tag", "../data/directions/direction_floor_3/log4_s3.cmf")
    
    polygons = tagFile.as_slimd_polygons()
    app = basewindow.makeApp()
    wnd = pathDescriberWindow.makeWindow(polygons, [[(43, 14), (40, 26)]])
    wnd.show()
    print len(polygons)
    retval = app.exec_()
if __name__=="__main__":
    main()
