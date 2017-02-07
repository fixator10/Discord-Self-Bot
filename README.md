# Discord-Self-Bot
A Discord Self bot to do helpful things

Requires Discord.py

**This version includes code from** [Twentysix26](https://github.com/Twentysix26)/[Red-DiscordBot](https://github.com/Twentysix26/Red-DiscordBot) and [cogs for it](https://twentysix26.github.io/Red-Docs/red_cog_approved_repos/)

#Windows Installation
1. Install [Python](https://www.python.org/downloads/) (recommended version is [3.5](https://www.python.org/downloads/))
	* Check `Add to PATH` - it must be enabled during installation
2. Install [git](https://git-scm.com/download/win)
	* Be sure to select `Run Git from the Windows Command Prompt` on `Adjusting your PATH environment` installation screen
3. [Download copy of bot](https://github.com/fixator10/Discord-Self-Bot/archive/master.zip)
4. Run `check_requirements.bat` or execute `pip install -r requirements.txt` manually
5. Press Ctrl+Shift+I in your Discord client or on the Discordapp page in your browser.
	* Then go to `Local Storage` → http://discordapp.com → copy Value of `token` key
	![Token](http://i.imgur.com/wxuIS8d.png)
6. Create file `self_token.txt` and paste your token **without quotes**
7. Run bot via `run.bat` or `python self_bot.py`