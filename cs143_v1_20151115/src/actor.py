"""This module contains all actor definitions.
   autosummary::
    Actor
    Buffer
    Flow
    Host
    Link
    Router

"""
from Queue import Queue

ACK_PACKET_SIZE = 512
GENERATE_ROUTER_PACKET_DEFAULT_INTERVAL = 1000
"""Time for every :class:`.Router` to wait before generating a new
:class:`.RouterPacket`, in milliseconds"""
PACKET_SIZE = 8192
DYNAMIC_ROUTE_DISTANCE_METRIC = True


from cs143_v1.events import LinkAvailable
from cs143_v1.events import PacketReceipt
from cs143_v1.events import RoutingTableOutdated

#from cs143sim.tla import TCPTahoe
#from cs143sim.tla import TCPVegas


class Actor(object):
    """Representation of an actor
    
    The superclass of all actors defining environment variables.
    :param env: SimPy simulation :class:`~simpy.core.Environment`
    :param str name: name from input file
    :ivar env: SimPy simulation :class:`~simpy.core.Environment`
    :ivar str name: name from input file
    """
    def __init__(self, env, name=None):
        self.env = env
        self.name = name

class Packet(object):
    """Representation of a quantum of information
    Packets carry information along the network, between :class:`Hosts <.Host>`
    or :class:`Routers <.Router>`.
    :param destination: destination :class:`.Host` or :class:`.Router`
    :param source: source :class:`.Host` or :class:`.Router`
    :param str timestamp: time at which the packet was created
    :ivar destination: destination :class:`.Host` or :class:`.Router`
    :ivar source: source :class:`.Host` or :class:`.Router`
    :ivar float timestamp: time at which the packet was created
    :ivar int size: size of the packet
    """
    def __init__(self, destination, source, timestamp):
        self.timestamp = timestamp
        self.source = source
        self.destination = destination
        self.size = PACKET_SIZE


class DataPacket(Packet):
    """A packet used for transferring data
    
    DataPackets transmit data along the network, between :class:`Hosts <.Host>`
    or :class:`Routers <.Router>`.
    :param destination: destination :class:`.Host` or :class:`.Router`
    :param source: source :class:`.Host` or :class:`.Router`
    :param float timestamp: time at which the packet was created
    :param bool acknowledgement: indicate whether the packet is an AckPacket
    :param int number: the number of the packet in a flow
    :ivar int number: the number of the packet in a flow
    :ivar bool acknowledgement: indicate whether the packet is an AckPacket
    """
    def __init__(self, destination, source, timestamp, acknowledgement, number):
        super(DataPacket, self).__init__(timestamp=timestamp, source=source,
                                         destination=destination)
        self.number = number
        self.acknowledgement = acknowledgement


class RouterPacket(Packet):
    """A packet used to update routing tables
    
    RouterPackets carry information of routing tables along the network, between :class:`Routers <.Router>`.
    :param source: source :class:`.Host` or :class:`.Router`
    :param float timestamp: time at which the packet was created
    :param dict router_table: the routing table
    :param bool acknowledgement: indicate whether the packet is an AckPacket
    :ivar dict router_table: the routing table of the RouterPacket
    :ivar int number: the number of the RouterPacket, which is always 0
    :ivar bool acknowledgement: indicate whether the packet is an AckPacket
    """
    def __init__(self, source, timestamp, router_table, acknowledgement):
        # TODO: define router_table in docstring
        super(RouterPacket, self).__init__(timestamp=timestamp, source=source,
                                           destination=0)
        self.router_table = router_table
        self.number = 0
        self.acknowledgement = acknowledgement


class Buffer(Actor):
    """Representation of a data storage container
    Buffers store data to be linked while :class:`.Link` is busy sending data.
    :param int capacity: maximum number of bits that can be stored
    :param link: :class:`.Link` containing this buffer
    :ivar int capacity: maximum number of bits that can be stored
    :ivar link: :class:`.Link` containing this buffer
    :ivar list packets: :class:`Packets <.Packet>` currently in storage
    :ivar int current_level: the current occupancy of the buffer
    """
    def __init__(self, env, capacity, link):
        super(Buffer, self).__init__(env=env)
        self.link = link
        self.packets = Queue()
        self.capacity = capacity
        self.current_level = 0

    def add(self, packet):
        """Adds packet to `packets` if `capacity` will not be exceeded,
        drops packet if buffer if full.
        :param packet: :class:`.Packet` added to buffer.
        """
        if self.current_level + packet.size <= self.capacity:
            self.packets.put(packet)
            self.current_level = self.current_level + packet.size
            self.env.controller.record_buffer_occupancy(link=self.link,
                                                        buffer_occupancy=self.current_level)
            return True
        else:
            # The packet cannot be stored, so the packet is dropped
            self.env.controller.record_packet_loss(link=self.link)
            self.env.controller.record_buffer_occupancy(link=self.link,
                                                        buffer_occupancy=self.current_level)
            return False
                    
    def get(self, timeout=None):
        """Link get a packet from its buffer.
        
        :param timeout
        """
        packet = self.packets.get(timeout=timeout)
        self.current_level = self.current_level - packet.size
        self.env.controller.record_buffer_occupancy(link=self.link,
                                                    buffer_occupancy=self.current_level)
        return packet


