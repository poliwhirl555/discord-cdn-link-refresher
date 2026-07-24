# Discord Media Link Refresher

Discord media links expire after 24 hours when used outside the Discord website or app. This usually isn't a problem as links are automatically refreshed when using the app, but if someone where to archive a chat, either through a archival tool like [Discord Archiver](https://github.com/rroy676/Discord-Archiver/) or through Discord's [Requesting a Copy of Your Data](https://support.discord.com/hc/en-us/articles/360004027692-Requesting-a-Copy-of-your-Data), then the links and thus the media in those chats will either expire quickly or already be expired. 

There are some tools that let you refresh the links, but they work through complicated processes or have you rely on someone else's bot and thus might allow for data capture of your media. They're also in different languages that aren't Python, with a more complicated installation and setup process.

This tool aims to fix that by giving you a Python library and CLI tool that allows you to use your own bot token to refresh links for whatever you need in a easy to install PIP package.

## Installation

## How to get a bot token

1. Login with your Discord account at the [Discord Developer Portal](https://discord.com/developers/applications)

2. Click "New Application", enter some name for that application (the name doesn't matter), and click "Create"

3. In the sidebar, under "Overview", go to the "Bot" tab. You should see a screen with options for changing the Icon and Banner of the Discord Bot.

4. Scroll down the page until you see "Token" section, and click the button "Reset Token"

5. A token, which is a string of random characters, will be generated. Click "Copy" or highlight and copy the token. Save this somewhere safe as it will not be shown again, and it can be misused if found by other people.

6. Use the token in this application. (More instructions below)

## Usage



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