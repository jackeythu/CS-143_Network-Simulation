from events import * 
from element import  *
from engine import *
import matplotlib.pyplot as plt
import tcp_fast

def main():
    
    '''
        For Test Case 0,
        Link ID: L1
        Link Rate: 10 Mbps
        Link Delay: 10 ms
        Link Buffer: 64 KB
        Flow ID: F1
        Flow Src: H1
        Flow Dest: H2
        Data Amt: 20MB
        Flow Start:1.0s
        
        dataPacket Size: 1024 bytes
        ackPacket Size: 64 KB
        ROUTER_PACKET_GENERATION_INTERVAL: 1.0 s
    '''
    
    engine = SimEngine(20)

    host1 = Host(engine, 'H1', '192.168.0.1')   
    host2 = Host(engine, 'H2', '192.168.0.2')
    
    flow1 = Flow(engine, 'F1', host1, host2, 20 * 1024 * 1024 / PACKET_SIZE, tcp_fast.TcpFast())

    link0 = Link(engine, 'L1', host1, host2, 0.01, 10 * 1024 * 1024, 64 * 1024)

    engine.push_event(Event(0.5, flow1, EVENT_FLOW_START))
    
    engine.run()
            
        
    '''
        Data Visualization
    '''
    plot_n = 1;
    
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
                    
    for i in range(1, 2):
        cur_variable = 'cate_link_rate'
        cur_name = 'L' + str(i)
        cur_string = cur_variable + '_' + cur_name
        engine.recorder.draw(engine.recorder.category[cur_variable][cur_name], plot_n,
                             cur_string, cur_string, 'Time / s', 'Link Rate / bps')
        plot_n = plot_n + 1
        
    for i in range(1, 2):
        cur_variable = 'cate_buffer_occupancy'
        cur_name = 'L' + str(i)
        cur_string = cur_variable + '_' + cur_name
        engine.recorder.draw(engine.recorder.category[cur_variable][cur_name], plot_n,
                             cur_string, cur_string, 'Time / s', 'Buffer Occupancy / bytes')
        plot_n = plot_n + 1
    
    for i in range(1, 2):
        cur_variable = 'cate_packet_loss'
        cur_name = 'L' + str(i)
        cur_string = cur_variable + '_' + cur_name
        engine.recorder.draw(engine.recorder.category[cur_variable][cur_name], plot_n,
                             cur_string, cur_string, 'Time / s', 'Packet Loss / pkts')
        plot_n = plot_n + 1
    
    print '\n'
    print 'Imgs Plot: Finished!'
    
#     plt.show()

if __name__ == '__main__':
    main()
