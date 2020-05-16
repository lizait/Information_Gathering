try:
    # for Python2
    import Tkinter
except ImportError:
    # for Python3
    from tkinter import *
    from tkinter import font

from functools import partial
import Nmap_Auto as nmap
import dnsenum

def interface():

    root = Tk()
    root.title("Information gathering")
    root['bg'] = 'blue'

    mainFrame = Frame(root, bg="green")
    Label(mainFrame, text='Please choose a tool', font=font.Font(weight="bold", size=25), bg="#1f2223", fg="#27beec",
          height=5, width=30).grid()

    def displayNmapInterface():

        for widget in root.winfo_children():
            if not widget.winfo_name() == topFrameName:
                widget.destroy()

        nmapFrame = Frame(root, bg="#1f2223", pady=105, padx=300)

        Button(nmapFrame, bg="#29353a", bd=0, fg="#27beec", activebackground="#384d54", activeforeground="#27beec",
               text="Lunch nmap host discovery", command=nmapHostDiscovery,  font=font.Font(size=10), highlightthickness=0)\
            .pack(side=TOP)

        Label(nmapFrame, bg="#1f2223", fg="#27beec", text="OR", pady=35, font=font.Font(size=20)).pack(side=TOP)

        #targetScanFrame = Frame(nmapFrame, bg="#1f2223").pack(side=TOP)

        targetScanFrame = Frame(nmapFrame, bg="#1f2223")

        targetEntry = Entry(targetScanFrame)

        Button(targetScanFrame, bg="#29353a", bd=0, fg="#27beec",  activebackground="#384d54", activeforeground="#27beec",
               text="Scan target:", command=partial(nmapScanTarget, targetEntry), highlightthickness=0)\
            .pack(side=LEFT)

        Label(targetScanFrame, bg="#1f2223", fg="#27beec", text="  ").pack(side=LEFT)

        targetEntry.pack(side=LEFT)

        targetScanFrame.pack(side=TOP)

        nmapFrame.pack(side=TOP, expand=True, fill='both')

    def nmapHostDiscovery():
        listTarget = nmap.getOpenPorts("192.168.43.0/24", arguments="-sn")
        for widget in root.winfo_children():
            if not widget.winfo_name() == topFrameName:
                widget.destroy()

        nmapListFrame = Frame(root, bg="#1f2223", pady=55, padx=250)

        Label(nmapListFrame, text="Found " + str(len(listTarget)) + " hosts", bg="#1f2223", fg="#27beec",
              font=font.Font(size=25), pady=30).pack(side=TOP)

        for hostIP, hostName in listTarget.items():
            Label(nmapListFrame, text=hostName["name"]+" with ip: "+hostIP, bg="#1f2223", fg="#27beec",
                  font=font.Font(size=15), pady=10).pack(side=TOP)

        nmapListFrame.pack(side=TOP, expand=True, fill="both")

    def nmapScanTarget(entry):
        target = entry.get()
        scanResult = nmap.getOpenPorts(target)
        for widget in root.winfo_children():
            if not widget.winfo_name() == topFrameName:
                widget.destroy()

        ipHost = scanResult.keys()

        nmapPortFrame = Frame(root, bg="#1f2223", pady=55, padx=150)
        Label(nmapPortFrame, text="Nmap scan report for " + scanResult[target]["name"] + " (" + target + ")",
              bg="#1f2223", fg="#27beec", font=font.Font(size=25), pady=30).pack(side=TOP)

        for port, description in scanResult[target]["tcp"].items():
            Label(nmapPortFrame, bg="#1f2223", fg="#42b97d", font=font.Font(size=15), pady=10,
                  text= str(port) + "/tcp => Service: " + description["service"] + " => Version: " + description["version"] + ", extra infos:" + description["extrainfo"]
                  ).pack(side=TOP)

        nmapPortFrame.pack(side=TOP, expand=True, fill="both")

    def displayDnsEnumInterface():

        for widget in root.winfo_children():
            if not widget.winfo_name() == topFrameName:
                widget.destroy()

        dnsEnumFrame = Frame(root, bg="#1f2223", pady=105, padx=300)

        targetScanFrame = Frame(dnsEnumFrame, bg="#1f2223")

        domainEntry = Entry(targetScanFrame)

        Button(targetScanFrame, bg="#29353a", bd=0, fg="#27beec",  activebackground="#384d54", activeforeground="#27beec",
               text="Scan domain:", command=partial(dnsEnumTarget, domainEntry), highlightthickness=0)\
            .pack(side=LEFT)

        Label(targetScanFrame, bg="#1f2223", fg="#27beec", text="  ").pack(side=LEFT)

        domainEntry.pack(side=LEFT)

        targetScanFrame.pack(side=TOP)

        dnsEnumFrame.pack(side=TOP, expand=True, fill='both')

    def dnsEnumTarget(domainEntry):
        domain = domainEntry.get()
        dnsEnumResult = dnsenum.dnsenum(domain)

        for widget in root.winfo_children():
            if not widget.winfo_name() == topFrameName:
                widget.destroy()

        dnsEnumFrame = Frame(root, bg="#1f2223", pady=105, padx=300)

        Label(dnsEnumFrame, text="Fierce scan report for " + domain,
              bg="#1f2223", fg="#27beec", font=font.Font(size=25), pady=30).pack(side=TOP)

        Label(dnsEnumFrame, text="DNS server: " + dnsEnumResult["serveur DNS"],
              bg="#1f2223", fg="#27beec", font=font.Font(size=25), pady=30).pack(side=TOP)

        Label(dnsEnumFrame, text="Master server: " + dnsEnumResult["serveur maitre"],
              bg="#1f2223", fg="#27beec", font=font.Font(size=25), pady=30).pack(side=TOP)

        if dnsEnumResult["Zone"]:
            pass
        else:
            Label(dnsEnumFrame, text="Zone transfert failure",
                  bg="#1f2223", fg="red", font=font.Font(size=25), pady=30).pack(side=TOP)




        dnsEnumFrame.pack(side=TOP, expand=True, fill='both')

        return




    topFrame = Frame(root, relief='flat', bg="red", cursor="crosshair", name="topFrame")
    buttonFont = font.Font(weight="bold", size=10)

    Button(topFrame, bg="#1f2223", bd=0, fg="#27beec", activebackground="#384d54", activeforeground="#27beec",
           font=buttonFont, highlightthickness=0, text="dnsenum", command=displayDnsEnumInterface, )\
        .pack(side=LEFT, expand=True, fill="x")
    Button(topFrame,
           bg="#1f2223", bd=0, fg="#27beec", text="nmap", command=displayNmapInterface, activebackground="#384d54",
           activeforeground="#27beec", font=buttonFont, highlightthickness=0).pack(side=LEFT, expand=True, fill="x")
    Button(topFrame,
           bg="#1f2223", bd=0, fg="#27beec", text="nessus", command=root.destroy, activebackground="#384d54",
           activeforeground="#27beec", font=buttonFont, highlightthickness=0)\
        .pack(side=LEFT, expand=True, fill="x")
    Button(topFrame,
           bg="#1f2223", bd=0, fg="#27beec", text="WhoIs", command=root.destroy, activebackground="#384d54",
           activeforeground="#27beec", font=buttonFont, highlightthickness=0)\
        .pack(side=LEFT, expand=True, fill="x")
    Button(topFrame,
           bg="#1f2223", bd=0, fg="#27beec", text="shodan", command=root.destroy, activebackground="#384d54",
           activeforeground="#27beec", font=buttonFont, highlightthickness=0)\
        .pack(side=LEFT, expand=True, fill="x")
    Button(topFrame,
           bg="#1f2223", bd=0, fg="#27beec", text="Mails Extract", command=root.destroy, activebackground="#384d54",
           activeforeground="#27beec", font=buttonFont, highlightthickness=0)\
        .pack(side=LEFT, expand=True, fill="x")
    topFrame.pack(side=TOP, padx=0, pady=0, fill="x")

    topFrameName = topFrame.winfo_name()

    mainFrame.pack(side=TOP, fill="both", expand=True)

    root.mainloop()


if __name__ == '__main__':
    interface()
