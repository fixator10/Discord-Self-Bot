@Echo off
chcp 65001
title Discord Selfbot.py
WHERE python >nul 2>nul
IF %ERRORLEVEL%==0 goto :check_git
ECHO NO PYTHON INSTALLED, ABORTING...
echo Install Python (recommended version is 3.5) https://www.python.org/downloads/

:check_git
WHERE git >nul 2>nul
IF %ERRORLEVEL%==0 goto :check_creds
ECHO NO GIT INSTALLED, ABORTING...
echo Install git https://git-scm.com/download/win
::TEST PURPOSE UNCOMMENT TO SKIP GIT CHECK
::goto :ask_for_input
pause
exit

:check_creds
IF EXIST %~dp0\data\SelfBot\self_token.json goto start_bot

IF EXIST %~dp0\data\SelfBot\self_password.json goto start_bot

:call_login
call login.bat
goto eof

:start_bot
echo "Bot launched. To exit instance press Ctrl+C"
python self_bot.py
echo Something went wrong. Possibly just wrong credentials
echo Press any key to reenter credentials or abort with Ctrl+C and make further investigations
pause
goto :call_login
Exit
