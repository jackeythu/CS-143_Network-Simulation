from events import * 
from element import  *
from engine import *

import matplotlib.pyplot as plt
import tcp_fast
import tcp_tahoe

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
    
    engine = SimEngine(60)

    host1 = Host(engine, 'H1', '192.168.0.1')   
    host2 = Host(engine, 'H2', '192.168.0.2')
    
    flow1 = Flow(engine, 'F1', host1, host2, 10000 * 1024 / PACKET_SIZE, tcp_fast.TcpFast())

    link0 = Link(engine, 'L1', host1, host2, 0.01, 10 * 1024 * 1024/8, 64 * 1024)

    engine.push_event(Event(0.5, flow1, EVENT_FLOW_START))
    
    engine.run()
            
    '''
        Data Visualization
    '''
    engine.recorder.plot()
    
        
    
    

if __name__ == '__main__':
    main()
