import networkx as nx

class RapidlyExploringRandomTreeBuilder:
    """
    Implemented following LaValle, 1998
    """
    
    def __init__(self):
        pass
        
    

    def randomState(self):
        raise NotImplementedError()
        
    
    def nearestNeighbor(self, x_rand, tree):
        raise NotImplementedError()
    
    def selectInput(self, goal, start):
        raise NotImplementedError()
    
    def newState(self, x_near, u, deltaT):
        raise NotImplementedError()
    
    def build(self, x_init, K, dt):
        tree = nx.Graph()
        
        tree.add_node(x_init)
        
        for k in range(K):
            print "k", k
            x_new = None
            
            cnt = 0
            while x_new == None and cnt < 10:
                x_rand = self.randomState()
                x_near = self.nearestNeighbor(x_rand, tree)
                u = self.selectInput(x_rand, x_near)
                x_new = self.newState(x_near, u, dt)
                if x_new != None:
                    tree.add_node(x_new)
                    tree.add_edge(x_near, x_new)
                    self.callback(k, tree)
                cnt += 10
        return tree
    
    def callback(self, k, tree):
        pass