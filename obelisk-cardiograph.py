#!/usr/bin/env python

"""
obelisk-cardiograph
Monitor obelisk servers' heartbeat.
Author: Noel Maersk <veox ta wemakethings tod net>

Based on "Pubsub envelope subscriber" example from zguide
Author: Guillaume Aubert (gaubert) <guillaume(dot)aubert(at)gmail(dot)com>

"""


import zmq


serveraddresses = ['preacher.veox.pw:9092']


class Server:
    """
    """
    def __init__(self, zmqcontext, address = 'tcp://localhost:9092'):
        """
        """
        self.address = address
        self.socket = zmqcontext.socket(zmq.SUB)

    def connect(self, address = ''):
        """
        """
        if address == '':
            address = self.address
        self.socket.connect('tcp://' + address)
        self.socket.setsockopt(zmq.SUBSCRIBE, b'')

    def disconnect(self):
        """
        """
        self.socket.close()

    def get_address(self):
        """
        """
        return self.address

    def get_heartbeat(self):
        """
        """
        rawreply = self.socket.recv()
        reply = rawreply[::-1]  # obelisk sends little-endian
        return ':'.join(hex(x)[2:] for x in reply)


def main():
    """ main method """
    context = zmq.Context()
    servers = []
    for address in serveraddresses:
        server = Server(context, address)
        server.connect()
        servers.append(server)
        
    print("Entering main loop.")
    while True:
        for server in servers:
            print(server.get_address(), server.get_heartbeat())

    # We never get here but clean up anyhow
    for server in servers:
        server.disconnect()
    context.term()


if __name__ == "__main__":
    main()
