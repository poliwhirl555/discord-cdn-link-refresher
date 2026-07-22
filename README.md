Give instructions for how to get bot link

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