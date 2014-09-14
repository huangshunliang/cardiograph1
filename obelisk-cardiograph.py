#!/usr/bin/env python

"""
    obelisk-cardiograph
    Monitor obelisk servers' heartbeat.

    Based on "Pubsub envelope subscriber" example from zguide
    Author: Guillaume Aubert (gaubert) <guillaume(dot)aubert(at)gmail(dot)com>

"""
import zmq

def main():
    """ main method """

    serverip = '79.98.29.93'
    serverport = '9092'

    ctx = zmq.Context()
    s = ctx.socket(zmq.SUB)
    s.connect('tcp://' + serverip + ':' + serverport)
    s.setsockopt(zmq.SUBSCRIBE, b'')    # subscribe to everything

    print("Entering main loop.")
    while True:
        reply = s.recv()
        reply = reply[::-1] # obelisk sent little-endian
        data = ':'.join(hex(x)[2:] for x in reply)
        print(serverip, data)

    # We never get here but clean up anyhow
    s.close()
    ctx.term()


if __name__ == "__main__":
    main()
