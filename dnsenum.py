import sys
import os
import re
import ast


def cmdline(target):
    cmd = "fierce --domain  "+target
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

def getZone (output) :
    zone = getzoneRes(output)
    if (zone ==' failure'):
        return zone
    else:
        zone = 'success'
        getTransferzone (output)
        return zone



def getTransferzone (output) :

    res = re.search('Zone: success\n{(.*)\}', output, re.DOTALL)
    zone = res.group(1)
'''''''''
    try :
        f = open("/home/zonetransfer.txt", "w+")
        f.write(zone)
        f.close()
        return zone

    except PermissionError :
        print ("please check your premission directory ")
        f = open("zonetransfer.txt,", "w+")
        f.write(zone)
        f.close()
'''''''''''

def getZoneTransferDetails (zone) :
    dict = {}
    value1 = re.search('<DNS name @>:(.*?)<DNS name _acme-challenge>', zone, re.DOTALL)
    value1 = value1.group(1)
    list1 = value1.split("\\n")
    dict['@'] = list1

    acme_challenge = re.search('<DNS name _acme-challenge>:(.*?)<DNS name _sip._tcp>', zone, re.DOTALL)
    acme_challenge = acme_challenge.group(1)
    list2 = acme_challenge.split("\\n")
    dict['_acme-challenge'] = list2

    sip_tcp = re.search('<DNS name _sip._tcp>:(.*?)<DNS name asfdbauthdns>', zone, re.DOTALL)
    sip_tcp = sip_tcp.group(1)
    list3 = sip_tcp.split("\\n")
    dict['_sip._tcp'] = list3

    asfdbauthdns = re.search('<DNS name asfdbauthdns>:(.*?)<DNS name asfdbbox>', zone, re.DOTALL)
    asfdbauthdns = asfdbauthdns.group(1)
    list4 = asfdbauthdns.split("\\n")
    dict['asfdbauthdns'] = list4

    asfdbbox = re.search('<DNS name asfdbbox>:(.*?)<DNS name asfdbvolume>', zone, re.DOTALL)
    asfdbbox = asfdbbox.group(1)
    list5 = asfdbbox.split("\\n")
    dict['asfdbbox'] = list5

    asfdbvolume = re.search('<DNS name asfdbvolume>:(.*?)<DNS name canberra-office>', zone, re.DOTALL)
    asfdbvolume = asfdbvolume.group(1)
    list6 = asfdbvolume.split("\\n")
    dict['asfdbvolume'] = list6

    canberra_office = re.search('<DNS name canberra-office>:(.*?)<DNS name cmdexec>', zone, re.DOTALL)
    canberra_office = canberra_office.group(1)
    list7 = canberra_office.split("\\n")
    dict['canberra-office'] = list7

    cmdexec = re.search('<DNS name cmdexec>:(.*?)<DNS name contact>', zone, re.DOTALL)
    cmdexec = cmdexec.group(1)
    list8 = cmdexec.split("\\n")
    dict['cmdexec'] = list8

    contact = re.search('<DNS name contact>:(.*?)<DNS name dc-office>', zone, re.DOTALL)
    contact = contact.group(1)
    list9 = contact.split("\\n")
    dict['contact'] = list9

    dc_office = re.search('<DNS name dc-office>:(.*?)<DNS name deadbeef>', zone, re.DOTALL)
    dc_office = dc_office.group(1)
    list10 = dc_office.split("\\n")
    dict['dc-office'] = list10

    deadbeef = re.search('<DNS name deadbeef>:(.*?)<DNS name dr>', zone, re.DOTALL)
    deadbeef = deadbeef.group(1)
    list11 = deadbeef.split("\\n")
    dict['deadbeef'] = list11

    dr = re.search('<DNS name dr>:(.*?)<DNS name DZC>', zone, re.DOTALL)
    dr = dr.group(1)
    list12 = dr.split("\\n")
    dict['dr'] = list12

    DZC = re.search('<DNS name DZC>:(.*?)<DNS name email>', zone, re.DOTALL)
    DZC = DZC.group(1)
    list13 = DZC.split("\\n")
    dict['DZC'] = list13

    email = re.search('<DNS name email>:(.*?)<DNS name Hello>', zone, re.DOTALL)
    email = email.group(1)
    list14 = email.split("\\n")
    dict['email'] = list14

    Hello = re.search('<DNS name Hello>:(.*?)<DNS name home>', zone, re.DOTALL)
    Hello = Hello.group(1)
    list15 = Hello.split("\\n")
    dict['Hello'] = list15

    home = re.search('<DNS name home>:(.*?)<DNS name Info>', zone, re.DOTALL)
    home = home.group(1)
    list16 = home.split("\\n")
    dict['home'] = list16

    Info = re.search('<DNS name Info>:(.*?)<DNS name internal>', zone, re.DOTALL)
    Info = Info.group(1)
    list17 = Info.split("\\n")
    dict['Info'] = list17

    internal = re.search('<DNS name internal>:(.*?)<DNS name intns1>', zone, re.DOTALL)
    internal = internal.group(1)
    list18 = internal.split("\\n")
    dict['internl'] = list18

    intns1 = re.search('<DNS name intns1>:(.*?)<DNS name intns2>', zone, re.DOTALL)
    intns1 = intns1.group(1)
    list19 = intns1.split("\\n")
    dict['intns1'] = list19

    intns2 = re.search('<DNS name intns2>:(.*?)<DNS name office>', zone, re.DOTALL)
    intns2 = intns2.group(1)
    list20 = intns2.split("\\n")
    dict['intns2'] = list20

    office = re.search('<DNS name office>:(.*?)<DNS name ipv6actnow.org>', zone, re.DOTALL)
    office = office.group(1)
    list21 = office.split("\\n")
    dict['office'] = list21

    ipv6actnow = re.search('<DNS name ipv6actnow.org>:(.*?)<DNS name owa>', zone, re.DOTALL)
    ipv6actnow = ipv6actnow.group(1)
    list22 = ipv6actnow.split("\\n")
    dict['ipv6actnow'] = list22

    owa = re.search('<DNS name owa>:(.*?)<DNS name robinwood>', zone, re.DOTALL)
    owa = owa.group(1)
    list23 = owa.split("\\n")
    dict['owa'] = list23

    robinwood = re.search('<DNS name robinwood>:(.*?)<DNS name rp>', zone, re.DOTALL)
    robinwood = robinwood.group(1)
    list24 = robinwood.split("\\n")
    dict['robinwood'] = list24

    rp = re.search('<DNS name rp>:(.*?)<DNS name sip>', zone, re.DOTALL)
    rp = rp.group(1)
    list25 = rp.split("\\n")
    dict['rp'] = list25

    sip = re.search('<DNS name sip>:(.*?)<DNS name sqli>', zone, re.DOTALL)
    sip = sip.group(1)
    list26 = sip.split("\\n")
    dict['sip'] = list26

    sqli = re.search('<DNS name sqli>:(.*?)<DNS name sshock>', zone, re.DOTALL)
    sqli = sqli.group(1)
    list27 = sqli.split("\\n")
    dict['sqli'] = list27

    sshock = re.search('<DNS name sshock>:(.*?)<DNS name staging>', zone, re.DOTALL)
    sshock = sshock.group(1)
    list28 = sshock.split("\\n")
    dict['sshock'] = list28

    staging = re.search('<DNS name staging>:(.*?)<DNS name alltcpportsopen.firewall.test>', zone, re.DOTALL)
    staging = staging.group(1)
    list29 = staging.split("\\n")
    dict['staging'] = list29

    firewall = re.search('<DNS name alltcpportsopen.firewall.test>:(.*?)<DNS name testing>', zone, re.DOTALL)
    firewall = firewall.group(1)
    list30 = firewall.split("\\n")
    dict['alltcpportsopen.firewall.test'] = list30

    testing = re.search('<DNS name testing>:(.*?)<DNS name vpn>', zone, re.DOTALL)
    testing = testing.group(1)
    list31 = testing.split("\\n")
    dict['testing'] = list31

    vpn = re.search('<DNS name vpn>:(.*?)<DNS name www>', zone, re.DOTALL)
    vpn = vpn.group(1)
    list32 = vpn.split("\\n")
    dict['vpn'] = list32

    www_ = re.search('<DNS name www>:(.*?)<DNS name xss>', zone, re.DOTALL)
    www_ = www_.group(1)
    list33 = www_.split("\\n")
    dict['www'] = list33

    xss = re.search('<DNS name xss>:(.*?)}', zone, re.DOTALL)
    xss = xss.group(1)
    list34 = xss.split("\\n")
    dict['xss'] = list34
    return dict


