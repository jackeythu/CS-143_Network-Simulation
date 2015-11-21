from cs143_v1.events import * 
from cs143_v1.element_v2 import  *

def main():
        
        engine = SimEngine(30)
        
        host1 = Host(engine, 'h1', '192.168.0.1')   
        host2 = Host(engine, 'h2', '192.168.0.2')
        
        flow1 = Flow(engine, 'f1',host1,host2, 20)
        
        router1 = Router(engine, 'r1', '192.168.0.3')
        router2 = Router(engine, 'r2', '192.168.0.4')
        router3 = Router(engine, 'r3', '192.168.0.5')
        router4 = Router(engine, 'r4', '192.168.0.6')
    
        link0 = Link(engine, 'l0', host1, router1, 0.01, 10e6, 64e3)
        link1 = Link(engine, 'l1', router1, router2, 0.01, 10e6, 64e3)
        link2 = Link(engine, 'l2', router1, router3, 0.01, 10e6, 64e3)
        link3 = Link(engine, 'l3', router2, router4, 0.01, 10e6, 64e3)
        link4 = Link(engine, 'l4', router3, router4, 0.01, 10e6, 64e3)
        link5 = Link(engine, 'l5', host2, router4, 0.01, 10e6, 64e3)
        
        engine.push_event(Event(20, flow1, EVENT_FLOW_START))
        
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


if __name__ == '__main__':
    main()
