from constants import *
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
        self.record(CATE_PACKET_LOSS, element, time, packetloss)
        
    def record_buffer_occupancy(self, element, time,bufferoccupancy): 
        self.record(CATE_BUFFER_OCCUPANCY, element, time, bufferoccupancy)
           
    def record_window_size(self, element, time, window_size): 
        self.record(CATE_WINDOW_SIZE, element, time, window_size) 

    def record_pkts_received(self, element, time, pkts_received): 
        self.record(CATE_PKTS_RECEIVED, element, time, pkts_received) 

    def draw(self, content, plot_n, title, file_name, xlabel, ylabel):

        x,y = zip(*content)
        
        plt.figure(plot_n)
        plt.plot(x,y)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        file_name = DIR_IMG + file_name
        plt.savefig(file_name)
    
    '''
        Plot specifying ymin and ymax
    '''
    def draw_minmax(self, content, plot_n, title, file_name, xlabel, ylabel, ymin, ymax):

        x,y = zip(*content)
        
        plt.figure(plot_n)
        plt.plot(x,y)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.ylim(ymin, ymax)
        file_name = DIR_IMG + file_name
        plt.savefig(file_name)