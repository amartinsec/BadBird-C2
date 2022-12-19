
                .-.      ／￣￣￣￣￣￣＼
               (  '>   ＜  BadBird C2  |
               /  \      ＼＿＿＿＿＿＿／
              /  \ |         
             / ,_//
    ~~~~~~~~//'--'~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~//@amartinsec/blog.amartinsec.com~~~
    ~~~~~~//C2 Through Canarytokens~~~~~~~~~~~~~


# BadBird C2

*BadBird can be unstable at times as this is the first release. I am working to improve stability as time permits.*


### Requirements
- Python 3
- Implant must run on Windows
- C2 Server must be run on Windows (working on *nix support)
<br>

### Installation
```
git clone https://github.com/amartinsec/BadBird.git
cd BadBird/BadBird
pip3 install -r requirements.txt
python3 c2Server.py
```


### Transfer of Data
When a canary token is triggered, it logs information about the request. BadBird C2 works by passing data
through http requests and obtaining data through the reporting mechanism. Using this method, there are two major limitations
that BadBird C2 has to follow to maintain stability:
- Each response when triggering a token must have an encoded length of less than 7000 characters.
- A token can only be triggered less than 50 times.

BadBird C2 abides by these limitations by splitting large responses into chunks and having the C2 Server reassemble. If the
amount of alerts gets too high or a response has to be chunked, the C2 Server will request a new token and facilitate with
the implant.

### Commands/Features
Current Help Menu:
```
[+] CMD: help
Creation:
	 Create-token:	Fetches a new token from Canarytokens.org
	 Create-implant:	Generates .exe or .py implant payload

Implant Interaction:
	 Shell <command>:	Tasks the implant with a command
	 Powershell <command>:	Tasks the implant with a PS command
	 Screenshot:	Takes a screenshot of the host
	 Keystrokes <command>:	Keylogging functionality. Commands are:`start` `stop` or `fetch`
	 ps:	Prints the running processes on the host and highlights suspected AV in red
	 Fallback:	Generates a new canarytoken for the and C2 to use implant switch to it
	 Kill:	Kills the implant. `Kill clean` will kill the implant and removes implant (TODO Add implant removal)
	 Sleep <seconds> <jitter>:	Changes the time that the implant sleeps(default 5 seconds). Use jitter value to randmly modify sleep time (TODO ADD JITTER IMPLEMENTATION)

Configuration/Misc:
	 Email <blah@foobar.com>	changes the email used to create tokens. Default email is blah@foobar.com
	 Exit:	Exits the C2
	 Help:	Shows the help menu
	 Canary-info:	Shows the current canary token info
	 PWD:	Prints the current working directory in each return (less opsec safe)

Not yet implemented commands:
	 Log <log name>:	Logs all command and output to text file (TODO)
	 Connect <canary management url>:	Connects to a listening implant (TODO)
	 Download:	Tasks implant to download remote file from host (TODO)
	 Upload:	Tasks implant to upload a file (TODO)
	 Post-exp:	Enter the post-exp shell (TODO)
	 Self-destruct:	Implant will remove itself after specified time of last C2 server checkin  (TODO)
	 Canary-endpoint:	Specify an endpoint for the implant to send results to. Default is a random path from the platforms options (TODO)

```

<br>






<br>

<br>
<p align="center">
  <img src="https://github.com/amartinsec/BadBird/raw/main/Media/badbirdCreateImplant.gif" alt="Gif of BadBird creating and connecting to an implant"/>
</p>


<br>


## TODO

- [ ] Implement other Canarytoken formats for C2 communication
- [ ] Add ability to connect to listening implant/manage multiple implants
- [ ] Encrypt the payloads instead of encoding
- [ ] Add ability to download/upload files
- [X] Add ability to take screenshots 
- [X] Implement .exe generation with pyinstaller
- [ ] Add functionality to bundle payloads with .lnk's for extension spoofing + disk image packing
- [ ] Fully port python implant to C#
- [ ] Add post-exploitation modules - In progress
- [X] Keylogger
- [ ] Staged payloads
- [X] Add ability for implant/teamserver to fallback to a new token if tasked
- [ ] Have implant/teamserver automatically attempt to fallback if connection is lost - In progress
- [ ] Trobule shoot why C2 server is extremely unstable when running from *.nix


## Disclaimer 
This is meant for research purposes only. I made this very late at night out of my own curiosity. 

Your actions are your responsibility so be responsible. Thinkst is an amazing platform that provides the canarytokens.org platform for free and I'd recommend you researching more into the company if you are unfamiliar.
