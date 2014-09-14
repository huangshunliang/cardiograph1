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

    # Prepare our context and publisher
    context    = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://79.98.29.93:9092")
    subscriber.setsockopt(zmq.SUBSCRIBE, b"B")

    print("Entering main loop.")
    while True:
        # Read envelope with address
        [address, contents] = subscriber.recv_multipart()
        print("[%s] %s" % (address, contents))

    # We never get here but clean up anyhow
    subscriber.close()
    context.term()


if __name__ == "__main__":
    main()
