from colorama import Fore, init
init(convert=True)

def welcome():
    # Just some ASCII art
    print("\n"+Fore.RED + "            .-.   ")
    print("           (  '>   " + Fore.GREEN + "BadBird C2" + Fore.RED )
    print("           /  \\     ")
    print("          /  \ |")
    print("         / ,_//")
    print(Fore.WHITE + "~~~~~~~~" + Fore.RED + "//'--'" + Fore.WHITE + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(
        Fore.WHITE + "~~~~~~~" + Fore.RED + "//" + Fore.WHITE + "~" + Fore.RESET + " @amartinsec/blog.amartinsec.com " + Fore.WHITE + "~~")
    print(
        Fore.WHITE + "~~~~~~" + Fore.RED + "//" + Fore.WHITE + "~~" + Fore.RESET + " C2 Through Canarytokens " + Fore.WHITE + "~~~~~~~~~~~")
    print(Fore.RESET)
    print("Type `help` for a list of commands\n")



def help():

    print("\nCreation:")
    print("   Create-token:\tFetches a new token from Canarytokens.org".expandtabs(35))
    print("   Create-implant:\tGenerates .exe or .py implant payload".expandtabs(35))

    print("\nImplant Interaction:")
    print("   Shell <command>:\tTasks the implant with a command".expandtabs(35))
    print("   Powershell <command>:\tTasks the implant with a PS command".expandtabs(35))
    print("   Screenshot:\tTakes a screenshot of the host".expandtabs(35))
    print("   Keystrokes <command>:\tKeylogging functionality. Commands are:`start` `stop` or `fetch`".expandtabs(35))
    print("   Ps:\tPrints the running processes on the host and highlights suspected AV in red".expandtabs(35))
    print("   Fallback:\tGenerates a new canarytoken for the and C2 to use implant switch to it".expandtabs(35))
    print("   Kill:\tKills the implant. `Kill clean` will kill the implant and removes implant (TODO Add implant removal)".expandtabs(35))
    print("   Sleep <seconds> <jitter>:\tChanges the time that the implant sleeps(default 5 seconds). Use jitter value to randmly modify sleep time (TODO ADD JITTER IMPLEMENTATION)".expandtabs(35))
    print("   Download <filename>:\tTasks implant to download remote file".expandtabs(35))

    print("\nConfiguration/Misc:")
    print("   Email <blah@foobar.com>:\tChanges the email used to create tokens.".expandtabs(35))
    print("   Exit:\tExits the C2".expandtabs(35))
    print("   Help:\tShows the help menu".expandtabs(35))
    print("   Canary-info:\tShows the current canary token info".expandtabs(35))
    print("   PWD:\tPrints the current working directory in each return (less opsec safe)".expandtabs(35))

    print("\nCommands coming soon:")
    print("   Log:\tLogs all commands and output to text file within loot (TODO)".expandtabs(35))
    print("   Connect <management url>:\tConnects to a listening implant (TODO)".expandtabs(35))
    print("   Upload:\tTasks implant to upload a file (TODO)".expandtabs(35))
    print("   Post-exp:\tEnter the post-exp shell (TODO)".expandtabs(35))
    print("   Self-destruct:\tImplant will remove itself after specified time of last C2 server checkin  (TODO)".expandtabs(35))
    print("   Canary-endpoint:\tSpecify an endpoint for the implant to send results to. Default is a random path from the platforms options (TODO)\n".expandtabs(35))
