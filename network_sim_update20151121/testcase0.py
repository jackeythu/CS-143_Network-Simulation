from events import * 
from element import  *
from engine import *
import matplotlib.pyplot as plt
import tcp_fast

def main():
    
    engine = SimEngine(20)
    
    host1 = Host(engine, 'h1', '192.168.0.1')
    host2 = Host(engine, 'h2', '192.168.0.1')
    
    '''
        [Zilong]
        Flow of 20 packets here, but end only sending out one packet
    '''
    flow1 = Flow(engine, 'f1', host1, host2, 20, tcp_fast.TcpFast())
    
    '''
        [Zilong]
        delay = 0.01, rate = 10e6, buffer_size = 64e3
    '''
    link1 = Link(engine, 'l1', host1, host2, 0.01, 10e6, 64 * 1024)
    engine.push_event(Event(0.5, flow1, EVENT_FLOW_START))
    
    engine.run()
    
    #engine.recorder.draw(engine.recorder.category['cate_link_rate']['l1'])
    #engine.recorder.draw(engine.recorder.category['cate_flow_rate']['f1'])
    #engine.recorder.draw(engine.recorder.category['cate_packet_delay']['f1'])
    #engine.recorder.draw(engine.recorder.category['cate_buffer_occupancy']['l1']) 
    engine.recorder.draw(engine.recorder.category['cate_packet_loss']['l1'])
    
    plt.show()

if __name__ == '__main__':
    main()
