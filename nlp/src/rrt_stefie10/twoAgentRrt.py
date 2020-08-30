from rrt.plane_rrt import PlaneRrtBuilder
from rrt.rapidlyExploringRandomTree import RapidlyExploringRandomTreeBuilder
import math2d
import pylab as mpl


class TwoAgentRrtBuilder(RapidlyExploringRandomTreeBuilder):
    
    def __init__(self, limits):
        RapidlyExploringRandomTreeBuilder.__init__(self)
        
        self.prb = PlaneRrtBuilder(limits)
     
    def randomState(self):
        return (self.prb.randomState(), self.prb.randomState())
    
    def nearestNeighbor(self, x_rand, tree):
        nodes = [n for n in tree.nodes()]
        
        x1, x2 = x_rand
        
        distances = [math2d.dist(p1, x1) + math2d.dist(p2, x2) for p1, p2 in nodes]
        
        minI, min = math2d.argMin(distances)
        return nodes[minI]
    
    def selectInput(self, goal, start):
        
        g1, g2 = goal
        s1, s2 = start
        
        deriv1 = self.prb.selectInput(g1, s1)
        deriv2 = self.prb.selectInput(g2, s2)
            
        return deriv1, deriv2

    
    def newState(self, x_near, u, dt):
        
        p1, p2 = x_near
        
        u1, u2 = u
        
        return (self.prb.newState(p1, u1, dt), 
                self.prb.newState(p2, u2, dt)) 
    
    def draw(self, tree):
        
        colors = ["b", "r"]
        for idx, color in enumerate(colors):
            X = []
            Y = []
            for node in tree.nodes():
                x, y = node[idx]
                X.append(x)
                Y.append(y)
            #mpl.scatter(X, Y, c=color)
                
        for edge in tree.edges():
            s1, s2 = edge[0]
            g1, g2 = edge[1]
            
            mpl.plot([s1[0], g1[0]], 
                     [s1[1], g1[1]], colors[0])
            mpl.plot([s2[0], g2[0]], 
                     [s2[1], g2[1]], colors[1])
                
        mpl.axis(self.limits)
        
    @property
    def limits(self):
        return self.prb.limits
        
def main():

    rrtBuilder = TwoAgentRrtBuilder([0, 100, 0, 100])
    
    for k in [10, 100, 1000]:
        tree = rrtBuilder.build(((50, 50), (50, 50)), K=k, dt=1)
        mpl.figure()
        rrtBuilder.draw(tree)
        mpl.title("Tree for k=%d" % k)
    
    
    mpl.show()
if __name__ == "__main__":
    main()