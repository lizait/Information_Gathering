import sys
import os
import re
import ast


def cmdline(target):
    cmd = "fierce --domain " + target
    stream = os.popen(cmd)
    output = stream.read()

    if not output:
        cmd = "python3 ~/fierce/fierce/fierce.py --domain " + target
        stream = os.popen(cmd)
        output = stream.read()
    return output


def getNS(output):
    result = re.search('NS:(.*?)\nSOA', output, re.DOTALL)
    NS = result.group(1)
    return NS


def getSOA(output):
    result = re.search('SOA:(.*?)\nZone', output, re.DOTALL)
    SOA = result.group(1)
    return SOA


def getzoneRes(output):
    zone = re.search('Zone:(.*?)\nWildcard''|''Zone:(.*?)\}' , output, re.DOTALL)
    zone = zone.group(1)
    return zone


def getZone(output):
    zone = getzoneRes(output)
    if zone ==' failure':
        return zone
    else:
        zone = 'success'
        getTransferzone (output)
        return zone


def getTransferzone(output):

    res = re.search('Zone: success\n{(.*)\}', output, re.DOTALL)
    zone = res.group(1)

    try :
        f = open("/home/zonetransfer.txt", "w+")
        f.write(zone)
        f.close()

    except PermissionError:
        print("please check your premission directory ")
        f = open("zonetransfer.txt,", "w+")
        f.write(zone)
        f.close()


def getwildcard(output):
    result = re.search('Wildcard:(.*?)\nFound', output, re.DOTALL)
    wildcard = result.group(1)
    return wildcard


def getsubdomains(output):
    list_sub = re.findall("Found:(.*) \)", output)
    return list_sub


def parsesubdomains(list_sub):
    subdomains = []
    for sub in list_sub:
        dict_sub = {}
        key, value = sub.split('(')
        dict_sub[key] = value
        subdomains.append(dict_sub)
    return subdomains


def getiprange(output):
    list_sub = re.findall("Nearby:(.*?)\}", output, re.DOTALL)
    return list_sub


def parselistrange(list_sub):
    list = []
    for sub in list_sub:
        sub = sub + '}'
        list.append(sub.replace("\n", ""))
    return list


def strtodict(list_sub):
    list_dict = []
    for i in list_sub:
        s = ast.literal_eval(i)
        list_dict.append(s)
    return list_dict


def dnsenum(target):
    dict = {}
    output = cmdline(target)
    dict["serveur DNS"] = getNS(output)
    dict["serveur maitre"] = getSOA(output)
    dict["Zone"] = getZone(output)
    try:
        dict["wildcard"] = getwildcard(output)
        list_sub = getsubdomains(output)
        domains = parsesubdomains(list_sub)
        dict['hosts found'] = domains
        iprange = getiprange(output)
        listrange = parselistrange(iprange)
        dictrange = strtodict(listrange)
        dict['ip range'] = dictrange
    except:
        dict["wildcard"] = 'none'
        dict['hosts found'] = 'none'
        dict['ip range'] = 'none'

    return dict


print (dnsenum ("ZoneTransfer.me"))




