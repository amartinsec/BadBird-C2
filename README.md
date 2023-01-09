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

My blogpost about canary tokens can be found [here.](https://blog.amartinsec.com/posts/canary/) 

*BadBird C2 is still in development, but I didn't want to wait before releasing. I am working to improve stability as time permits.*

<br>

## Transfer of Data
When a canary token is triggered, it logs information about the request. BadBird C2 works by passing data
through the user-agent of the token. Using this method, there are two major limitations
by using the platform:
- Data for a triggered token must have an encoded length of less than 7000 characters.
- A token can only be triggered ~50 times.


BadBird C2 works around these limitations by splitting large responses into chunks and having the C2 Server reassemble. If the
amount of alerts gets too high or a response has to be chunked, the C2 Server will request a new token and update the implant.

<br>

## Requirements
- Python 3
- Implant/payload must run on Windows
- c2Server.py was having issues running on *nix
  - I haven't narrowed down the issue, but there's massive stability issues.
  - Due to the current color scheme, it's recommended to run from cmd.exe.
    - The above will be fixed soon

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


## Commands/Features

**Update (1/6/23):** Traffic is now AES encrypted. Change the key to something unique or anyone can decrypt the task/result
if they get the management URL (The default key is ```b'badbirdbadbirdbadbirdbadbirdbadb'```. If using the default implant.py, change the key in both c2Server.py and implant.py. Generating a payload through the BadBird shell `generate-implant` command will update
the generated payload with the key.

<br>

Run `help` to see a list of commands within the BadBird shell.

### Creation

- create-token:
    - Fetches a new token from Canarytokens.org. Copy and paste the management url if using the template `implant.py`:
<img src="https://github.com/amartinsec/BadBird/raw/main/Media/implant.png"/>


- create-implant:
    - Fetches a new token from Canarytokens.org and generates a new implant. The implant is saved to the `payloads/<chosen name>/` directory.
    - Generates a .exe (using pyinstaller) or .py implant payload. The resulting .exe/.py will have the management url added.
    - If creating a .exe, you can choose one of the .ico files stored in resources/icons/ to use as the icon.

### Implant Interaction

- shell \<command>:
    - Tasks the implant with a running a command through cmd.exe
- powershell \<command>:
    - Tasks the implant with a running a command through powershell.exe
- screenshot:
    - Takes a screenshot and stores it in loot/\<implant name>/
    - The implant will attempt to take the best screenshot possible while staying under 45 token alerts
    - Multiple screens will cause the image to be shrunk to abide by the limit
    - Due to the large amount of data, a new token will be requested before and after the screenshot is received
    - TODO: Add ability to specify monitor (multiple monitors will cause the screenshot to be low res)
- keystrokes \<start stop fetch>:
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
- ps:
    - Prints all processes and highlights based on suspected type
- fallback:
    - Grabs a new canarytoken for the and C2 to use implant switch to it
    - C2 Server will coordinate with the implant and automatically switch to the new token
- kill:
    - Kills the implant
    - TODO: Add self-removal
- sleep \<seconds> \<jitter percentage>:
    - Sleeps the implant for a specified amount of time
    - Add jitter percentage amount to enable random jitter
- download \<filename>:
  - Downloads a file from the implant's host and stores it in loot/\<implant name>/
- upload \<filename>:
  - Uploads a file to the implant's host
- post-exp:
  - Enters into the BadBird post-exploitation shell
  - Current implemented features:
    - steal-wifi: Grabs all saved Wi-Fi Creds
    - basic-enum: Grabs basic system information
    - schedtasks: Grabs all scheduled tasks
    - killEtw: Sets the `COMPlus_ETWEnabled` environment var to 0 to disable ETW logging
    - wdigest-downgrade: Adds reg entry to force Wdigest credential caching. Wait for a new login then dump LSASS for cleartext creds
    - elevated: Checks for the AlwaysInstalledElevated reg key
    - mimikatz: Grabs Invoke-Mimikatz.ps1 (PowerSploit) from Github and executes it in memory
    - back: Returns to the main BadBird shell
- self-destruct \<hours>:
  - Kills the implant after x hours of last check-in with the C2 Server (default is 1 week)

### Configuration/Misc

- email:
    - Sets the email to be used for token generation. Default is `blah@foobar.com`
    - Entering a real email will result in receiving many emails for each task/result
- exit:
    - Exits the BadBird shell
- help:
    - Prints the help menu
- canary-info:
    - Prints the current canarytoken information (management url, token, etc.)
- PWD:
    - Adds the current working directory to the BadBird shell
- local \<command>:
    - Runs a local command on the c2Server.py host

### Features coming soon

- log:
  - Logs everything to a .txt file stored within the loot dir
- connect:
  - Connects to a listening implant
- canary-endpoint:
  - Sets the canarytoken alerting endpoint to use (currently random from options that canarytokens.org provides)
- token-type:
  - Specifies the type of token to use (currently using web bug/URL token that canarytokens.org provides)
- background:
  - Backgrounds the implant
- sessions:
  - Lists all active sessions


<br>
<p>
  <img src="https://github.com/amartinsec/BadBird/raw/main/Media/badbirdCreateImplant.gif" alt="Gif of BadBird creating and connecting to an implant"/>
</p>


<br>

## Detection 

Currently, all data is transmitted through the useragent (I plan on changing this eventually by adding data in other headers). 
This means that monitoring the user-agent is a good way to identify strange activity. After some quick research of the most common
useragent lengths, I found that the longest of the averages was 162 bytes. Here's a basic Snort rule to detect traffic that 
has a user-agent length greater than 200 bytes (BadBird C2 will always trigger this alert):

```Snort
alert tcp $EXTERNAL_NET any -> $HOME_NET 80 (msg:"Suspicious User-Agent"; flow:to_server,established; content:"User-Agent:"; nocase; content:".{200,}"; nocase; classtype:bad-unknown; sid:10000001; rev:1;)
```

(TODO:) Publish better and more up-to-date detections once tool is more complete

<br>

## Disclaimer 
This is meant for research purposes only. I made this very late at night out of my own curiosity to see if "it could be done". 

Your actions are your own so be responsible. Thinkst is an amazing platform that provides the canarytokens.org platform for free, and I'd recommend researching more if you are unfamiliar.

<br>

## Final Note
As of now, the implant will get flagged by most AV/EDR/XDR/Or whatever its being called nowadays (usually from the keylogger functionality  (HackTool:SH/PythonKeylogger.B --> Defender alert)). I plan on porting the implant to C# but that won't be done until the current project is more stable. If you want to obfuscate, try pyarmor or something...