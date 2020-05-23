try:
    # for Python2
    from Tkinter import *
    from Tkinter import font
except ImportError:
    # for Python3
    from tkinter import *
    from tkinter import font

import functools
import dnsenum
import Nmap_Auto as nmap
import MailsExtract
import WhoIs
import SHodan
import nessusPy


class ScrollableFrame(Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = Canvas(self, bg="#1f2223", highlightthickness=0, bd=0)
        scrollbar = Scrollbar(self, orient="vertical", command=canvas.yview, activebackground="#29839e", bg="#29839e",
                              troughcolor="#1f2223", activerelief="flat", bd=0)
        self.scrollable_frame = Frame(canvas, bg="#1f2223")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


def interface():

    root = Tk()
    root.title("Information gathering")
    root['bg'] = 'black'

    def displayWelcomeInterface():
        mainFrame = Frame(root, bg="green")
        Label(mainFrame, text='Please choose a tool', font=font.Font(weight="bold", size=25), bg="#1f2223",
              fg="#27beec", height=5, width=30).grid()
        mainFrame.pack(side=TOP, fill="both", expand=True)

    def displayNmapInterface():

        nmapFrame = Frame(root, bg="#1f2223", pady=55, padx=210)

        Button(nmapFrame, bg="#29353a", bd=0, fg="#27beec", activebackground="#384d54", activeforeground="#27beec",
               text="Launch nmap host discovery", command=nmapHostDiscovery,
               font=font.Font(size=10), highlightthickness=0)\
            .pack(side=TOP)

        Label(nmapFrame, bg="#1f2223", fg="#27beec", text="OR", pady=25, font=font.Font(size=15)).pack(side=TOP)

        #targetScanFrame = Frame(nmapFrame, bg="#1f2223").pack(side=TOP)

        targetScanFrame = Frame(nmapFrame, bg="#1f2223")

        targetEntry = Entry(targetScanFrame)

        Button(targetScanFrame, bg="#29353a", bd=0, fg="#27beec",  activebackground="#384d54", highlightthickness=0,
               activeforeground="#27beec", text="Scan target:", command=functools.partial(nmapScanTarget, targetEntry))\
            .pack(side=LEFT)

        Label(targetScanFrame, bg="#1f2223", fg="#27beec", text="  ").pack(side=LEFT)

        targetEntry.pack(side=LEFT)

        targetScanFrame.pack(side=TOP)

        for widget in root.winfo_children():
            if not widget.winfo_name() == topFrameName and not widget.winfo_name() == nmapFrame.winfo_name():
                widget.destroy()

        nmapFrame.pack(side=TOP, expand=True, fill='both')

    def nmapHostDiscovery():
        listTarget = nmap.getOpenPorts("192.168.0.0/24", arguments="-sn")
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
            Label(nmapPortFrame, bg="#1f2223", fg="#42b97d", font=font.Font(size=10), pady=10,
                  text=str(port) + "/tcp => Service: " + description["service"] + " => Version: " +
                        description["version"] + ", extra infos:" + description["extrainfo"]
                  ).pack(side=TOP)

        nmapPortFrame.pack(side=TOP, expand=True, fill="both")

    def displayDnsEnumInterface():

        for widget in root.winfo_children():
            if not widget.winfo_name() == topFrameName:
                widget.destroy()
        mainFrame = Frame(root, bg="#1f2223", pady=55, padx=200)
        Label(mainFrame, text="Dns Enum", bg="#1f2223", fg="#27beec",
              font=font.Font(size=15, weight="bold"), pady=10).pack(side=TOP)
        targetFrame = Frame(mainFrame, bg="#1f2223", pady=30)
        domainEntry = Entry(targetFrame)
        Button(targetFrame, bg="#29353a", fg="#27beec", activebackground="#384d54", activeforeground="#27beec",
               bd=0, text="Scan domain:", command=functools.partial(dnsEnumTarget, domainEntry), highlightthickness=0) \
            .pack(side=LEFT)
        Label(targetFrame, bg="#1f2223", fg="#27beec", text="  ").pack(side=LEFT)
        domainEntry.pack(side=LEFT)
        targetFrame.pack(side=TOP)
        mainFrame.pack(side=TOP, expand=True, fill='both')

    def dnsEnumTarget(domain):
        domainName = domain.get()
        dnsEnumResult = dnsenum.dnsenum(domainName)

        for widget in root.winfo_children():
            if not widget.winfo_name() == topFrameName:
                widget.destroy()

        dnsEnumFrame = Frame(root, bg="#1f2223", pady=60, padx=200)

        Label(dnsEnumFrame, text="Fierce scan report for " + domainName,
              bg="#1f2223", fg="#27beec", font=font.Font(size=15, weight="bold"), pady=10).pack(side=TOP)
        Label(dnsEnumFrame, text="DNS server: " + dnsEnumResult["serveur DNS"],
              bg="#1f2223", fg="#27beec", font=font.Font(size=15), pady=5, justify="left")\
            .pack(side=TOP, expand=True, fill='x')
        Label(dnsEnumFrame, text="Master server: " + dnsEnumResult["serveur maitre"],
              bg="#1f2223", fg="#27beec", font=font.Font(size=15), pady=5, anchor="w")\
            .pack(side=TOP, expand=True, fill='x')

        if dnsEnumResult["Zone"]:
            maxLen = 0
            for dnsName in dnsEnumResult["ZoneInfos"].keys():
                if len(dnsName) > maxLen:
                    maxLen = len(dnsName)

            listDNSinfos = ScrollableFrame(dnsEnumFrame)

            for dnsName, infos in dnsEnumResult["ZoneInfos"].items():

                containerF = Frame(listDNSinfos.scrollable_frame)
                Label(containerF, text=dnsName, bg="#1f2223", anchor="w", fg="#27beec", width=maxLen).pack(side=LEFT)
                Label(containerF, text=": " + infos[0], bg="#1f2223", anchor="w", fg="#27beec")\
                    .pack(side=LEFT, expand=True, fill='x')
                containerF.pack(side=TOP, expand=True, fill='x')

                for i in range(1, len(infos)):
                    containerOtherInfos = Frame(listDNSinfos.scrollable_frame)
                    Label(containerOtherInfos, text="", width=maxLen, bg="#1f2223").pack(side=LEFT)
                    Label(containerOtherInfos, text=": " + infos[i], bg="#1f2223", anchor="w", fg="#27beec")\
                        .pack(side=LEFT, expand=True, fill='x')
                    containerOtherInfos.pack(side=TOP, expand=True, fill='x')

            listDNSinfos.pack(side=TOP, expand=True, fill="both")
        else:
            Label(dnsEnumFrame, text="Zone transfert failure", bg="#1f2223", fg="red",
                  font=font.Font(size=25), pady=30).pack(side=TOP)

        dnsEnumFrame.pack(side=TOP, expand=True, fill='both')
        return

    def displayMailExtractorInterface():

        for widget in root.winfo_children():
            if not widget.winfo_name() == topFrameName:
                widget.destroy()
        mainFrame = Frame(root, bg="#1f2223", pady=55, padx=200)
        Label(mainFrame, text="Mail-extractor", bg="#1f2223", fg="#27beec",
              font=font.Font(size=15, weight="bold"), pady=10).pack(side=TOP)
        targetFrame = Frame(mainFrame, bg="#1f2223", pady=30)
        domainEntry = Entry(targetFrame)
        Button(targetFrame, bg="#29353a", fg="#27beec", activebackground="#384d54", activeforeground="#27beec",
               bd=0, text="Scan domain:", command=functools.partial(extractMails, domainEntry), highlightthickness=0) \
            .pack(side=LEFT)
        Label(targetFrame, bg="#1f2223", fg="#27beec", text="  ").pack(side=LEFT)
        domainEntry.pack(side=LEFT)
        targetFrame.pack(side=TOP)
        mainFrame.pack(side=TOP, expand=True, fill='both')

    def extractMails(domain):
        domainName = domain.get()
        e = MailsExtract.Extractor(domainName)
        listMails = e.crawl()

        for widget in root.winfo_children():
            if not widget.winfo_name() == topFrameName:
                widget.destroy()
        mainFrameMails = Frame(root, bg="#1f2223", pady=60, padx=200)

        Label(mainFrameMails, text="Found " + str(len(listMails)) + " mails in " + domainName,
              bg="#1f2223", fg="#27beec", font=font.Font(size=15, weight="bold"), pady=10).pack(side=TOP)

        listFrame = ScrollableFrame(mainFrameMails)

        for mails in listMails:
            Label(listFrame.scrollable_frame, text=mails, bg="#1f2223", anchor="w", fg="#27beec") \
                .pack(side=TOP, expand=True, fill='x')

        listFrame.pack(side=TOP, expand=True, fill="both")

        mainFrameMails.pack(side=TOP, expand=True, fill='both')

        return

    def displayWhoIsInterface():

        for widget in root.winfo_children():
            if not widget.winfo_name() == topFrameName:
                widget.destroy()
        mainFrame = Frame(root, bg="#1f2223", pady=55, padx=200)
        Label(mainFrame, text="WhoIs", bg="#1f2223", fg="#27beec",
              font=font.Font(size=15, weight="bold"), pady=10).pack(side=TOP)
        targetFrame = Frame(mainFrame, bg="#1f2223", pady=30)
        domainEntry = Entry(targetFrame)
        Button(targetFrame, bg="#29353a", fg="#27beec", activebackground="#384d54", activeforeground="#27beec",
               bd=0, text="Scan domain:", command=functools.partial(launchWhoIs, domainEntry), highlightthickness=0) \
            .pack(side=LEFT)
        Label(targetFrame, bg="#1f2223", fg="#27beec", text="  ").pack(side=LEFT)
        domainEntry.pack(side=LEFT)
        targetFrame.pack(side=TOP)
        mainFrame.pack(side=TOP, expand=True, fill='both')

    def launchWhoIs(domain):
        domainName = domain.get()
        domainDict = WhoIs.new_whois(domainName)

        for widget in root.winfo_children():
            if not widget.winfo_name() == topFrameName:
                widget.destroy()
        mainFrameMails = Frame(root, bg="#1f2223", pady=25, padx=200)

        Label(mainFrameMails, text="Result for " + domainName,
              bg="#1f2223", fg="#27beec", font=font.Font(size=15, weight="bold"), pady=30).pack(side=TOP)

        listFrame = ScrollableFrame(mainFrameMails)

        for field, valu in domainDict.items():
            Label(listFrame.scrollable_frame, text=str(field) + ": " + str(valu), bg="#1f2223", anchor="w",
                  fg="#27beec").pack(side=TOP, expand=True, fill='x')

        listFrame.pack(side=TOP, expand=True, fill="both")

        mainFrameMails.pack(side=TOP, expand=True, fill="both")

    def displayShodanInterface():

        mainFrame = Frame(root, bg="#1f2223", pady=55, padx=200)
        Label(mainFrame, text="Shodan", bg="#1f2223", fg="#27beec",
              font=font.Font(size=15, weight="bold"), pady=10).pack(side=TOP)
        targetFrame = Frame(mainFrame, bg="#1f2223", pady=30)
        domainEntry = Entry(targetFrame)
        Button(targetFrame, bg="#29353a", fg="#27beec", activebackground="#384d54", activeforeground="#27beec",
               bd=0, text="Scan domain:", command=functools.partial(launchShodan, domainEntry), highlightthickness=0) \
            .pack(side=LEFT)
        Label(targetFrame, bg="#1f2223", fg="#27beec", text="  ").pack(side=LEFT)
        domainEntry.pack(side=LEFT)
        targetFrame.pack(side=TOP)
        for widget in root.winfo_children():
            if not widget.winfo_name() == topFrameName and not mainFrame.winfo_name() == widget.winfo_name():
                widget.destroy()
        mainFrame.pack(side=TOP, expand=True, fill='both')

    def launchShodan(domain):
        domainName = domain.get()
        domainDict = SHodan.SHodan(domainName)

        for widget in root.winfo_children():
            if not widget.winfo_name() == topFrameName:
                widget.destroy()
        mainFrame = Frame(root, bg="#1f2223", pady=25, padx=200)

        Label(mainFrame, text="Result for " + domainName,
              bg="#1f2223", fg="#27beec", font=font.Font(size=15, weight="bold"), pady=30).pack(side=TOP)

        listFrame = ScrollableFrame(mainFrame)

        for field, valu in domainDict.items():
            if not field == "information" and not valu is None and len(valu) > 0:
                Label(listFrame.scrollable_frame, text=str(field) + ": " + str(valu), bg="#1f2223", anchor="w",
                      fg="#27beec").pack(side=TOP, expand=True, fill='x')

        if "information" in domainDict:
            maxLen = 11
            for banner in domainDict["information"]:
                containerF = Frame(listFrame.scrollable_frame)
                Label(containerF, text="port: " + str(banner["port"]), bg="#1f2223", anchor="w", fg="#27beec")\
                    .pack(side=LEFT, expand=True, fill='x')
                containerF.pack(side=TOP, expand=True, fill='x')

                for field, valu in banner.items():
                    if not field == "port":
                        containerOtherInfos = Frame(listFrame.scrollable_frame)
                        Label(containerOtherInfos, text="", width=maxLen, bg="#1f2223").pack(side=LEFT)
                        Label(containerOtherInfos, text=field + ": " + str(valu), bg="#1f2223", anchor="w",
                              fg="#27beec").pack(side=LEFT, expand=True, fill='x')
                        containerOtherInfos.pack(side=TOP, expand=True, fill='x')

        listFrame.pack(side=TOP, expand=True, fill="both")
        mainFrame.pack(side=TOP, expand=True, fill="both")
        return

    def displayNessusInterface():

        for widget in root.winfo_children():
            if not widget.winfo_name() == topFrameName:
                widget.destroy()
        mainFrame = Frame(root, bg="#1f2223", pady=55, padx=200)
        Label(mainFrame, text="Nessus API", bg="#1f2223", fg="#27beec",
              font=font.Font(size=15, weight="bold"), pady=10).pack(side=TOP)

        fieldWidth = 15
        entryTab = []
        fieldNames = ["login", "password", "target"]

        for i in range(3):
            containerFrame = Frame(mainFrame, bg="#1f2223", pady=10)
            Label(containerFrame, text=fieldNames[i] + ": ", bg="#1f2223", fg="#27beec",
                  font=font.Font(size=11, weight="bold"), pady=8, width=fieldWidth, justify=LEFT).pack(side=LEFT)
            entryTab.append(Entry(containerFrame))
            entryTab[i].pack(side=LEFT)
            containerFrame.pack(side=TOP)
        Label(mainFrame, text=" ", bg="#1f2223", fg="#27beec",
              font=font.Font(size=15, weight="bold"), pady=6).pack(side=TOP)
        Button(mainFrame, bg="#29353a", fg="#27beec", activebackground="#384d54", activeforeground="#27beec",
               bd=0, text="Launch basic nessus scan", command=functools.partial(launchNessusBasicScan, entryTab),
               highlightthickness=0).pack(side=TOP)
        mainFrame.pack(side=TOP, expand=True, fill='both')

    def launchNessusBasicScan(listEntry):

        login = listEntry[0].get()
        password = listEntry[1].get()
        target = listEntry[2].get()

        for widget in root.winfo_children():
            if not widget.winfo_name() == topFrameName:
                widget.destroy()
        try:
            nessusPy.doScanByNessus(login, password, target, "basic")
            mainFrame = Frame(root, bg="green")
            Label(mainFrame, text='Nessus scan launched', font=font.Font(weight="bold", size=25), bg="#1f2223",
                  fg="#27beec", height=5).pack(side=TOP)
            mainFrame.pack(side=TOP, fill="both", expand=True)
        except:
            t = sys.exc_info()
            mainFrame = Frame(root, bg="green")
            Label(mainFrame, text=sys.exc_info()[1], font=font.Font(weight="bold", size=25), bg="#1f2223",
                  fg="#27beec", height=5, padx=40).pack(side=TOP, expand=True, fill="both")
            mainFrame.pack(side=TOP, fill="both", expand=True)

            print("Unexpected error:", sys.exc_info()[1])

    topFrame = Frame(root, relief='flat', bg="red", cursor="crosshair", name="topFrame")
    buttonFont = font.Font(weight="bold", size=10)

    Button(topFrame,
           bg="#1f2223", bd=0, fg="#27beec", text="WhoIs", command=displayWhoIsInterface, activebackground="#384d54",
           activeforeground="#27beec", font=buttonFont, highlightthickness=0).pack(side=LEFT, expand=True, fill="x")
    Button(topFrame, bg="#1f2223", bd=0, fg="#27beec", activebackground="#384d54", activeforeground="#27beec",
           font=buttonFont, highlightthickness=0, text="Shodan", command=displayShodanInterface, ) \
        .pack(side=LEFT, expand=True, fill="x")
    Button(topFrame,
           bg="#1f2223", bd=0, fg="#27beec", text="Mails Extract", command=displayMailExtractorInterface,
           activebackground="#384d54", activeforeground="#27beec", font=buttonFont, highlightthickness=0)\
        .pack(side=LEFT, expand=True, fill="x")
    Button(topFrame,
           bg="#1f2223", bd=0, fg="#27beec", text="Dns Enum", command=displayDnsEnumInterface,
           activebackground="#384d54", activeforeground="#27beec", font=buttonFont, highlightthickness=0)\
        .pack(side=LEFT, expand=True, fill="x")
    Button(topFrame,
           bg="#1f2223", bd=0, fg="#27beec", text="Nmap", command=displayNmapInterface, activebackground="#384d54",
           activeforeground="#27beec", font=buttonFont, highlightthickness=0)\
        .pack(side=LEFT, expand=True, fill="x")
    Button(topFrame,
           bg="#1f2223", bd=0, fg="#27beec", text="Nessus", command=displayNessusInterface,
           activebackground="#384d54", activeforeground="#27beec", font=buttonFont, highlightthickness=0)\
        .pack(side=LEFT, expand=True, fill="x")
    topFrame.pack(side=TOP, padx=0, pady=0, fill="x")

    topFrameName = topFrame.winfo_name()

    displayWelcomeInterface()

    root.mainloop()


if __name__ == '__main__':
    interface()
