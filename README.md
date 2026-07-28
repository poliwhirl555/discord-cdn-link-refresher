# Discord Media Link Refresher

Discord CDN media links expire after 24 hours when used outside the Discord website or app. This usually isn't a problem as links are automatically refreshed when using the app, but if someone where to archive a chat, either through an archival tool like [Discord Archiver](https://github.com/rroy676/Discord-Archiver/) or through Discord's [Requesting a Copy of Your Data](https://support.discord.com/hc/en-us/articles/360004027692-Requesting-a-Copy-of-your-Data), then the links and thus the media in those chats will either expire quickly or already be expired. 

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

3. (For file) Copy and paste the exe into the same folder as the file with the links you wish to refresh.

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
  -t, --token TOKEN     Discord API authentication token. Defaults to environmental variable "DISCORD_TOKEN" if none provided
  -d, --download [DOWNLOAD]
                        download the media of any refreshed links to given directory, or the working directory if not specified
  -v, --verbosity       print refreshed links as they arrive (helps with knowing that the program didn't freeze for large lists). -vv to show both the old and the
                        new links at the same time.
```

### Examples

#### Refresh a single link
 ```
dclr -l "https://cdn.discordapp.com/attachments/1424247441405771958/1424247677830435007/A_Grim_Hunt-1_.png?ex=6a5a5443&is=6a5902c3&hm=601a5f08f402ef47e2e9c514bc5a427f15a03fe8f2869aad55a920f78ba47b26&" -t "your token here"
 ```

#### Refresh all links in a file
```cmd
dclr -lf "links.txt" -t "your token here"
```

#### Refresh all links in an HTML file

```
dclr -lf "archive_(349) Test Chat Gif Discord_2026-07-20.html" -ht -t "your token here"
```

#### Refresh and download the contents of a link to a specific folder

```
dclr -lf "archive_(349) Test Chat Gif Discord_2026-07-20.html" -ht -t "your token here" -d "specific-folder"
```

#### Note

If you get tired of entering your token every time, add it to the environmental variables via one of these three ways, depending on your operating system and the program will automatically use it if the token field is blank. (Note: Each of these ways aside from one is temporary. If you restart your terminal, the environmental variable will go away.)

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

## Python Library
```python
import disc_link_refresher

def refresh_cdn_links(expired_links: list[str], auth_token : str = "", download_location : str = "", verbosity : int = 0) -> dict:
    '''
    Uses the Discord API to get new versions of expired CDN links. Returns a dict of format {expired_link \: refreshed_link}.

    :param expired_links: List of expired Discord CDN links
    :type expired_links: list[str]
    :param auth_token: Authentication token for the Discord API. Defaults to environmental variable DISCORD_TOKEN if none provided.
    :type auth_token: str
    :param download_location: if not empty, location to download and save the contents of the refreshed link
    :type download_location: str
    :param verbosity: level of verbosity to print outputs in console when running. 
        Default is 0 meaning no prints, 1 prints the refreshed links as they are acquired, 2 prints both the old links alongside the refreshed links
    :type verbosity: int
    :return: a dict of format {expired_link \: refreshed_link}
    :rtype: dict
    '''

def refresh_cdn_link(expired_link : str, auth_token : str = "", download_location: str = "", verbosity : int = 0) -> str:
    """
    Refresh a single Discord CDN link.
    
    :param expired_link: the expired Discord CDN link
    :type expired_link: str
    :param auth_token: Authentication token for the Discord API. Defaults to environmental variable DISCORD_TOKEN if none provided.
    :type auth_token: str
    :param download_location: if not empty, location to download and save the contents of the refreshed link
    :type download_location: str
    :param verbosity: level of verbosity to print outputs in console when running. 
        Default is 0 meaning no prints, 1 prints the refreshed links as they are acquired, 2 prints both the old links alongside the refreshed links
    :type verbosity: int
    :return: Refreshed, working version of the expired link
    :rtype: str
    """

def refresh_cdn_links_no_old(expired_links: list[str], auth_token : str = "", download_location: str = "", verbosity = 0) -> list[str]:
    """
    Use Discord API to get refreshed cdn links from expired cdn links. Returns only the new links with no association to the old ones.
    
    :param expired_links: List of expired Discord CDN links
    :type expired_links: list[str]
    :param auth_token: Authentication token for the Discord API. Defaults to environmental variable DISCORD_TOKEN if none provided.
    :type auth_token: str
    :param download_location: if not empty, location to download and save the contents of the refreshed links
    :type download_location: str
    :param verbosity: level of verbosity to print outputs in console when running. 
        Default is 0 meaning no prints, 1 prints the refreshed links as they are acquired, 2 prints both the old links alongside the refreshed links
    :type verbosity: int
    :return: A list of the new, refreshed links as strings
    :rtype: list[str]
    """

def refresh_links_in_file(file_path : str, auth_token : str = "", download_location: str = "", is_html : bool = False, verbosity : int = 0):
    """
    Refresh all links in a given file and create a copy of it with all expired links replaced by the new links.
    
    :param file_path: path of file with links to be refreshed
    :type file_path: str
    :param auth_token: Authentication token for the Discord API. Defaults to environmental variable DISCORD_TOKEN if none provided.
    :type auth_token: str
    :param download_location: if not empty, location to download and save the contents of the refreshed links
    :type download_location: str
    :param is_html: indicates to the function whether the file is an html file, to know if unescaping the links is necessary
    :type is_html: bool
    :param verbosity: level of verbosity to print outputs in console when running. 
        Default is 0 meaning no prints, 1 prints the refreshed links as they are acquired, 2 prints both the old links alongside the refreshed links
    :type verbosity: int
    """

def fetch_links_in_file(file_path : str, is_html : bool = False, save_location : str = "") -> list[str]:
    """
    Utility function to find all the Discord cdn links in a given file
    
    :param file_path: path of file to search for links in
    :type file_path: str
    :param is_html: indicates to the function whether the file is an html file, to know if unescaping the links is necessary
    :type is_html: bool
    :param save_location: location to save a file listing all the found links
    :type save_location: str
    :return: a list of the links found in the file as strings
    :rtype: list[str]
    """
```

## Note

For some reason if you've scrolled all the way to the end, and found this package useful for you in some way, please star or watch or say something in Discussions. Not for the clout, but just because it's nice to know for sure that something I spent time on to make was useful to someone out there aside from me.

## Changelog

### V 1.0.0

Initial release.

### V 1.0.1

Added description in toml for PyPi
