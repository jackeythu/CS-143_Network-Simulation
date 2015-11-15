from Errors import ParaMissing
from Errors import unknownObject
from Errors import unknownKeyword

class parse:
# Read parameters from testcase file
    def __init__(self, case = 'xxx/testcase/testcase0.txt'):
        self.hosts = {}
        self.routers = {}
        self.links = {}
        self.flows = {}
        self.readCase(case)
        
    def readCase(self, testcase):
        with open(testcase, 'rb') as testcaseFile:
            # read file line by line
            lineNum = 0
            objectType = ''
            objectID = ''
            hostAttributes = ('IP')
            routerAttributes = ('IP')
            flowAttributes = ('src', 'dst', 'data_amt', 'start')
            linkAttributes = ('rate', 'delay', 'buffer', 'source', 'destination')
            
            hostPara = {key:'' for key in hostAttributes}
            routerPara = {key:'' for key in routerAttributes}
            flowPara = {key:'' for key in flowAttributes}
            linkPara = {key:'' for key in linkAttributes}
            
            
            for line in testcaseFile:
                lineNum += 1
                line_content = line.split()
                if line_content == []:#ignore empty line
                    continue
                keyword = line_content[0]
                if keyword == '//':#ignore comment line
                    continue
                elif keyword in ['Host', 'Link', 'Router', 'Flow']:
                    objectType = keyword
                    objectID = ''
                    
                elif keyword in hostAttributes and line_content[1] != '':
                    hostPara[keyword] = line_content[1]
                elif keyword in routerAttributes and line_content[1] != '':
                    routerPara[keyword] = line_content[1]
                elif keyword in flowAttributes and line_content[1] != '':
                    flowPara[keyword] = line_content[1]
                elif keyword in linkAttributes and line_content[1] != '':
                    linkPara[keyword] = line_content[1]
                elif keyword == 'connection' and line_content[1] != '' and line_content[2] != '':
                    linkPara['source'] = line_content[1]
                    linkPara['destination'] = line_content[2]
                
                    
                elif keyword == 'ID':
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
                            if routerPara[key] in ['',[]]:
                                raise ParaMissing(lineNum = lineNum,
                                                  objectType = objectType,
                                                  objectID = objectID,
                                                  missingPara = key)
                        self.make_router(name = objectID, IP_address = hostPara['IP'])
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
                                           data_amount = int(flowPara['data_amt']),
                                           start_time = float(flowPara['start']))
                        else:
                            raise  unknownObject(lineNum = lineNum, 
                                                 message = 'unknown host')     
                    elif objectType == 'Link':
                        for key in linkAttributes:
                            if linkPara[key] in ['', []]:
                                raise ParaMissing(lineNum = lineNum,
                                                  objectType = objectType,
                                                  objectID = objectID,
                                                  missingPara = key)
                        #make sure that the link connects two valid hosts/routers
                        for i in [linkPara['source'], linkPara['destination']]:
                            if (i not in self.hosts) and (i not in self.routers):
                                raise unknownObject(lineNum = lineNum,
                                                    message = 'unknown host/router')
                        self.make_link(name = objectID, 
                                       source = linkPara['source'],
                                       destination = linkPara['destination'],
                                       rate = float(linkPara['rate']),
                                       delay = float(linkPara['delay']),
                                       buffer = int(linkPara['buffer']))
                else:
                    raise unknownKeyword(lineNum = lineNum, 
                                         message = 'invalid keyword')
                    
                
                
            
        
