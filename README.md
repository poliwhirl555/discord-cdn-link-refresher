# Discord Media Link Refresher

Discord media links expire after 24 hours when used outside the Discord website or app. This usually isn't a problem as links are automatically refreshed when using the app, but if someone where to archive a chat, either through a archival tool like [Discord Archiver](https://github.com/rroy676/Discord-Archiver/) or through Discord's [Requesting a Copy of Your Data](https://support.discord.com/hc/en-us/articles/360004027692-Requesting-a-Copy-of-your-Data), then the links and thus the media in those chats will either expire quickly or already be expired. 

There are some tools that let you refresh the links, but they work through complicated processes or have you rely on someone else's bot and thus might allow for data capture of your media. They're also in different languages that aren't Python, with a more complicated installation and setup process.

This tool aims to fix that by giving you a Python library and CLI tool that allows you to use your own bot token to refresh links for whatever you need in a easy to install PIP package.

## Installation

### Option 1

1. Download the latest version of Python from [python.org](https://www.python.org/downloads/)

2. Install with the following command
```cmd
python -m pip install discord-cdn-link-refresher
```

3. Get a bot authentication token from Discord. (See instructions below)

### Option 2

1. Go to the Releases section the side of the Github page.

2. Download the latest compiled exe version

3. Get a bot authentication token from Discord. (See instructions below)

## How to get a bot token

1. Login with your Discord account at the [Discord Developer Portal](https://discord.com/developers/applications)

2. Click "New Application", enter some name for that application (the name doesn't matter), and click "Create"

3. In the sidebar, under "Overview", go to the "Bot" tab. You should see a screen with options for changing the Icon and Banner of the Discord Bot.

4. Scroll down the page until you see "Token" section, and click the button "Reset Token"

5. A token, which is a string of random characters, will be generated. Click "Copy" or highlight and copy the token. Save this somewhere safe as it will not be shown again, and it can be misused if found by other people.

6. Use the token in this application. (More instructions below)

## Usage

```cmd
usage: dclr [-h] [-l LINK] [-lf LINK_FILE] [-ht] [-t TOKEN] [-d [DOWNLOAD]] [-v]

options:
  -h, --help            show this help message and exit
  -l, --link LINK       single Discord CDN link to refresh
  -lf, --link-file LINK_FILE
                        a file to refresh and replace the Discord CDN links in
  -ht, --html           used with -lf or --link-file to indicate the argument file is in html and links need to be unescaped. Does nothing otherwise
  -t, --token TOKEN     Discord API authentication token. Defaults to environmental variable \"DISCORD_TOKEN\" if none provided
  -d, --download [DOWNLOAD]
                        download the media of any refreshed links to given directory, or the working directory if not specified
  -v, --verbosity       print refreshed links as they arrive (helps with knowing that the program didn't freeze for large lists)
```

### Examples

#### Refresh a single link
 ```cmd
dclr -l "https://cdn.discordapp.com/attachments/1424247441405771958/1424247677830435007/A_Grim_Hunt-1_.png?ex=6a5a5443&is=6a5902c3&hm=601a5f08f402ef47e2e9c514bc5a427f15a03fe8f2869aad55a920f78ba47b26&" -t "your token here"
 ```

#### Refresh all links in a file
```cmd
dclr -lf "links.txt" -t "your token here"
```
## Notes

If you get tired of entering your token every time, add it to the environmental variables via one of these three ways, depending on your operating system and the program will automatically use it if the token field is blank:

```bash
# Linux - bash/zsh
export DISCORD_TOKEN="your-token-here"
```

```powershell
# Windows - Powershell - Temporary
$env:DISCORD_TOKEN = "your-token-here"

# Windows - Powershell - Permanent
[System.Environment]::SetEnvironmentVariable("DISCORD_TOKEN", "your-token-here", "User")
```

```cmd
# Windows - cmd
set DISCORD_TOKEN=your-token-here
```