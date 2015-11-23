CATE_LINK_RATE = "cate_link_rate"
CATE_PACKET_LOSS = "cate_packet_loss"
CATE_BUFFER_OCCUPANCY = "cate_buffer_occupancy"
CATE_FLOW_RATE = "cate_flow_rate"
CATE_WINDOW_SIZE = "cate_window_size"
CATE_PACKET_DELAY = "cate_packet_delay"
CATE_ALL = [CATE_LINK_RATE, CATE_PACKET_LOSS, CATE_BUFFER_OCCUPANCY, CATE_FLOW_RATE, CATE_WINDOW_SIZE, CATE_PACKET_DELAY]


import matplotlib.pyplot as plt

class Record(object):
    def __init__(self):
        self.category = {}
        for cate in CATE_ALL:
            self.category[cate] = {}
    
    def record(self, cate, element, time, value):
        """
        if cate == "cate_packet_loss":
                print "!!!!!!!!", self.category[cate]
        """
        if element.name not in self.category[cate]:
            
            self.category[cate][element.name] = [(0, 0)]
        content = self.category[cate][element.name]
        if content[-1][0] != time:
            if content[-1][1] == value:
                content.append((time,value))
            else:
                content.append((time,content[-1][1]))
                content.append((time,value))
        else:
            if content[-1][1] == value:
                pass
            else:
                if len(content) <= 1:
                    content.append((time,value))
                else:
                    if value != content[-2][1]:
                        content.append((time,value))
                    else:
                        content.pop()
                        content.append((time,value))
                

    def record_link_rate(self, element, time, linkrate): 
        self.record(CATE_LINK_RATE, element, time, linkrate)
        
    def record_flow_rate(self, element, time, flowrate): 
        self.record(CATE_FLOW_RATE, element, time, flowrate)
        
    def record_packet_delay(self, element, time, packetdelay): 
        self.record(CATE_PACKET_DELAY, element, time, packetdelay)
      
    def record_packet_loss(self, element, time, packetloss): 
        #print "____________record loss",element.name
        self.record(CATE_PACKET_LOSS, element, time, packetloss)
    def record_buffer_occupancy(self, element, time,bufferoccupancy): 
        self.record(CATE_BUFFER_OCCUPANCY, element, time, bufferoccupancy)   
       
    #def record_window_size(self, element, time, windowsize): 
     #   self.record(CATE_LINK_RATE, element, time, windowsize)
        
    def draw(self, content):

        x,y = zip(*content) 
        plt.plot(x,y)
            
    
            
    
    
