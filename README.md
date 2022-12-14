# BadBird C2
Canarytokens as a C2 channel

<br>

Coming soon...

<br>

                .-.      ／￣￣￣￣￣￣＼
               (  '>   ＜  BadBird C2  |
               /  \      ＼＿＿＿＿＿＿／
              /  \ |         
             / ,_//
    ~~~~~~~~//'--'~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~//@amartinsec/blog.amartinsec.com~~~
    ~~~~~~//C2 Through Canarytokens~~~~~~~~~~~~~


<br>
<br>
<p align="center">
  <img src="https://github.com/amartinsec/BadBird/raw/main/Media/badbirdCreateImplant.gif" alt="Gif of BadBird creating and connecting to an implant"/>
</p>


<br>


## TODO

- [ ] Release pre-alpha version once the codebase is fixed (and a major refactor)
- [ ] Add advanced functionality (steal token, process injection, etc)
- [ ] Implement other Canarytoken formats for C2 communication
- [ ] Add ability to connect to listening implant/manage multiple implants
- [ ] Encrypt the payloads instead of encoding
- [ ] Add ability to download/upload files
- [ ] Add ability to take screenshots - In progress. Has the ability to only take partial screenshots 
- [X] Implement .exe generation with pyinstaller
- [ ] Add functionality to bundle payloads with .lnk's for extension spoofing + disk image packing
- [ ] Fully port python implant to C#
- [ ] Add post-exploitation modules - In progress
- [ ] OS testing
- [X] Keylogger
- [ ] Staged payloads
- [X] Add ability for implant/teamserver to fallback to a new token if tasked
- [ ] Have implant/teamserver automatically attempt to fallback if connection is lost - In progress
- [ ] JSON config to allow for more customization similar to a CS profile
- [ ] Web App UI?

<br>

## Commands/Features
Current Help Menu:

	 Create-token:	Fetches a new token from Canarytokens.org
	 Shell <command>:	Tasks the implant with a command
	 Powershell <command>:	Tasks the implant with a PS command
	 Email <blah@foobar.com>	changes the email used to create tokens. Currently using: blah@foobar.com
	 Exit:	Exits the C2
	 Help:	Shows the help menu
	 Sleep <seconds>:	Changes the time that the implant sleeps(default 5 seconds)
	 Canary-info:	Shows the current canary token info
	 Screenshot:	Takes a screenshot of the host (TODO)
	 PWD:	Prints the current working directory in each return (less opsec safe)
	 PS:	Lists the running processes. Will highlight processes based on suspected functionality
	 Fallback:	Generates a new canarytoken for the and C2 to use implant switch to it
	 Kill:	Kills the implant. `Kill clean` will kill the implant and removes implant
	 Log <log name>:	Logs all command and output to text file (TODO)
	 Create-implant:	Generates .exe or .py implant payload
	 Connect <canary management url>:	Connects to a listening implant (TODO)
	 Download:	Tasks implant to download remote file from host (TODO)
	 ps:	Prints the running processes on the host and highlights suspected AV in red
	 keystrokes <command>:	Keylogging functionality. Commands are:`start` `stop` or `fetch`
	 post-exp:	post-exp shell (TODO)
	 Canary-endpoint:	Specify an endpoint for the implant to send results to. Default is a random path from the platforms options (TODO)
   
<br>

## Create-token

Requests a new token from canarytokens.org

## Shell &lt;command&gt;

Tasks implant to run a command through: cmd.exe &lt;command&gt;

## Powershell &lt;command&gt;

Tasks implant to run a command through: powershell.exe -c &lt;command&gt;

## Email &lt;email&gt;

Changes the used to request new tokens.
When creating a canary token, an email that an alerts are sent to is required. Will display the current email in help menu

## Exit

Ends the teamserver shell. Will warn if there is a current implant connection

## Help

Displays the help menu

## Sleep &lt;time in seconds&gt;

Has the implant sleep for <seconds> before checking in with the management URL

## Canary-info

Prints the current canary alert/secret token
  
## Screenshot

(TODO) - Takes a screenshot of the open windows. Currently only take in a small amout of bytes. Will fix soon
                                                                                    
## PWD

Adds the current directory in the command shell. Works by sending command \"dir\" before all commands so this is less opsec safe
                                                                                    
## Screenshot

(TODO) - Takes a screenshot of the open windows. Currently only implements sizes < a small amout. Will fix soon

## Fallback

Will generate a new canary token and send/reconnect with the active implant.
                                                                                    
This function (fallback) is automatically called every ~45 token alerts due to losing connection around 50 requests (need to dig into this further)
  
  
## Kill 

Ends the current implant. Run \"kill clean\" (TODO) to delete the implant from the system

  
## Log

Logs all commands to a text file (It works but need to fix the wonky way I did this)
  

## Create-implant

Creates an implant using pyinstaller and will spit out wither a .exe or .py 
If creating .exe file, you can currently choose the .ico for it. Any .ico can be added to \\icons\\<ico file> to be used
(TODO - disk image payload creation)
  
## Connect
  
Connect to a listening implant (TODO - currently not implemented)
  
## Download

Download a remote file (TODO - currently not implemented
  
 
## Upload

Upload a file to the victim (TODO - currently not implemented)
  
  
## Ps

Lists the current running processes by executing: cmd.exe tasklist /V
  
Will highlight processes by suspected: AV, Explorer/Winlogon, Browsers, and common Admin Tools

Process list used is from: [ars3n11's CS aggressor script.](https://github.com/ars3n11/Aggressor-Scripts/blob/master/ProcessTree.cna) Thank for for the great list!
  
TODO - Implement an indented process tree
  
  
## keystrokes &lt;command&gt;

Lists the current running processes by executing &lt;cmd.exe tasklist /V&gt;
  
Will highlight processes by suspected: AV, Explorer/Winlogon, Browsers, and typical Admin Tools
  

  
Options are: keystrokes &lt;\'start\' \'stop\' or \'fetch\'&gt;
  
\'keystrokes fetch\' will return the keystrokes since the last fetch command
  
Output will be automatically written to the loot\\ dir

  
## post-exp
  
Enter a post-exploitation shell 
  
TODO - Persistence, more loot, etc.
  

## Canary-endpoint

Set URL that the implant uses to send data
  
Default is a random value from the canarytokens.org available options

<br>
<br>
  
## Why this was made

I recently went through the \`C2 Development in C#\` from Zero-Point Security/@rastamouse (I can't recommend these courses enough) and have wanted to create my own C2.
After seeing the VirusTotalC2 from @D1rkMtr, it sparked my interest in using a typical \'blue team tool\' for offensive purposes. I've used the canarytokens.org platform in the past and realized it could be used for so much more. After writing [this blogpost](https://blog.amartinsec.com/posts/canary/) on canary tokens, I started creating this project. I'm going (arguably) overboard on features because they can be resued in future projects.
  
<br>
<br>

## Headaches I'm working through
TODO

<br>
<br>


## Detection
Will be published when code is

<br>
<br>

## Requirements
Python 3+
Alot of dependencies (This will change when I refactor)

<br>
<br>


## Disclaimer 
This is meant for research purposes only. I made this very late at night out of my own curiosity. 

Your actions are your responsibility so be responsible. Thinkst is an amazing platform that provides the canarytokens.org platform for free and I'd recommend you researching more into the company if you are unfamiliar.