class Flow(Actor):
    """Representation of a connection between access points
    Flows try to transmit data from :class:`.Host` to :class:`.Host`.
    :param source: source :class:`.Host`
    :param destination: destination :class:`.Host`
    :param float amount: amount of data to transmit
    :param int algorithm: indicate which tla this flow is using
    :ivar source: source :class:`.Host`
    :ivar destination: destination :class:`.Host`
    :ivar float amount: amount of data to transmit
    :ivar int algorithm: indicate which tla this flow is using
    :ivar rcv_expect_to_receive: next packet expect to receive
    :ivar rcv_received_packets:  list of packets that have been received, but not what we need now.
    """
    def __init__(self, env, name, source, destination, amount, algorithm=0):
        super(Flow, self).__init__(env=env, name=name)
        self.source = source
        self.destination = destination
        self.amount = amount
        '''
        if algorithm == 0:
            self.tla = TCPTahoe(env=self.env, flow=self)
            self.tla.enable_fast_recovery = False
            self.tla.enable_fast_retransmit = False
        elif algorithm == 1:
            self.tla = TCPTahoe(env=self.env, flow=self)
            self.tla.enable_fast_recovery = False
            self.tla.enable_fast_retransmit = True
        elif algorithm == 2:
            self.tla = TCPTahoe(env=self.env, flow=self)
            self.tla.enable_fast_recovery = True
            self.tla.enable_fast_retransmit = False
        elif algorithm == 3:
            self.tla = TCPVegas(env=self.env, flow=self)
            self.tla.enable_fast = False
        else:
            self.tla = TCPVegas(env=self.env, flow=self)
            self.tla.enable_fast = True
        '''
        self.rcv_expect_to_receive = 0
        self.rcv_received_packets = list()

    def __str__(self):
        return ('Flow from ' + self.source.address +
                ' to ' + self.destination.address)

    def make_packet(self, packet_number):
        """
        Make a packet based on the packet number
        """

        packet = DataPacket(number=packet_number,
                            acknowledgement=False, timestamp=self.env.now,
                            source=self.source, destination=self.destination)
        packet.size = PACKET_SIZE
        return packet
        
    def make_ack_packet(self, packet):
        """Make an ack packet
        """
        # Go Back N version, compatible with stop and wait
        n = packet.number
        if n < self.rcv_expect_to_receive:
            # This packet has been received before
            pass
        elif n == self.rcv_expect_to_receive:
            # This packet is what we expect to receive
            # Find out next packet expect to receive
            self.rcv_expect_to_receive += 1
            flag = True
            while flag:
                for x in self.rcv_received_packets:
                    if x == self.rcv_expect_to_receive:
                        self.rcv_expect_to_receive += 1
                        continue
                flag = False
        else:
            # This packet is not what we expect to receive
            # Store it
            self.rcv_received_packets.append(n)
        # using the timestamp of packet to be acked as the timestamp of ack packet
        # to calculate RTT
        ack_packet = DataPacket(number=self.rcv_expect_to_receive,
                                acknowledgement=True, timestamp=packet.timestamp,
                                source=packet.destination, destination=packet.source)
        ack_packet.size = ACK_PACKET_SIZE
        return ack_packet

    def send_packet(self, packet):
        """When possible, TLA use this method to send a packet
        """
        if packet.acknowledgement:
            self.destination.send(packet)
        else:
            self.source.send(packet)
        
    def react_to_packet_receipt(self, event):
        packet = event.value
        # If the packet is a data packet, generate an ack packet
        if not packet.acknowledgement:
            ack_packet = self.make_ack_packet(packet)
            self.send_packet(ack_packet)
            self.env.controller.record_flow_rate(flow=self, packet_size=packet.size)
        packet_delay = self.env.now - packet.timestamp
        self.env.controller.record_packet_delay(flow=self, packet_delay=packet_delay)
        if packet.acknowledgement:
            self.tla.react_to_ack(packet)
        print 'Reactor: [{}] is reacting to event [{}]'.format(self.name, 'PacketReceive')

    def time_out(self, timeout_packet_number):
        """When time out happens, run TLA
        Time_out timers should be reset if a the ack arrive
        """
        self.tla.react_to_time_out(timeout_packet_number)
        print 'Reactor: [{}] is reacting to event [{}]'.format(self.name, 'TimeOut')

    def react_to_flow_start(self, event):
        self.tla.react_to_flow_start(event=event)
        print 'Reactor: [{}] is reacting to event [{}]'.format(self.name, 'FlowStart')
    

