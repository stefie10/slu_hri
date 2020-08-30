#!/usr/bin/python
import os
import sys
import math
import array
import cPickle

import lcm
from bot.lcmgl import *


def draw_poses_from_model(model):
    tmap_locations = model.tmap_locs_3d
    tmap = model.tmap
    
    X, Y = [], []
    gl = lcmgl('pose', lcm.LCM())
    # draw path
    gl.glEnable(GL_DEPTH_TEST)
    gl.glPushMatrix()
    gl.glTranslated(0, 0, -0.01)
    #gl.glBegin(GL_LINE_STRIP)

    
    dirs = []
    #tmap, tmap_nc, tmap_locations = model.clusters.get_topological_map()
    
    gl.glLineWidth(2)
    #plot the connections
    for p_from in tmap.keys():
        #gl.glColor3f(0.5-(1-z)*0.5, 0, 0.5-((1/4.0)*z)*0.5)

        
        gl.glBegin(GL_LINES)

        for p_to in tmap[p_from]:
            x1, y1, z1 = tmap_locations[p_from]
            x2, y2, z2 = tmap_locations[p_to]

            if(z1 == z2 and z1 < 2.0):
                gl.glColor3f(0.9, 0, 0)
            elif(z1 == z2 and z1 >= 2.0):
                gl.glColor3f(0, 0, 0.9)
            else:
                gl.glColor3f(0.4, 0.4, 0.4)

            gl.glVertex3d(x1, y1, z1)
            gl.glVertex3d(x2, y2, z2)

        gl.glEnd()


    for p_key in tmap_locations.keys():
        print "location:", tmap_locations[p_key]
        x,y,z = tmap_locations[p_key]        
        gl.glEnable(GL_LIGHTING)
        #gl.glMaterialf(GL_FRONT, GL_AMBIENT, 0.25, 0.25, 0.25, 1);
        #gl.glMaterialf(GL_FRONT, GL_DIFFUSE, 0.25, 0.25, 0.25, 1);

        if(z < 2.0):
            gl.glMaterialf(GL_FRONT, GL_AMBIENT, 0.9, 0, 0, 1);
            gl.glMaterialf(GL_FRONT, GL_DIFFUSE, 0.9, 0, 0, 1);

        elif(z >= 2.0):
            gl.glMaterialf(GL_FRONT, GL_AMBIENT, 0, 0, 0.9, 1);
            gl.glMaterialf(GL_FRONT, GL_DIFFUSE, 0, 0, 0.9, 1);

        #gl.glColor3f(0, 0.5, 0)
        gl.sphere(x, y, z, 0.5, 10, 10)
    
    
        
    gl.glPopMatrix()
    gl.glDisable(GL_DEPTH_TEST)
    gl.switch_buffer()


if __name__ == "__main__":
    args = sys.argv[1]

    def usage():
        print "usage:  %s [options] <model>" % sys.argv[0]
        sys.exit(1)

    if len(args) < 1:
        usage()

    model = cPickle.load(open(sys.argv[1], 'r'))
    draw_poses_from_model(model)
