import nmap
import nmap3
from nmap3.nmapparser import NmapCommandParser
import shlex
import subprocess
from xml.etree import ElementTree as ET


def getOpenPorts(hosts, ports=None, arguments="-sV", sudo=False):
    """
    Scan by nmap given hosts and their ports

    :param hosts: string for hosts
    :param ports: string for ports
    :param arguments: string of arguments for nmap
    :param sudo: true if launch by sudo

    :return: scan result as dictionary
    """

    scanner = nmap.PortScanner()
    listHosts = scanner.scan(hosts=hosts, ports=ports, arguments=arguments, sudo=sudo)

    result_scan = {}

    for host, info in listHosts["scan"].items():
        result_scan[host] = {}
        result_scan[host]["name"] = info["hostnames"][0]["name"]
        result_scan[host]["tcp"] = {}
        if "tcp" in info:
            for p, port_info in info["tcp"].items():
                result_scan[host]["tcp"][p] = {}
                result_scan[host]["tcp"][p]["state"] = port_info["state"]
                result_scan[host]["tcp"][p]["service"] = port_info["name"]
                result_scan[host]["tcp"][p]["version"] = port_info["product"] + port_info["version"]
                result_scan[host]["tcp"][p]["extrainfo"] = port_info["extrainfo"]

    return result_scan



if __name__ == '__main__':

    resultScan = getOpenPorts("192.168.137.86", arguments="-sn", ports="-p-")
    print("next")


    print("temp")



    '''nm.command_line()  # get command line used for the scan : nmap -oX - -p 22-443 127.0.0.1
    nm.scaninfo()  # get nmap scan informations {'tcp': {'services': '22-443', 'method': 'connect'}}
    nm.all_hosts()  # get all hosts that were scanned
    nm['127.0.0.1'].hostname()  # get one hostname for host 127.0.0.1, usualy the user record
    nm['127.0.0.1'].hostnames()  # get list of hostnames for host 127.0.0.1 as a list of dict
    # [{'name':'hostname1', 'type':'PTR'}, {'name':'hostname2', 'type':'user'}]
    nm['127.0.0.1'].hostname()  # get hostname for host 127.0.0.1
    nm['127.0.0.1'].state()  # get state of host 127.0.0.1 (up|down|unknown|skipped)
    nm['127.0.0.1'].all_protocols()  # get all scanned protocols ['tcp', 'udp'] in (ip|tcp|udp|sctp)
    nm['127.0.0.1']['tcp'].keys()  # get all ports for tcp protocol
    nm['127.0.0.1'].all_tcp()  # get all ports for tcp protocol (sorted version)
    nm['127.0.0.1'].all_udp()  # get all ports for udp protocol (sorted version)
    nm['127.0.0.1'].all_ip()  # get all ports for ip protocol (sorted version)
    nm['127.0.0.1'].all_sctp()  # get all ports for sctp protocol (sorted version)
    nm['127.0.0.1'].has_tcp(22)  # is there any information for port 22/tcp on host 127.0.0.1
    nm['127.0.0.1']['tcp'][22]  # get infos about port 22 in tcp on host 127.0.0.1
    nm['127.0.0.1'].tcp(22)  # get infos about port 22 in tcp on host 127.0.0.1
    nm['127.0.0.1']['tcp'][22]['state']'''



