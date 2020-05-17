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


class ScrollableFrame(Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = Canvas(self, bg="#1f2223", highlightthickness=0, bd=0)
        scrollbar = Scrollbar(self, orient="vertical", command=canvas.yview, activebackground="#27beec", bg="#27beec",
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

        dnsEnumFrame = Frame(root, bg="#1f2223", pady=60, padx=200)

        Label(dnsEnumFrame, text="Fierce scan report for " + domain,
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
                #Label(listDNSinfos.scrollable_frame, text=dnsName + ": " + infos[0], bg="green", anchor="w")\
                 #   .pack(expand=True, fill='x')

                containerF = Frame(listDNSinfos.scrollable_frame, bg="green")
                Label(containerF, text=dnsName, bg="#1f2223", anchor="w", fg="#27beec", width=maxLen).pack(side=LEFT)
                Label(containerF, text=": " + infos[0], bg="#1f2223", anchor="w", fg="#27beec").pack(side=LEFT, expand=True, fill='x')
                containerF.pack(side=TOP, expand=True, fill='x')

                """
                for i in range(1, len(infos)):
                    containerOtherInfos = Frame(listDNSinfos.scrollable_frame, bg="purple")
                    Label(containerOtherInfos, text="", width=maxLen).pack(side=LEFT)
                    Label(containerOtherInfos, text=": " + infos[i]).pack(side=LEFT)
                    containerOtherInfos.pack(side=TOP)
                """
            listDNSinfos.pack(side=TOP, expand=True, fill="both")

        else:
            Label(dnsEnumFrame, text="Zone transfert failure",
                  bg="#1f2223", fg="red", font=font.Font(size=25), pady=30).pack(side=TOP)

        dnsEnumFrame.pack(side=TOP, expand=True, fill='both')
        root.update()
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
