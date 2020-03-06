import sys
import nmap
import nessrest


def getOpenPorts(hosts, ports=None, arguments="-sV -sC", sudo=False):
    """
    Scan by nmap given hosts and their ports

    :param hosts: string for hosts
    :param ports: string for ports
    :param arguments: string of arguments for nmap
    :param sudo: true if launch by sudo

    :returns: scan result as dictionary
    :error: can raise AttributeError if bad arguments and nmap.PortScannerError for all problem in nmap
    """

    scanner = nmap.PortScanner()

    try:
        nmapResult = scanner.scan(hosts=hosts, ports=ports, arguments=arguments, sudo=sudo)
    except nmap.PortScannerError:
        print("PortScannerError exception ==> problem with nmap: {}".format(nmap.PortScannerError.args))
        return -1

    result_scan = {}

    if "error" in nmapResult["nmap"]["scaninfo"]:
        for error in nmapResult["nmap"]["scaninfo"]["error"]:
            print(error)
        raise AttributeError()
    else:
        for host, info in nmapResult["scan"].items():
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

    try:
        resultScan = getOpenPorts("192.168.137.3/24", arguments="-sn")
        resultScan = getOpenPorts("192.168.137.3/24")

    except:
        t = sys.exc_info()
        print("Unexpected error:", sys.exc_info()[0])
    print("next")