class Host(Actor):
    """Representation of an access point
    Hosts send :class:`Packets <.Packet>` through a :class:`.Link` to a
    :class:`.Router` or to another :class:`.Host`.
    :param str address: IP address
    :ivar str address: IP address
    :ivar list flows: :class:`Flows <.Flow>` on this :class:`.Host`
    :ivar link: :class:`Link` connected to this :class:`.Host`
    """
    def __init__(self, env, name, address):
        super(Host, self).__init__(env=env, name=name)
        self.address = address
        self.flows = []
        self.link = None

    def __str__(self):
        return 'Host at ' + self.address

    def send(self, packet):
        self.link.add(packet)

    def react_to_packet_receipt(self, event):
        packet = event.value
        if packet.destination == self:
            if isinstance(packet, DataPacket):
                for f in self.flows:
                    if packet.acknowledgement:
                        if packet.source == f.destination and packet.destination == f.source:
                            f.react_to_packet_receipt(event=event)
                    else:
                        if packet.source == f.source and packet.destination == f.destination:
                            f.react_to_packet_receipt(event=event)
        print 'Reactor: [{}] is reacting to event [{}]'.format(self.name, 'PacketReceive')


class Link(Actor):
    """Representation of a physical link between access points or routers
    Links carry packets from one end to the other.
    :param source: source :class:`.Host` or :class:`.Router`
    :param destination: destination :class:`.Host` or :class:`.Router`
    :param float delay: amount of time required to transmit a :class:`.Packet`
    :param float rate: speed of removing data from source
    :param int buffer_capacity: :class:`.Buffer` capacity in bits
    :ivar source: source :class:`.Host` or :class:`.Router`
    :ivar destination: destination :class:`.Host` or :class:`.Router`
    :ivar float delay: amount of time required to transmit a :class:`.Packet`
    :ivar float rate: speed of removing data from source
    :ivar list buffer: :class:`Packets <.Packet>` currently in transmission
    :ivar bool busy: whether currently removing data from source
    :ivar float utilization: fraction of capacity in use
    """
    def __init__(self, env, name, source, destination, delay, rate, buffer_capacity):
        super(Link, self).__init__(env=env, name=name)
        self.source = source
        self.destination = destination
        self.delay = delay
        self.rate = rate
        self.buffer = Buffer(env=env, capacity=buffer_capacity, link=self)
        self.busy = False
        self.utilization = 0
        self.env = env

    def __str__(self):
        return ('Link from ' + self.source.address +
                ' to ' + self.destination.address)

    def add(self, packet):
        if self.busy:
            self.buffer.add(packet)
        else:
            self.send(packet)

    def react_to_link_available(self, event):
        self.busy = False
        if not self.buffer.packets.empty():
            self.send(self.buffer.get())
        print 'Reactor: [{}] is reacting to event [{}]'.format(self.name, 'LinkAvailable')

    def send(self, packet):
        self.busy = True
        d_trans = 1.0 * packet.size / self.rate  # (bits to be tx'ed)/(rate in bits/ms) should give the
        # transit time in ms
        PacketReceipt(env=self.env, delay=self.delay + d_trans, receiver=self.destination, packet=packet)
        LinkAvailable(env=self.env, delay=d_trans, link=self)
        self.env.controller.record_link_rate(link=self, packet_size=packet.size)


