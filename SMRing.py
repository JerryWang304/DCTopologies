# Small World topology
#% matplotlib inline
# coding: utf-8

import networkx as nx
import simpy
import matplotlib.pyplot as plt
import random
class SWRing(object):
    """
    k个点组成首位相接的环；每个点再和其他任意四个点相连
    """
    def __init__(self,k):
        self.k = k
        self.num_switches = k
        self.switches_ids = [i for i in range(self.k)]
        self.topo = nx.Graph()
        self.generate_topo()
    def generate_topo(self):
        # 先构建环
        for i in range(self.k):
            self.topo.add_edge(i,(i+1)%(self.k))
        # 然后每个节点随机连接四条线
        for node in range(self.k):
            old = [(node+1)%self.k,(node-1)%self.k] #   和node已经连接的节点
            print node,
            print old
            for i in range(4)
                random_node = random.randint(0,self.k-1)
                
                if random_node not in old and self.topo.degree(random_node)<4:
                    old.append(random_node)
                    self.topo.add_edge(random_node,node)
                
    def show(self):
        pos = nx.circular_layout(self.topo)
        nx.draw_networkx(self.topo,pos)
        nx.draw_networkx_nodes(self.topo,pos,self.switches_ids,node_color='w')
        
        plt.title(r"Small World Ring nodes = {}".format(self.k))
        plt.axis('off')
        plt.show()
        
ring = SWRing(12)
print ring.topo.node
#print ring.topo.adj[3].keys()
#print dir(ring.topo)
ring.show()