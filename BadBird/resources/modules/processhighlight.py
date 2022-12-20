# BadBird C2 Through Canarytokens
# Author: Austin Martin @amartinsec/blog.amartinsec.com
from colorama import Fore


def highlightprocesses(processlist):
    # Thanks to ars3n11 https://github.com/ars3n11/Aggressor-Scripts/blob/master/ProcessTree.cna for process list
    # TODO ADD TREE FUNCTIONALITY
    print("\n")
    try:
        avfile = open("resources/processlist/av.txt", "r")
        avlist = avfile.read().split(" ")
        avfile.close()

        explorerWinlogon = ["explorer.exe", "winlogon.exe"]
        browserlist = ["chrome.exe", "firefox.exe", "iexplore.exe", "opera.exe", "safari.exe", "msedge.exe",
                       "MicrosoftEdgeCP.exe"]

        admintoolfile = open("resources/processlist/admintools.txt", "r")
        admintoollist = admintoolfile.read().split(" ")
        admintoolfile.close()

        list = processlist.splitlines()

        for line in list:
            process = line.split(" ")[0]
            if process in avlist:
                print(Fore.RED + line + Fore.RESET)

            elif process in explorerWinlogon:
                print(Fore.BLUE + line + Fore.RESET)

            elif process in browserlist:
                print(Fore.GREEN + line + Fore.RESET)

            elif process in admintoollist:
                print(Fore.YELLOW + line + Fore.RESET)

            else:
                print(Fore.RESET + line)

    except Exception as e:
        print(Fore.RED + "[-]" + Fore.RESET + " Error opening .txt files")
        print(e)