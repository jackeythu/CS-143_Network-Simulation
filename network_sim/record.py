from constants import *
import matplotlib.pyplot as plt
import __main__

class Record(object):
    def __init__(self):
        self.category = {}
        self.unit_string = {
            CATE_LINK_RATE: ('Time / s', 'Link Rate / Mbps'),
            CATE_PACKET_LOSS: ('Time / s', 'Packet Loss / pkts'), 
            CATE_BUFFER_OCCUPANCY: ('Time / s', 'Buffer Occupancy / PCK_SIZE'), 
            CATE_FLOW_RATE: ('Time / s', 'Flow Rate / bps'), 
            CATE_WINDOW_SIZE: ('Time / s', 'Window Size / pkts'), 
            CATE_PACKET_DELAY: ('Time / s', 'Packet Delay / s'), 
            CATE_PKTS_RECEIVED: ('Time / s', 'Packets Received / pkts')
            
        }
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
                pass
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
        
    def smooth(self, interval, inventory):
        i = 1
        start = inventory[0][0]
        sumup = 0; avg = 0
        outputList = []
        slideSize = interval/4; 
        while start + interval< inventory[-1][0]:
            sumup = 0
            returnPoint = -1
            while inventory[i][0]< start + interval:
                if inventory[i][0] > start+slideSize:
                    if returnPoint == -1:
                        returnPoint = i
                if inventory[i-1][0] < start:
                    sumup -= (start-inventory[i-1][0]) * inventory[i-1][1]
                sumup += (inventory[i][0] - inventory[i-1][0])* inventory[i-1][1]
                i += 1
            sumup += (start + interval - max(inventory[i-1][0], start))*inventory[i-1][1]
            
            avg = sumup/interval
            outputList.append((start+interval/2, avg))
            
            start += slideSize
            if returnPoint != -1:
                i = returnPoint
        return outputList
    
    def plot(self):
        n = 0
        for cate in self.category:        
            cur_cate = cate
            x_unit, y_unit = self.unit_string[cate]
            for element in self.category[cur_cate]:                
                cur_string = cur_cate + '_' + element     
    #         print engine.recorder.category[cur_variable]
                smooth = self.smooth(0.1, self.category[cur_cate][element])
#                 smooth = self.category[cur_cate][element]
                if smooth:
                    self.draw(smooth, n, cur_string, cur_string, x_unit, y_unit)
                    n += 1
                else:
                    print 'empty smooth ' + cur_string
   
        print 'Imgs Plot: Finished!'
        
        
        plt.show()
            

            
 
def main():
    a = Record()
    a.calAvg()
         
if __name__ == '__main__':
     
    main()
    
        