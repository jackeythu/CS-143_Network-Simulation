from cs143_v1.events import * 
from cs143_v1.element import  *

def main():
        
        engine = SimEngine(20)
        
        host1 = Host(engine, 'h1', '192.168.0.1')
        
        host2 = Host(engine, 'h2', '192.168.0.2')
        flow1 = Flow(engine, 'f1',host1,host2, 20)
    
        link1 = Link(engine, 'l1', host1, host2, 0.01, 10e6, 64e3)
        engine.push_event(Event(0, flow1, EVENT_FLOW_START))
        
        engine.run()


if __name__ == '__main__':
    main()