class Router(Actor):
    """Representation of a router
    Routers route packets through the network to their destination Hosts.
    :param str address: IP address for router
    :param list links: all connected Links
    :param float update_time: the time interval of updating routing tables
    :ivar str address: IP address for router
    :ivar list links: all connected Links
    :ivar dict table: routing table
    :ivar default_gateway: default out port if can not decide route
    :ivar float update_time: the time interval of updating routing tables
    """
    def __init__(self, env, name, address, update_time=GENERATE_ROUTER_PACKET_DEFAULT_INTERVAL):
        super(Router, self).__init__(env=env, name=name)
        self.address = address
        self.links = []
        self.table = {}
        self.default_gateway = None
        self.update_time = update_time

    def __str__(self):
        return self.address
  
    def initialize_routing_table(self, all_host_ip_addresses):
        """
        the key of table is destination (IP_address of hosts)
        the first element in value of table is the distance between current router to final host
        the second element in value of table is where to go for next hop
        If the host destination is not in neighbor links, then set the distance to be inf, the next_hop to be the default_gateway
        If the host destination is in its neighbor links, then set the distance to be 1( dynamic still inf?), the next_hop to be direct host destination
        """
        self.default_gateway = self.links[0].destination.address
        for host_ip_address in all_host_ip_addresses:
            val = float("inf"), self.default_gateway
            self.table[host_ip_address] = val
        for link in self.links:
            if isinstance(link.destination, Host):
                val = 1, link.destination.address
                self.table[link.destination.address] = val
        self.generate_router_packet()
    
    def update_router_table(self, router_packet):
        """Check every item in router table if any update
        Implement Bellman-Ford algorithm here.
        Measurement is number of hops if DYNAMIC_ROUTE_DISTANCE_METRIC = False.
        Measurement is link delay if DYNAMIC_ROUTE_DISTANCE_METRIC = True.
        """
        for (destination, val) in router_packet.router_table.items():
            if DYNAMIC_ROUTE_DISTANCE_METRIC:
                metric = self.env.now - router_packet.timestamp
                if destination in self.table:
                    if self.table[destination][1] == router_packet.source.address:
                        update_val = val[0] + metric, router_packet.source.address
                        self.table[destination] = update_val
                    else:
                        if val[0] + metric < self.table[destination][0]:
                            update_val = val[0] + metric, router_packet.source.address
                            self.table[destination] = update_val
                else:
                    update_val = val[0] + metric, router_packet.source.address
                    self.table[destination] = update_val
            else:
                metric = 1
                if destination in self.table:
                    if val[0] + metric < self.table[destination][0]:
                        update_val = val[0] + metric, router_packet.source.address
                        self.table[destination] = update_val
                else:
                    update_val = val[0] + metric, router_packet.source.address
                    self.table[destination] = update_val

    def generate_router_packet(self):
        """Design RouterPacket(source,timestamp,routertable) that send the whole router table of this router to communicate with its neighbor
        """
        for l in self.links:
            if isinstance(l.destination, Router):
                router_packet = RouterPacket(timestamp=self.env.now, router_table=self.table, source=self, acknowledgement=False)
                self.send(link=l, packet=router_packet)

    def generate_ack_router_packet(self, router_packet):
        source_packet = router_packet
        ack_router_packet = RouterPacket(timestamp=source_packet.timestamp, router_table=self.table, source=self, acknowledgement=True)
        for l in self.links:
            if l.destination == router_packet.source:
                self.send(link=l, packet=ack_router_packet)
                break

    def map_route(self, packet):
        if packet.destination.address in self.table:
            next_hop = self.table[packet.destination.address][1]
            for link in self.links:
                if next_hop == link.destination.address:
                    route_link = link
                    break
            self.send(link=route_link, packet=packet)
        else:
            self.send(link=self.links[0], packet=packet)

    def react_to_packet_receipt(self, event):
        """Read packet head to tell whether is a DataPacket or a RouterPacket
        If it is normal packet, call map_route function
        If it is update_RT_communication packet, call update_router_table function
        """
        packet = event.value
        if isinstance(packet, DataPacket):
            self.map_route(packet=packet)
        elif isinstance(packet, RouterPacket):
            if not packet.acknowledgement:
                self.generate_ack_router_packet(router_packet=packet)
            else:   
                self.update_router_table(router_packet=packet)
        print 'Reactor: [{}] is reacting to event [{}]'.format(self.name, 'PacketReceive')

    def send(self, link, packet):
        """Send packet to certain link
        The packet could be normal packet to forward or communication packet to send to all links.
        """
        link.add(packet=packet)

    def react_to_routing_table_outdated(self, event):
        """Periodically generate RouterPacket to all neighbor links.
        """
        self.generate_router_packet()
        RoutingTableOutdated(env=self.env, delay=self.update_time, router=self)
        print 'Reactor: [{}] is reacting to event [{}]'.format(self.name, 'RoutingTableOutdated')