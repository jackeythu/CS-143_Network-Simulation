
from events import *
from element import *
from engine import *
import tcp_fast
import tcp_tahoe



class parse:
# Read parameters from testcase file
     
    def __init__(self, engine, case):
        self.hosts = {}
        self.routers = {}
        self.links = {}
        self.flows = {}
        self.engine = engine
        self.read(case)
        engine.parse = self
        

    def read(self, testcase):
        with open(testcase, 'rb') as testcaseFile:
            objectType = ''
            objectID = ''
            hostAttributes = ['IP']
            routerAttributes = ['IP']
            flowAttributes = ['src', 'dst', 'data_amt', 'start']
            linkAttributes = ['rate', 'delay', 'buffer', 'node1', 'node2']
            
            hostPara = {key: '' for key in hostAttributes}
            routerPara = {key: '' for key in routerAttributes}
            flowPara = {key: '' for key in flowAttributes}
            linkPara = {key: '' for key in linkAttributes}
            
            
            for line in testcaseFile:
                content = line.split()
                if content == [] and objectID == '':#ignore empty line
                    objectType = ''
                    objectID = ''
                    continue
                elif content == []:
                    keyword = ''
                else:
                    keyword = content[0]
                    
                    
                if keyword == '//':#ignore comment line
                    continue
                
                elif keyword in ['Host', 'Link', 'Router', 'Flow']:
                    objectType = keyword
                    objectID = ''
                                    
                elif keyword == 'ID' or (keyword == '' and objectID != ''):
                    #Create the object if we finish reading all attributes of the object
                    #and followed by the next object ID or an empty line.
                    if objectID == '':
                        objectID = content[1]
                    elif objectType == 'Host':
                        new_host = Host(engine = self.engine, name = objectID, address = hostPara['IP'])
                        self.hosts[objectID] = new_host
                        
                    elif objectType == 'Router':
                        new_router = Router(engine = self.engine, name = objectID, address = routerPara['IP'], updateTime=ROUTER_PACKET_GENERATION_INTERVAL)
                        self.routers[objectID] = new_router
                        self.engine.push_event(Event(0, new_router, EVENT_ROUTINGTABLE_UPDATE))
                        
                    elif objectType == 'Link':
                        #make sure that the link connects two valid hosts/routers
                        if linkPara['node1'] in self.hosts:
                            n1 = self.hosts[linkPara['node1']]
                        elif linkPara['node1'] in self.routers:
                            n1 = self.routers[linkPara['node1']]
                        
                        if linkPara['node2'] in self.hosts:
                            n2 = self.hosts[linkPara['node2']]
                        elif linkPara['node2'] in self.routers:
                            n2 = self.routers[linkPara['node2']]
                        
                        new_link = Link(engine = self.engine, name = objectID, node1 = n1, node2 = n2,
                                        rate = 1.0* 1024 * 1024 * float(linkPara['rate'] )/ 8, 
                                        delay = 0.001 * float(linkPara['delay']),
                                        buffer_size = 1024 * int(linkPara['buffer']))
                        self.links[objectID] = new_link
                         
                    elif objectType == 'Flow':     
                        new_flow = Flow(engine = self.engine, name = objectID, 
                                        source = self.hosts[flowPara['src']], 
                                        destination = self.hosts[flowPara['dst']],
                                        amount = 1024 * int(flowPara['data_amt']),
                                        start_time = float(flowPara['start']), 
                                        tcp = tcp_fast.TcpFast())
                        self.flows[objectID] = new_flow
                        self.engine.push_event(Event(new_flow.start_time, new_flow, EVENT_FLOW_START))

                    if keyword == 'ID':
                        objectID = content[1]
                
                
                if (objectType == 'Host'):
                    if keyword in hostAttributes:
                        hostPara[keyword] = content[1]
                        
                elif (objectType == 'Router'):
                    if keyword in routerAttributes:
                        routerPara[keyword] = content[1]
                        
                elif (objectType == 'Link'):
                    if keyword in linkAttributes:
                        linkPara[keyword] = content[1]
                    elif keyword == 'connection':
                        linkPara['node1'] = content[1]
                        linkPara['node2'] = content[2]
                        
                elif (objectType == 'Flow'):
                    if keyword in flowAttributes:
                        flowPara[keyword] = content[1]
                   
                    
               
                
            
        