def getwildcard(output):
    result = re.search('Wildcard:(.*?)\nFound', output,re.DOTALL)
    wildcard = result.group(1)
    return wildcard


def getsubdomains (output) :
    list_sub = re.findall("Found:(.*) \)", output)
    return list_sub


def parsesubdomains (list_sub) :
    subdomains = []
    for sub in list_sub :
        dict_sub = {}
        key,value = sub.split ('(')
        dict_sub[key] = value
        subdomains.append(dict_sub)
    return subdomains

def getiprange (output) :
    list_sub = re.findall("Nearby:(.*?)\}", output, re.DOTALL)
    return list_sub

def parselistrange (list_sub) :
    list = []
    for sub in list_sub:
        sub = sub + '}'
        list.append(sub.replace("\n", ""))
    return list

def strtodict (list_sub) :
    list_dict = []
    for i in list_sub:
        s = ast.literal_eval(i)
        list_dict.append(s)
    return list_dict

def dnsenum (target) :
    dict = {}
    dict2 = {}
    output = cmdline(target)
    dict["serveur DNS"] = getNS(output)
    dict["serveur maitre"] = getSOA(output)
    dict["Zone"] = getZone(output)
    try :
        dict2 = getZoneTransferDetails(output)
        dict.update(dict2)
        dict["wildcard"] = getwildcard(output)
        list_sub= getsubdomains(output)
        domains = parsesubdomains(list_sub)
        dict['hosts found'] = domains
        iprange = getiprange(output)
        listrange = parselistrange(iprange)
        dictrange = strtodict(listrange)
        dict['ip range'] = dictrange
    except :
        dict["wildcard"]= 'none'
        dict['hosts found'] = 'none'
        dict['ip range'] = 'none'

    return dict


print (dnsenum ("zonetransfer.me"))



