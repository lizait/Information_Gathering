import socket
import ipaddress
from netaddr import valid_ipv4
import os


def whoisIP (target):
    stream = os.popen('whois '+target)
    output = stream.read()
    return output

def whoisDomain (target) :
    stream = os.popen('whois ' + target)
    output = stream.read()
    return output


def listtodict (str):
    list = (str).split("\n")
    list = [i for i in list if i[:1] != '%']
    list = [i for i in list if i[:1] != '#']
    list = [i for i in list if i != '']
    print (list)
    dict = {}
    for i in list:
        key, value = i.split(":",1)
        value = value.strip()
        dict[key] = value
    return dict


def new_whois (target) :
    if (target[0].isdigit()) :
        try :
            assert (valid_ipv4(target)), "invalid IP ! pleasse retry"
            query = whoisIP(target)
            ip_dict = listtodict(query)
            return  ip_dict
        except AssertionError as error :
            print (error)
    else:
        try:
            if (socket.gethostbyname(target)) :
                 query = whoisDomain(target)
                 domain_dict = listtodict(query)
            return domain_dict
        except socket.gaierror:
            print ("invalid domain name\nplease retry !")


print (new_whois("eni.fr"))
