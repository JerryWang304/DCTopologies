
# coding: utf-8

# In[15]:

# Elements in DC simulation
from DCTopo import FatTree
import simpy
import random
import networkx as nx
class Flow(object):   
    # def __init__(self,src,des,demand,size):
    # src and des are integer
    def __init__(self,time,src,des,size):
        self.begin_time = time
        self.src = src
        self.end_time = time
        self.des = des
#        self.demand = demand # bandwidth demand of each flow
        self.size = size # flow size such as 1Gb
    def __repr__(self):
        return "from {} to {},\t size: {:.4f},\t time: {:.2f}".format(self.src,self.des,self.size,self.begin_time)
        
        
class FlowGenerator(object):
    """
    generate a flow to receiver
    the destination of the flow is randomly choosen from left switches
    
    """
    def __init__(self,env,god,out,interval,initial_delay=0,end_time=float('inf'),debug=False):
        self.env = env
        self.god = god
        self.interval = interval
        self.initial_delay = initial_delay
        self.end_time = end_time
        self.out = out # out is a switch
        self.flow_generated = 0
        self.debug = debug
        self.action = self.env.process(self.run())
    def run(self):
        while True:
            yield self.env.timeout(self.initial_delay)
            while self.env.now < self.end_time:
                #print "Flow Generator"
                #yield self.env.timeout(self.interval)
                yield self.env.timeout(random.expovariate(1.0/self.interval))
                #assert self.out is not None
                # 同一时刻向out注入flows
                for receiver in self.out:
                    des = receiver.id
                    while des == receiver.id:
                        des = random.randint(0,self.god.topo.num_of_nodes-1)
                    flow = Flow(self.env.now,receiver.id,des,random.uniform(1,100))
                    #print flow
                    if self.debug:
                        print flow
                    self.flow_generated += 1
                    receiver.store.put(flow)
# 收集flows                    
class Statistics(object):
    def __init__(self,env):
        self.env = env
        self.store = simpy.Store(env)
       
    @property
    def ave_time(self):
        
        durations = [] # 每个流持续的时间
        #print len(self.store.items)
        for flow in self.store.items:
            duration = flow.end_time - flow.begin_time
            durations.append(duration)
        average = sum(durations)*1.0/len(durations)
        return average
    
class Port(object):
    # port is designed for forwarding flows
    """
    implement ECMP
    src: where the flows originate
    """
    def __init__(self,env,god,src,rate,statistic):
        self.env = env
        self.src = src
        self.rate = rate
        self.god = god # it knows all the switches...
        self.topo = god.topo.topo # nx Graph()
        self.out = statistic
        self.action = self.env.process(self.run())
    def run(self):
        while True:
            flow = yield self.src.store.get()
            #print flow
            if flow.des == self.src.id:
                flow.end_time = self.env.now
                self.out.store.put(flow)
                #print flow,
                #print " -> arriving time %.8f" % self.env.now
                continue
            # compute the next hop
            
            paths = nx.all_shortest_paths(self.topo,self.src.id,flow.des)
            next_hops = []
            for path in paths:
                if len(path)>1:
                    next_hops.append(path[1])
            next_hop = random.choice(next_hops)
            #print next_hop,
            # forwarding to next_hop
            target = self.src.id
            for sw in self.god.all_nodes:
                if sw.id == next_hop:
                    target = sw
                    break
            #print target
            if target:
                flow.src = target.id
                yield self.env.timeout(flow.size*1.0/self.rate)
                target.store.put(flow)

# class Link(object):
#     # link between adjacent switches
#     # src and des are both switches
#     # sending flows fron src to des
#     def __init__(self,god,env,src,des,rate):
#         self.env = env
#         self.topo = god.topo.topo # the flow knows all the shortest pathes from src to des......
#         self.original = src
#         self.src = src
#         self.des = des
#         self.rate = rate
#         self.action = env.process(self.run())
        
#     def __repr__(self):
#         return "{} to {}".format(self.src,self.des)
    
#     def run(self):
#         while True:
#             flow = yield self.src.store.get() # FIFO temporayily
#             #print "Original: ",
#             print flow
            
            
#             #if flow.des == self.src.id: # the flow arrives at the destination
#             #    print flow,
#             #    print " arrives"
#             #    continue
#             # choose the next hop according to the shortest pathes
#             #paths = nx.all_shortest_paths(self.topo,self.src.id,self.des.id)
#             #next_hops = []
#             #for path in paths:
#             #    next_hops.append(path[1])
#             #if len(next_hops) == 1:
#             #    flow.src = next_hops[0]
#             #else:
#                 # 随机选择下一跳
#             #    next_hop = random.choice(next_hops)
#                 # 当前的流发送到下一跳后，流的src更新为到达后的节点的编号（为了方便下一次计算最短路径）
#                 # 若想知道流最原始的来源，flow.original便是
#             #    flow.src = nex_hop
                
