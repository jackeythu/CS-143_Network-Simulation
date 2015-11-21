from network_sim.events import * 
from network_sim.element import  *
from network_sim.engine import *

def main():
    
    engine = SimEngine(20)
    
    host1 = Host(engine, 'h1', '192.168.0.1')
    host2 = Host(engine, 'h2', '192.168.0.1')
    
    '''
        [Zilong]
        Flow of 20 packets here, but end only sending out one packet
    '''
    flow1 = Flow(engine, 'f1', host1, host2, 20)
    
    '''
        [Zilong]
        delay = 0.01, rate = 10e6, buffer_size = 64e3
    '''
    link1 = Link(engine, 'l1', host1, host2, 0.01, 10e6, 64 * 1024)
    engine.push_event(Event(1, flow1, EVENT_FLOW_START))
    
    engine.run()


if __name__ == '__main__':
    main()