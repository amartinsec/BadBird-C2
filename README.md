<!--
BadBird C2 Through Canarytokens
Author: Austin Martin @amartinsec/blog.amartinsec.com
-->
```
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
```
# BadBird C2

*BadBird C2 is still in active development, but I didn't want to wait before releasing. I am working to improve stability as time permits.*

<br>

## Requirements
- Python 3
- Implant must run on Windows
- C2 Server must *currently* be run on Windows (working on *nix support)
  - Due to the current color scheme, it's recommended to run from cmd.exe (powershell's blue background causes the color scheme to be hard to read)
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
through the triggered tokens and reporting mechanism. Using this method, there are two major limitations
by using the platform:
- Data for a triggered token must have an encoded length of less than 7000 characters.
- A token can only be triggered around 50 times.


BadBird C2 works around these limitations by splitting large responses into chunks and having the C2 Server reassemble. If the
amount of alerts gets too high or a response has to be chunked, the C2 Server will request a new token and update the implant.

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
    - TODO: Add ability to specify monitor (3+ monitors will cause the screenshot to be low res)
- keystrokes \<start stop fetch>
    - Will capture typed keys and the corresponding focused window
    - `keystrokes start` will task the implant to start logging keystrokes
    - `keystrokes stop` will stop keylogging
    - `keystrokes fetch` will fetch the keystrokes from the implant and save to loot/\<implant name>/
    - Ex. output from ```keystrokes fetch```:
  ```
      -------------------< focused process name >-------------------
      ----------------------- < Date/Time >-------------------------
      haxor@l33t.com
      super_secret_password <ENTER KEY>
      --------------------------------------------------------------
  ```
- ps
    - Prints the running processes on the host and highlights processes based on type
- fallback
    - Generates a new canarytoken for the and C2 to use implant switch to it
    - C2 Server will coordinate with the implant and automatically switch to the new token
- kill
    - Kills the implant
    - TODO: Add self-removal
- sleep \<seconds> \<jitter percentage>
    - Sleeps the implant for a specified amount of time
    - Add jitter percentage amount to enable random jitter
- download \<filename>
  - Downloads a file from the implant's host and stores it in loot/\<implant name>/
- post-exp
  - BadBird post-exploitation shell (currently in development)

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
    - Adds the current working directory to the BadBird shell
    - Less OPSEC safe

### Features coming soon

- log
  - Logs everything to a .txt file stored within the loot dir
- connect
  - Connects to a listening implant
- upload
  - Uploads a file to the implant's host
- self-destruct
  - Kills the implant after a certain amount of time
- canary-endpoint
  - Sets the canarytoken alerting endpoint to use (currently random from options that canarytokens.org provides)
- token-type
  - Specifies the type of token to use (currently using web bug/URL token that canarytokens.org provides)
-background
  - Backgrounds the implant


<br>
<p>
  <img src="https://github.com/amartinsec/BadBird/raw/main/Media/badbirdCreateImplant.gif" alt="Gif of BadBird creating and connecting to an implant"/>
</p>


<br>

## Detection 
Coming Soon

<br>

## Disclaimer 
This is meant for research purposes only. I made this very late at night out of my own curiosity to see if "it could be done". 

Your actions are your responsibility so be responsible. Thinkst is an amazing platform that provides the canarytokens.org platform for free, and I'd recommend researching more if you are unfamiliar.

<br>

## Final Note
As of now, the implant will get flagged by most AV/EDR/XDR/Or whatever its being called nowadays (usually from the keylogger functionality  (HackTool:SH/PythonKeylogger.B Defender alert)). I plan on porting the implant to C# but that won't be done until the current project is deemed stable. If you want to obfuscate, try pyarmor or something...