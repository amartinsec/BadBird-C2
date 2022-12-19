
                               (  .      )        ( 
             .-.            )           (           )   )
            (  '>                 .  '   .   '  .  '  . 
            /  \        (    , )       (.   )  (   ',    )
           /  \ |         .' ) ( . )    ,  ( ,     )   ( .
          / ,_//       ). , ( .   (  ) ( , ')  .' (  ,    ) 
    ~~~~~//'--'~~~~~~~(_,) . ), ) _) _,')  (, ) '. )  ,. (' )~~~~
    ~~~~//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~//~~~~~~~~~~~~~~~~~~~~~~~~~~ BadBird C2~~~~~~~~~~~~~~~~~~~~~
                      Canary Tokens For Command and Control
                         @amartinsec/blog.amartinsec.com

# BadBird C2

*BadBird can be unstable at times as this is the first release. I am working to improve stability as time permits.*

<br>

## Requirements
- Python 3
- Implant must run on Windows
- C2 Server must be run on Windows (working on *nix support)
  - Due to the current color scheme, it's recommended to run from cmd.exe (not powershell's blue background)
  - This will be fixed soon

<br>

## Installation
```
git clone https://github.com/amartinsec/BadBird.git
cd BadBird/
pip3 install -r requirements.txt
cd BadBird/
python3 c2Server.py
```

<br>


## Transfer of Data
When a canary token is triggered, it logs information about the request. BadBird C2 works by passing data
through http requests and obtaining data through the reporting mechanism. Using this method, there are two major limitations
that BadBird C2 has to follow to maintain stability:
- Each response when triggering a token must have an encoded length of less than 7000 characters.
- A token can only be triggered less than 50 times.

BadBird C2 abides by these limitations by splitting large responses into chunks and having the C2 Server reassemble. If the
amount of alerts gets too high or a response has to be chunked, the C2 Server will request a new token and facilitate with
the implant.

<br>


## Commands/Features

Run `help` to see a list of commands within the BadBird shell.

### Creation

- create-token
    - Fetches a new token from Canarytokens.org. Copy and paste the management url if running implant.py
- create-implant
    - Generates .exe (using pyinstaller) or .py implant payload. The resulting .exe/.py will have the management url added.
    - If creating a .exe, you can choose one of the .ico files stored in resources/icons/ to use as the icon.

### Implant Interaction

- shell \<command>
    - Tasks the implant with a running a command through cmd.exe
- powershell \<command>
    - Tasks the implant with a running a command through powershell.exe
- screenshot
    - Takes a screenshot and stores it in loot/\<implant name>/
    - The implant will attempt to take the best screenshot possible while staying under 45 token alerts
    - Multiple screens will cause the image to be shrunk to abide by the limit
    - Due to the large amount of data, a new token will be requested before and after the screenshot is received
- keystrokes \<start stop fetch>
    - Will capture typed keys and the corresponding focused window
    - `keystrokes start` will task the implant to start logging keystrokes
    - `keystrokes stop` will stop keylogging
    - `keystrokes fetch` will fetch the keystrokes from the implant and save to loot/\<implant name>/
- ps
    - Prints the running processes on the host and highlights processes based on type
- fallback
    - Generates a new canarytoken for the and C2 to use implant switch to it
    - C2 Server will coordinate with the implant and automatically switch to the new token
- kill
    - Kills the implant
    - TODO: Add self-removal
- sleep
    - Sleeps the implant for a specified amount of time
    - TODO: Add jitter functionality

### Configuration/Misc

- email
    - Sets the email to be used for token generation. Default is `blah@foobar.com`
    - Entering a real email will result in receiving many emails for each task/result
- exit
    - Exits the BadBird shell
- help
    - Prints the help menu
- canary-info
    - Prints the current canarytoken information (management url, token, etc)
- PWD
    - Adds the current working directory to the BadBird shell prompt
    - Less OPSEC safe

### Not yet implemented (coming soon features)

- log
- connect
- download
- upload
- post-exp
- self-destruct
- canary-endpoint


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

<br>

## Disclaimer 
This is meant for research purposes only. I made this very late at night out of my own curiosity. 

Your actions are your responsibility so be responsible. Thinkst is an amazing platform that provides the canarytokens.org platform for free and I'd recommend you researching more into the company if you are unfamiliar.
