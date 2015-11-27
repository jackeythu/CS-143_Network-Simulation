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
        print engine.queue
        engine.run()
        
        
        '''
            Data Visualization
        '''
        plot_n = 1;
        
        for i in range(1, 2):
            cur_variable = 'cate_window_size'
            cur_name = 'F' + str(i)
            cur_string = cur_variable + '_' + cur_name
            engine.recorder.draw(engine.recorder.category[cur_variable][cur_name], plot_n,
                                 cur_string, cur_string, 'Time / s', 'Window Size / pkts')
            plot_n = plot_n + 1 

        for i in range(1, 2):
            cur_variable = 'cate_pkts_received'
            cur_name = 'F' + str(i)
            cur_string = cur_variable + '_' + cur_name
            engine.recorder.draw(engine.recorder.category[cur_variable][cur_name], plot_n,
                                 cur_string, cur_string, 'Time / s', 'Packets Received / pkts')
            plot_n = plot_n + 1 
            
        for i in range(1, 2):
            cur_variable = 'cate_flow_rate'
            cur_name = 'F' + str(i)
            cur_string = cur_variable + '_' + cur_name
            engine.recorder.draw(engine.recorder.category[cur_variable][cur_name], plot_n,
                                 cur_string, cur_string, 'Time / s', 'Flow Rate / bps')
            plot_n = plot_n + 1 
              
        for i in range(1, 2):
            cur_variable = 'cate_packet_delay'
            cur_name = 'F' + str(i)
            cur_string = cur_variable + '_' + cur_name
            engine.recorder.draw(engine.recorder.category[cur_variable][cur_name], plot_n,
                                 cur_string, cur_string, 'Time / s', 'Packet Delay / s')
            plot_n = plot_n + 1  
                        
        for i in range(0, 6):
            cur_variable = 'cate_link_rate'
            cur_name = 'L' + str(i)
            cur_string = cur_variable + '_' + cur_name
            engine.recorder.draw(engine.recorder.category[cur_variable][cur_name], plot_n,
                                 cur_string, cur_string, 'Time / s', 'Link Rate / bps')
            plot_n = plot_n + 1
            
        for i in range(0, 6):
            cur_variable = 'cate_buffer_occupancy'
            cur_name = 'L' + str(i)
            cur_string = cur_variable + '_' + cur_name
            engine.recorder.draw(engine.recorder.category[cur_variable][cur_name], plot_n,
                                 cur_string, cur_string, 'Time / s', 'Buffer Occupancy / bytes')
            plot_n = plot_n + 1
        
        for i in range(0, 6):
            cur_variable = 'cate_packet_loss'
            cur_name = 'L' + str(i)
            cur_string = cur_variable + '_' + cur_name
            engine.recorder.draw(engine.recorder.category[cur_variable][cur_name], plot_n,
                                 cur_string, cur_string, 'Time / s', 'Packet Loss / pkts')
            plot_n = plot_n + 1
        
        print '\n'
        print 'Imgs Plot: Finished!'
#         plt.show()

if __name__ == '__main__':
    main()
