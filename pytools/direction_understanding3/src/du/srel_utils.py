from scipy import *
import os
import numpy as na
import sys
import logging
import time
import math2d
exWindow = 20.0
#import threading
import multiprocessing
from  multiprocessing import Process
import traceback

handler = logging.StreamHandler(sys.stdout)

def worker(input, output):
    for i in range(200):
        job = input.get()
        if job == "DONE":
            return
        else:
            desc, func, args = job
            #print "Running test", desc
            try:
                result = func(*args)
                output.put(result)
            except:
                stackTrace = traceback.format_exc()
                output.put({"exception":stackTrace})
                raise

        input.task_done()
        
        

class ProcessPool:
    def __init__(self, jobs, numberOfProcesses=multiprocessing.cpu_count()):
        self.taskQueue = multiprocessing.JoinableQueue()
        self.doneQueue = multiprocessing.Queue()
        # count job size so it's accurate in the case where we break for debugging.
        self.jobSize = 0 
        for i, job in enumerate(jobs):
            self.taskQueue.put(job)
            self.jobSize += 1 
#            if i > 10:
#                break
        for i in range(numberOfProcesses):
            self.taskQueue.put("DONE")
        #self.taskQueue.close()
        self.processes = [self.make_process() for i in range(numberOfProcesses)]

    def make_process(self):
        return Process(target=worker, args=(self.taskQueue, 
                                            self.doneQueue))         
    def restart(self):
        for i, p in enumerate(self.processes):
            if not p.is_alive():
                self.processes[i] = self.make_process()
                self.processes[i].start()
        
    def start(self):
        for p in self.processes:
            p.start()
    
    def is_alive(self):
        for p in self.processes:
            if p.is_alive():
                return True
        return False
    def terminate(self):
        for p in self.processes:
            p.terminate()

def createFigure(clusters, sloc, eloc):
    XY = clusters.skel.compute_path(sloc, eloc)
    if len(XY) <= 1 or len(XY[0])<= 1:
        return None

    figure = transpose(XY)
    if len(figure) >= 100:
        figure = math2d.subSample(figure, 100)
    #figure = math2d.stepAlongLine(figure, 100)

    figure = figure.tolist()
    if len(figure) <= 1:
        return None
    else:
        return figure

def srel_mat_expected_shape(sr_class, tmap, obj_locations):
    return [len(sr_class.engineMap), 
            len(tmap), 
            len(tmap),
            len(obj_locations[0])]

def get_srel_given_lmark_vpts_matrix(m4du):
    functions = pack_get_srel_given_lmark_vpts_matrix(m4du)

    print "loaded", len(functions), "jobs."
    numcores = os.sysconf('SC_NPROCESSORS_ONLN')
    pool = ProcessPool(functions, numcores)
    totalExamples = pool.jobSize
    print "starting", pool.jobSize, "threads."
    #pool.threads[0].run()
    pool.start()
    startTime = time.time()
    
    srel_mat = zeros(srel_mat_expected_shape(m4du.sr_class, 
                                             m4du.tmap,
                                             m4du.obj_locations))*1.0
    
    
    processedExamples = 0

    while processedExamples < totalExamples:
        pool.restart()
        #desc, func, args = functions[processedExamples]
        #result = func(*args)
        result = pool.doneQueue.get()

        processedExamples += 1
        for (i, j, k, l), score in result:
            srel_mat[i, j, k, l] = score
        now = time.time()
        progress = float(processedExamples)/totalExamples
        elapsedMinutes = (now - startTime) / 60.0
        estimatedTotal = elapsedMinutes / progress
        print "progress: %.2f%%" % (progress * 100.0),
        print "(going for %.2f minutes," % elapsedMinutes,
        print "about %.2f minutes remaining)" % (estimatedTotal - elapsedMinutes)
    now = time.time()

    totalTime = (now - startTime)/60.0
    print "took %.2f minutes" %  totalTime
    print "matrix", na.shape(srel_mat)
    return srel_mat
    

def pack_get_srel_given_lmark_vpts_matrix(m4du):
    functions = []
    tmap, tmap_cnt, tmap_locs = m4du.clusters.get_topological_map()
    engineMap = m4du.sr_class.engineMap
    
    
    globals()["m4du"] = m4du

    #sorted(m4du.tmap.keys())
    tmap_keys = m4du.tmap_keys 
    exampleCount = 0

    for j, tmapKey_j in enumerate(tmap_keys):
        sloc = m4du.tmap_locs[tmapKey_j]
        for k, tmapKey_k in enumerate(tmap_keys):
            eloc = m4du.tmap_locs[tmapKey_k]
            if math2d.dist(sloc, eloc) <= 20:
                desc = "viewpoint %d, %d" % (j, k)
                functions.append((desc, spatialRelationLoop, 
                                  (sloc, eloc, j, k)))

    return functions

def spatialRelationLoop(sloc, eloc, j, k):
    #get the path here

    global m4du
    figure = createFigure(m4du.clusters, sloc, eloc)

    if figure is None:
        return []

    spatial_relations = m4du.sr_class.engineNames
    results = []
    for i, sr in enumerate(spatial_relations):
        for l in range(len(m4du.obj_locations[0])):
            
            ground = m4du.createGround(l)
            
            sc = m4du.p_srel(sr, ground, figure)

            results.append(((i, j, k, l), sc))

        #print "i=", i, engine

    return results



def loadSrelMatrix(fname, expectedShape):
    print "loading", fname
    mat = na.fromfile(fname)
    print "shape", mat.shape
    print "expected", expectedShape
    return mat.reshape(expectedShape)


def main(argv):
    smat = loadSrelMatrix(argv[1], expectedShape=[11, 148, 148, 171])
    print "loaded", smat.shape

    flatSmat = na.ravel(smat[0])
    sorted = na.argsort(flatSmat)
    print "biggest", sorted[-1], flatSmat[sorted[-1]]

    biggestIdx = na.unravel_index(sorted[-1], smat[0].shape)
    
    print biggestIdx, smat[0][biggestIdx]

    
    
if __name__=="__main__":
    main(sys.argv)
    
