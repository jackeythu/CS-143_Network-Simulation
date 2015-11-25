from events import * 
from element import  *
from engine import SimEngine

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
        
        host1 = Host(engine, 'H1', '192.168.0.1')   
        host2 = Host(engine, 'H2', '192.168.0.2')
        
        flow1 = Flow(engine, 'F1', host1, host2, 20 * 1024 * 1024 / PACKET_SIZE, tcp_tahoe.TcpTahoe())
        
        router1 = Router(engine, 'R1', '192.168.1.1')
        router2 = Router(engine, 'R2', '192.168.1.2')
        router3 = Router(engine, 'R3', '192.168.1.3')
        router4 = Router(engine, 'R4', '192.168.1.4')

        link0 = Link(engine, 'L0', host1, router1, 0.01, 12.5 * 1024 * 1024, 64 * 1024)
        link1 = Link(engine, 'L1', router1, router2, 0.01, 10 * 1024 * 1024, 64 * 1024)
        link2 = Link(engine, 'L2', router1, router3, 0.01, 10 * 1024 * 1024, 64 * 1024)
        link3 = Link(engine, 'L3', router2, router4, 0.01, 10 * 1024 * 1024, 64 * 1024)
        link4 = Link(engine, 'L4', router3, router4, 0.01, 10 * 1024 * 1024, 64 * 1024)
        link5 = Link(engine, 'L5', host2, router4, 0.01, 12.5 * 1024 * 1024, 64 * 1024)
                
        engine.push_event(Event(0.5, flow1, EVENT_FLOW_START))
                
        event1 = Event(0, router1, EVENT_ROUTINGTABLE_UPDATE)
        event2 = Event(0, router2, EVENT_ROUTINGTABLE_UPDATE)
        event3 = Event(0, router3, EVENT_ROUTINGTABLE_UPDATE)
        event4 = Event(0, router4, EVENT_ROUTINGTABLE_UPDATE)
        engine.push_event(event1) 
        engine.push_event(event2) 
        engine.push_event(event3) 
        engine.push_event(event4) 
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
