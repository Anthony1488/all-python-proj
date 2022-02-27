#!/usr/bin venv python3
import netfilterqueue
import scapy.all as scapy
import argparse


def process_packet(packet):
 print(packet)
 packet.drop()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()

