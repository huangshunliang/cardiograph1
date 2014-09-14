#!/usr/bin/env python

"""
obelisk-cardiograph
Monitor obelisk servers' heartbeat.
Author: Noel Maersk <veox ta wemakethings tod net>

Based on "Pubsub envelope subscriber" example from zguide
Author: Guillaume Aubert (gaubert) <guillaume(dot)aubert(at)gmail(dot)com>

"""


import zmq


def main():
    """ main method """

    servers = ['preacher.veox.pw:9092']

    context = zmq.Context()
    s = context.socket(zmq.SUB)
    s.connect('tcp://' + servers[0])
    s.setsockopt(zmq.SUBSCRIBE, b'')    # subscribe to everything

    print("Entering main loop.")
    while True:
        reply = s.recv()
        reply = reply[::-1] # obelisk sent little-endian
        data = ':'.join(hex(x)[2:] for x in reply)
        print(servers[0], data)

    # We never get here but clean up anyhow
    s.close()
    context.term()


if __name__ == "__main__":
    main()
