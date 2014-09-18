#!/usr/bin/env python

"""
obelisk-cardiograph
Script to monitor obelisk servers' heartbeat.
Author: Noel Maersk <veox ta wemakethings tod net>
License: Affero GNU GPLv3 (see LICENSE).

A few examples from `zguide` were used, see:
https://github.com/imatix/zguide

"""


import zmq


# This list is necessarily over 72 characters wide.
serverlist = [{'address': 'tcp://obelisk.coinkite.com:9092', 'network': 'bitcoin'},
              {'address': 'tcp://preacher.veox.pw:9092', 'network': 'bitcoin-testnet'}]


class Server(object):
    """
    """
    def __init__(self, zmqcontext, properties):
        """
        """
        # Consider using an initialiser wrapper as in
        # https://stackoverflow.com/questions/1389180
        # if the property list gets too long.
        # Alternatively, find if there's a lib way to do it.
        self._address = properties['address']
        self._network = properties['network']
        self.socket = zmqcontext.socket(zmq.SUB)

    @property
    def address(self):
        """tcp://<server-address>:<port>"""
        return self._address

    @address.setter
    def address(self, value):
        self._address = value

    @property
    def network(self):
        """Human-readable string description of the P2P network."""
        return self._network

    @network.setter
    def network(self, value):
        self._network = value

    def receive_heartbeat(self):
        """
        """
        rawreply = self.socket.recv()
        reply = rawreply[::-1]  # obelisk sends little-endian
        return ':'.join(hex(x)[2:] for x in reply)

    def connect(self, address = None):
        """
        """
        if address == None:
            address = self._address
        self.socket.connect(address)
        self.socket.setsockopt(zmq.SUBSCRIBE, b'')

    def disconnect(self):
        """
        """
        self.socket.close()


def main():
    """ main method """
    context = zmq.Context()
    servers = []
    for i in serverlist:
        server = Server(context, i)
        server.connect()
        servers.append(server)
        
    print("Entering main loop.")
    while True:
        for server in servers:
            print(server.network, server.address,
                  server.receive_heartbeat())

    # We never get here but clean up anyhow
    for server in servers:
        server.disconnect()
    context.term()


if __name__ == "__main__":
    main()
