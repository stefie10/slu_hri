from rrt.rapidlyExploringRandomTree import RapidlyExploringRandomTreeBuilder
import math2d
import pylab as mpl
import random

class PlaneRrtBuilder(RapidlyExploringRandomTreeBuilder):
    
    def __init__(self, limits):
        self.xmin, self.xmax, self.ymin, self.ymax = limits
        
    
    @property    
    def limits(self):
        return [self.xmin, self.xmax, self.ymin, self.ymax]
    
    def randomState(self):
        return (random.uniform(self.xmin, self.xmax), 
                random.uniform(self.ymin, self.ymax))
    
    def nearestNeighbor(self, x_rand, tree):
        nodes = [n for n in tree.nodes()]
        distances = [math2d.dist(n, x_rand) for n in nodes]
        
        minI, min = math2d.argMin(distances)
        return nodes[minI]
    
    def selectInput(self, goal, start):    
        direction = math2d.direction(start, goal)
        dx, dy = math2d.unitVector(direction)
        return dx, dy

    
    def newState(self, x_near, u, deltaT):
        x, y = x_near
        return (x_near[0] + u[0] * deltaT,
                x_near[1] + u[1] * deltaT)
        
    def draw(self, tree):
        X = [x for x,y in tree.nodes()]
        Y = [y for x,y in tree.nodes()]

        #mpl.scatter(X, Y)
            
        for edge in tree.edges():
            mpl.plot([x for x,y in edge],
                     [y for x,y in edge], "k")
        mpl.axis(self.limits)
            
    def tcallback(self, k, tree):
        
        if k % 30 == 0:
            
            self.draw(tree)

            mpl.ion()
            mpl.draw()
            #time.sleep(10)
            #mpl.show()
def main():

    rrtBuilder = PlaneRrtBuilder([0, 100, 0, 100])
    
    for k in [10, 100, 500, 1000]:
        tree = rrtBuilder.build((50, 50), K=k, dt=1)
        mpl.figure()
        rrtBuilder.draw(tree)
        mpl.title("Tree for k=%d" % k)
    
    
    mpl.show()
if __name__ == "__main__":
    main()