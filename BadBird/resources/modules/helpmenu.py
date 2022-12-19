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

    print(Fore.GREEN + "[+]" + Fore.RESET + " BadBird C2:")
    print("\t Create-token:\tFetches a new token from Canarytokens.org")
    print("\t Shell <command>:\tTasks the implant with a command")
    print("\t Powershell <command>:\tTasks the implant with a PS command")
    print("\t Email <blah@foobar.com>\tchanges the email used to create tokens. Default email is blah@foobar.com")
    print("\t Exit:\tExits the C2")
    print("\t Help:\tShows the help menu")
    print("\t Sleep <seconds> <jitter>:\tChanges the time that the implant sleeps(default 5 seconds). Use jitter value to randmly modify sleep time (TODO ADD JITTER IMPLEMENTATION)")
    print("\t Canary-info:\tShows the current canary token info")
    print("\t Screenshot:\tTakes a screenshot of the host (TODO)")
    print("\t PWD:\tPrints the current working directory in each return (less opsec safe)")
    print("\t Fallback:\tGenerates a new canarytoken for the and C2 to use implant switch to it")
    print(
        "\t Kill:\tKills the implant. `Kill clean` will kill the implant and removes implant (TODO Add implant removal)")
    print("\t Log <log name>:\tLogs all command and output to text file (TODO)")
    print("\t Create-implant:\tGenerates .exe or .py implant payload")
    print("\t Connect <canary management url>:\tConnects to a listening implant (TODO)")
    print("\t Download:\tTasks implant to download remote file from host (TODO)")
    print("\t Upload:\tTasks implant to upload a file (TODO)")
    print("\t ps:\tPrints the running processes on the host and highlights suspected AV in red")
    print("\t Keystrokes <command>:\tKeylogging functionality. Commands are:`start` `stop` or `fetch`")
    print("\t Post-exp:\tEnter the post-exp shell (TODO)")
    print("\t Self-destruct:\tImplant will remove itself after specified time of last C2 server checkin  (TODO)")
    print(
        "\t Canary-endpoint:\tSpecify an endpoint for the implant to send results to. Default is a random path from the "
        "platforms options (TODO)\n")
