
from Errors import *
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
        self.readCase(case)
        engine.parse = self
    
    def make_host(self, name, IP_address):
        new_host = Host(engine = self.engine, name = name, address = IP_address)
        self.hosts[name] = new_host
        print "Host " + name + " at " + IP_address + " has been made"
        
    def make_router(self, name, IP_address):
        new_router = Router(engine = self.engine, name = name, address = IP_address, updateTime=ROUTER_PACKET_GENERATION_INTERVAL)
        self.routers[name] = new_router
        self.engine.push_event(Event(0, new_router, EVENT_ROUTINGTABLE_UPDATE))
        print "Router " + name + " at " + IP_address + " has been made"
     
    def make_link(self, name, node1, node2, rate, delay, buffer_size):
        new_link = Link(engine = self.engine, name = name, node1 = node1, node2 = node2,
                        rate = rate, delay = delay, buffer_size = buffer_size)
        self.links[name] = new_link
        print "Link " + name + " at " + node1.name + " and " + node2.name + " has been made"
          
    def make_flow(self, name, source, destination, data_amount, start_time):
        new_flow = Flow(engine = self.engine, name = name, source = source, destination = destination,
                        amount = data_amount, start_time = start_time, tcp = tcp_fast.TcpFast())
        self.flows[name] = new_flow
        self.engine.push_event(Event(new_flow.start_time, new_flow, EVENT_FLOW_START))
        print "Flow " + name + " from " + source.name + " to " + destination.name + " has been made"
        

    def readCase(self, testcase):
        with open(testcase, 'rb') as testcaseFile:
            # read file line by line
            lineNum = 0
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
                lineNum += 1
                line_content = line.split()
                if line_content == [] and objectID == '':#ignore empty line
                    objectType = ''
                    objectID = ''
                    continue
                elif line_content == []:
                    keyword = ''
                else:
                    keyword = line_content[0]
                    
                    
                if keyword == '//':#ignore comment line
                    continue
                
                elif keyword in ['Host', 'Link', 'Router', 'Flow']:
                    objectType = keyword
                    objectID = ''
                                    
                elif keyword == 'ID' or (keyword == '' and objectID != ''):
                    #Create the object if we finish reading all attributes of the object
                    #and followed by the next object ID.
                    if objectID == '':
                        objectID = line_content[1]
                    elif objectType == 'Host':
                        for key in hostAttributes:
                            if hostPara[key] in ['', []]:
                                raise ParaMissing(lineNum = lineNum,
                                                  objectType = objectType,
                                                  objectID = objectID,
                                                  missingPara = key)
                        self.make_host(name = objectID, IP_address = hostPara['IP'])
                        
                    elif objectType == 'Router':
                        for key in routerAttributes:
                            if routerPara[key] in ['', []]:
                                raise ParaMissing(lineNum = lineNum,
                                                  objectType = objectType,
                                                  objectID = objectID,
                                                  missingPara = key)
                        self.make_router(name = objectID, IP_address = routerPara['IP'])
                        
                    elif objectType == 'Link':
                        for key in linkAttributes:
                            if linkPara[key] in ['', []]:
                                raise ParaMissing(lineNum = lineNum,
                                                  objectType = objectType,
                                                  objectID = objectID,
                                                  missingPara = key)
                        #make sure that the link connects two valid hosts/routers
                        if linkPara['node1'] in self.hosts:
                            n1 = self.hosts[linkPara['node1']]
                        elif linkPara['node1'] in self.routers:
                            n1 = self.routers[linkPara['node1']]
                        else:
                            raise unknownObject(lineNum = lineNum,
                                                message = 'unknown host/router')
                        
                        if linkPara['node2'] in self.hosts:
                            n2 = self.hosts[linkPara['node2']]
                        elif linkPara['node2'] in self.routers:
                            n2 = self.routers[linkPara['node2']]
                        else:
                            raise unknownObject(lineNum = lineNum,
                                                message = 'unknown host/router')
                        
                        
                        self.make_link(name = objectID, 
                                       node1 = n1,
                                       node2 = n2,
                                       rate = 1.0* 1024 * 1024 * float(linkPara['rate'] )/ 8,
#                                        rate = float(linkPara['rate']),
#                                        delay = float(linkPara['delay']),
                                       delay = 0.001 * float(linkPara['delay']),
#                                        buffer_size =int(linkPara['buffer']))
                                       buffer_size = 1024 * int(linkPara['buffer']))
                         
                    elif objectType == 'Flow':  
                        for key in flowAttributes:
                            if flowPara[key] in ['', []]:
                                raise ParaMissing(lineNum = lineNum,
                                                  objectType = objectType,
                                                  objectID = objectID,
                                                  missingPara = key)
                        #make sure that the source host and destination host are valid
                        if flowPara['src'] in self.hosts and flowPara['dst'] in self.hosts:
                            self.make_flow(name = objectID, 
                                           source = self.hosts[flowPara['src']],
                                           destination = self.hosts[flowPara['dst']],
#                                            data_amount = int(flowPara['data_amt']),
                                           data_amount = 1024 * int(flowPara['data_amt']),
                                           start_time = float(flowPara['start']))             
                        else:
                            raise  unknownObject(lineNum = lineNum, 
                                                 message = 'unknown host') 

                    if keyword == 'ID':
                        objectID = line_content[1]
                
                
                if (objectType == 'Host'):
                    if keyword in hostAttributes:
                        hostPara[keyword] = line_content[1]
                        
                elif (objectType == 'Router'):
                    if keyword in routerAttributes:
                        routerPara[keyword] = line_content[1]
                        
                elif (objectType == 'Link'):
                    if keyword in linkAttributes:
                        linkPara[keyword] = line_content[1]
                    elif keyword == 'connection':
                        linkPara['node1'] = line_content[1]
                        linkPara['node2'] = line_content[2]
                        
                elif (objectType == 'Flow'):
                    if keyword in flowAttributes:
                        flowPara[keyword] = line_content[1]
                        
                else:
                    raise unknownKeyword(lineNum = lineNum, 
                                         message = 'invalid keyword')
                   
                    
               
                
            
        
