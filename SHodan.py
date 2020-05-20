import shodan
import requests

SHODAN_KEY = "aerdEG08BEtHxjvTzCh620CkReOlqmpL"
api = shodan.Shodan(SHODAN_KEY)


def dnsresolve (target) :
    dnsResolve = 'https://api.shodan.io/dns/resolve?hostnames=' + target + '&key=' + SHODAN_KEY
    resolved = requests.get(dnsResolve)
    IP = resolved.json()[target]
    return IP

def strtolist (banner_str) :
    datalist = banner_str.split('\r\n')
    tmp = datalist[0]
    datalist[0] = 'banner: ' + tmp
    datalist = list(filter(None, datalist))
    return datalist

def listtodict (banner_list) :
    dict = {}
    for i in banner_list:
        try :
            key, value = i.split(":",1)
            dict[key] = value
        except:
            key = i
            value = ''
    return dict


def ordereddict (dict1, dict2):
    dict1.update(dict2)
    return dict1

def listinfo (listhost) :
    listinf = []
    for item in listhost['data']:
        dict_banner ={}
        dict1 = {}
        dict2 = {}
        banner_str = item['data']
        banner_list = strtolist(banner_str)
        dict2= listtodict(banner_list)
        dict1['port']=item['port']
        dict_banner = ordereddict(dict1,dict2)
        listinf.append(dict_banner)

    alldict= {}
    alldict['information '] = listinf
    return alldict


def generalinfo (host) :
    dict = {
        "ip": host['ip_str'],
        "org": host.get('org', 'n/a'),
        "os": host.get('os', 'n/a'),
        "vulns":
            host['vulns'] if 'vulns' in host else
            ' ',
        "product" :
            host['product'] if 'product' in host else
            ' ',
        "uptime" :
            host['uptime'] if 'uptime' in host else
            ' ',
        "link" :
            host['host'] if 'host' in host else
            ' ',
        "devicetype" :
            host['devicetype'] if 'devicetype' in host else
            ' ',
        "cpe" :
            host['cpe'] if 'cpe' in host else
            ' '
    }
    return dict

def vulnsdescription (vulns) :
    CVE = vulns.replace('!', '')
    exploits = api.exploits.search(CVE)
    for item in exploits['matches']:
        if item.get('cve')[0] == CVE:
            item.get('description')
    return item



def SHodan (target) :
    try :
        if (target[0].isalpha()) :
                target = dnsresolve (target)
        host = api.host(target)
        dict1 = generalinfo(host)
        dict2 = listinfo(host)
        dict1.update(dict2)
        return dict1

    except shodan.exception.APIError as error :
        print(error)
    except TypeError :
        print ("nvalid domain name\nplease retry !")
    except requests.exceptions.ConnectionError :
        print ("The server refuses your  connections\n "
               "too many requests sent from same ip address in short period of time\n  "
               "please wait a few minutes before you try again ;)")
        
print (SHodan("www.packtpub.com"))