#             assert self.des is not None
#             sending_time = flow.size/self.rate
#             yield self.env.timeout(sending_time)
#             self.des.store.put(flow)           

class Switch(object):
    
    def __init__(self,env,god,id,qlimit=None,portNum=1,rate=10000,statistic=None):
        self.env = env
        self.id = id
        self.god = god
        self.qlimit = qlimit
        self.store = simpy.Store(env)# store flows
        self.portNum = portNum
        
        self.ports = [Port(env,god,self,rate,statistic) for i in range(portNum)] 
        self.flow_queue = []
        #self.connect_others()
    # connect other switches with links
#     def connect_others(self):
#         index_of_neighbors = self.god.topo.topo.neighbors(self.id) # len(index_of_neighbors) == slef.portNum
#         neighbor_switches = [sw for sw in self.god.switches if sw.id in index_of_neighbors] # from smaller id to bigger id
#         for i in range(self.portNum):
#             self.ports[i].des = neighbor_switches[i]
    def __repr__(self):
        return "Switch:{}".format(self.id)
        
        
# class WaitAndHop(object):
#     # it has to schedule all the flows to achieve a low network cost
#     def __init__(self,flows,god):
#         self.flows = flows
#         self.topo = god.topo.topo # use it to generate VLANs
        
   
# class God(object):
#     # topo maybe ft(FatTree Type).topo
#     def __init__(self,env,DCTopo,rate,statistic):
#         self.topo = DCTopo 
#         self.env = env
#         self.rate = rate
#         self.switches = self.generate_switches() # Switch object
#         self.statistic = statistic
#         #print self.switches
#         #self.connect_switches()
#         self.generate_flows()
        
#     def generate_switches(self):
#         num_switches = self.topo.num_of_switches
#         sw = []
#         for i in range(num_switches):
#             switch = Switch(self.env,self,i,qlimit=None,portNum=self.topo.portNum,rate=self.rate,statistic=None)
#             sw.append(switch)
#         return sw
    
#     def connect_switches(self):
#         # print len(self.switches[13].ports)
#         #print "All Switches: ",
#         #print self.switches 
#         for sw in self.switches:
#             index_of_neighbors = self.topo.topo.neighbors(sw.id) # len(index_of_neighbors) == sw.portNum
#             #print sw,
#             #print index_of_neighbors
#             neighbor_switches = [switch for switch in self.switches if switch.id in index_of_neighbors]
#             #print sw,
#             #print neighbor_switches
            
#             for i in range(len(neighbor_switches)):
#                 sw.ports[i].des = neighbor_switches[i]
#             # delete useless links
#             for link in sw.ports[:]:
#                 if link.des.id == link.src.id:
#                     sw.ports.remove(link)
#             #print sw,
#             #print sw.ports
        
    # def generate_flows(self):
    #     # generate flows first
    #     # onyl apply to fat tree
    #     # 向每个edge switches注入流，这些流会发送到网络中
    #     edge_switch = [sw for sw in self.switches if sw.id in self.topo.edge_switches]
    #     flow_generator = FlowGenerator(self.env,self,edge_switch,interval=10,initial_delay=0,end_time=float('inf'),debug=False)
    
    #def run(self):
    
# env = simpy.Environment()
# ft = FatTree(4)

# # path = nx.all_shortest_paths(ft.topo,12,4)
# # for i in path:
# #     print i
# # print ft.topo.neighbors(14)
# g = God(env,ft,100)
# env.run(until=100)
# 只适应于全部用来转发的情况      
class God(object):
    
    def __init__(self,env,DCTopo,rate,statistic):
        self.topo = DCTopo 
        self.env = env
        self.rate = rate
        self.statistic = statistic
        
        self.switches = self.generate_switches() # Switch object
        self.all_nodes = self.switches
        self.generate_flows()
        
    def generate_switches(self):
        
        sw = []
        
        for id in self.topo.switches_ids:
            degree = self.topo.topo.degree(id) # 当前交换机连接多少个节点
            switch = Switch(self.env,self,id,qlimit=None,portNum=degree,rate=self.rate,statistic=self.statistic)
            sw.append(switch)
        return sw
        
    
    def generate_flows(self):
        # generate flows first
        # 每个server
        servers = [s for s in self.switches]
        #print servers
        flow_generator = FlowGenerator(self.env,self,servers,interval=10,initial_delay=0,end_time=float('inf'),debug=False)



# In[ ]:



