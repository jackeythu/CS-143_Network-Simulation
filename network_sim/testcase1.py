from events import * 
from element import  *
from engine import SimEngine
from parse import *

import matplotlib.pyplot as plt
import tcp_fast
import tcp_tahoe

def main():
        
        '''
            For Test Case 1,
            Link ID: L0, L1, L2, L3, L4, L5
            Link Rate: 10 Mbps (For L0 and L5, Link Rate: 12.5 Mbps)
            Link Delay: 10 ms
            Link Buffer: 64 KB
            Flow ID: F1
            Flow Src: H1
            Flow Dest: H2
            Data Amt: 20MB
            Flow Start: 0.5s
            
            dataPacket Size: 1024 bytes
            ackPacket Size: 64 KB
            ROUTER_PACKET_GENERATION_INTERVAL: 1.0 s
        '''
        
        engine = SimEngine(30)
        file_name = 'testcase1.txt'
        parse(engine, file_name)
        #print engine.queue
        engine.run()
        
        
        '''
            Data Visualization
        '''
#         print engine.recorder.category[CATE_LINK_RATE]
        
        
        with open('1_window_size.txt', 'w') as myFile:
            for name, inventory in engine.recorder.category[CATE_WINDOW_SIZE].items():
                myFile.write('{}:\n'.format(name))
                for x,y in inventory:
                    myFile.write('{}, {}\n'.format(x, y))
        
        
        engine.recorder.plot()
        print 'Imgs Plot: Finished!'


if __name__ == '__main__':
    main()
