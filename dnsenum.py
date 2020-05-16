import os
import re
import ast


def cmdline(target):
    cmd = "fierce --domain  "+target
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
    zone = re.search('Zone:(.*?)\nWildcard''|''Zone:(.*?)\}', output, re.DOTALL)
    zone = zone.group(1)
    return zone


def getZone(output):
    zone = getzoneRes(output)
    if zone == ' failure':
        return False
    else:
        zone = 'success'
        return True


def getTransferzone(output):

    res = re.search('Zone: success\n{(.*)\}', output, re.DOTALL)
    zone = res.group(1)
    zone = zone.split("',")

    nameAndInfosDict = {}
    for dnsName in zone:
        name = re.search('<DNS name (.*?)>', dnsName, re.DOTALL).group(1)

        infos = dnsName[dnsName.find("'"):]
        infos = infos.split("'\n")

        cleanInfos = []
        for element in infos:
            element = element.strip()
            if element.startswith("'"):
                element = element[1:]
            element = element.replace("\\n", "")
            cleanInfos.append(element)

        nameAndInfosDict[name] = cleanInfos
        
    return nameAndInfosDict


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
    fierceResultParse = {}
    output = cmdline(target)
    fierceResultParse["serveur DNS"] = getNS(output)
    fierceResultParse["serveur maitre"] = getSOA(output)
    fierceResultParse["Zone"] = getZone(output)
    try:
        fierceResultParse["ZoneInfos"] = getTransferzone(output)
        fierceResultParse["wildcard"] = getwildcard(output)
        list_sub = getsubdomains(output)
        domains = parsesubdomains(list_sub)
        fierceResultParse['hosts found'] = domains
        iprange = getiprange(output)
        listrange = parselistrange(iprange)
        dictrange = strtodict(listrange)
        fierceResultParse['ip range'] = dictrange
    except:
        fierceResultParse["wildcard"] = None
        fierceResultParse['hosts found'] = None
        fierceResultParse['ip range'] = None

    return fierceResultParse


if __name__ == '__main__':
    print(dnsenum("zonetransfer.me"))
    print(dnsenum("pcnerds.co.za"))




