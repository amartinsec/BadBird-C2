# BadBird C2 Through Canarytokens
# Author: Austin Martin @amartinsec/blog.amartinsec.com
from colorama import Fore


#!/usr/bin/env python3

def postExpWelcome():
    #More ASCII
    # fire ascii from https://ascii.co.uk/art/fire
    print(Fore.RED)
    print("                           (  .      )        ( ")
    print("         .-.            )           (           )   )")
    print("        (  '>                 .  '   .   '  .  '  . ")
    print("        /  \\        (    , )       (.   )  (   ',    )")
    print("       /  \ |         .' ) ( . )    ,  ( ,     )   ( .")
    print("      / ,_//       ). , ( .   (  ) ( , ')  .' (  ,    ) " )
    print(Fore.WHITE + "~~~~~" + Fore.RED + "//'--'" + Fore.WHITE + "~~~~~~~" + Fore.RED + "(_,) . ), ) _) _,')  (, ) '. )  ,. (' )" + Fore.WHITE + "~~~~")
    print("~~~~" + Fore.RED + "//" + Fore.WHITE + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("~~~" + Fore.RED + "//" + Fore.WHITE + "~~~~~~~~~~~~~~~~~~~~~ " + Fore.RESET + "Post-exp Shell " + Fore.WHITE + "~~~~~~~~~~~~~~~~~~~~~")

    print(Fore.RESET + "\nType `help` for a list of post-exploitation commands\n")


def postExpHelp():

    print(Fore.GREEN + "[+]" + Fore.RESET + " Post Exploitation Shell\n")
    print("\t`Back` or `Exit`\tReturns to the main menu\n")
    print("\tHelp\tPrints this menu")
    print("\tgetprivs\tGrabs the current user's privileges")
    print("\tgetuid\tReturns the current user's UID with the current token")
    print("\tkillproc\tKills a process by PID")
    print("\tsysmon-kill\tStops sysmon")
    print("\tbyod\tAttempts to elevate to SYSTEM by using the BYOD (Bring-your-own-driver) method")
    print("\tcursed-chrome\tCursed Chrome implementation from mandatoryprogrammer")
    print("\tteam-thief <`cookies` or `snoop`>\tSteal the user's MS Teams session token or grabs cached conversations")
    print("\treg stuff\tFun post-exp registry stuff here")
    print("\tHelp:\tPrints this menu\n")


def postExpShell():
    postExpWelcome()

    while True:
        user_input = input(Fore.GREEN + "BadBird>> " + Fore.RESET)
        if user_input.lower() == "back" or user_input.lower() == "exit":
            print(Fore.RESET + "Returning to main menu...\n")
            break
        elif user_input.lower() == "help":
            postExpHelp()

        else:
            print(Fore.RED + "[-]" + Fore.RESET + " Unknown command: " + user_input)

