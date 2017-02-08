@Echo off
chcp 65001
title Discord Selfbot.py
WHERE python >nul 2>nul
IF %ERRORLEVEL%==0 goto :check_git
ECHO NO PYTHON INSTALLED, ABORTING...
echo Install Python (recommended version is 3.5) https://www.python.org/downloads/

:check_git
WHERE git >nul 2>nul
IF %ERRORLEVEL%==0 goto :check_req
ECHO NO GIT INSTALLED, ABORTING...
echo Install git https://git-scm.com/download/win
::TEST PURPOSE UNCOMMENT TO SKIP GIT CHECK
::goto :ask_for_input
pause
exit

:check_req
Echo INSTALLING DEPENDENCIES...
call check_requirements.bat >nul

:ask_for_input
echo Enter 1 for token, enter 2 for username and password:
set /p inputVar=
if %inputvar%==1 goto set_token
if %inputvar%==2 goto set_password
echo INVALID INPUT
goto ask_for_input

:set_token
del %~dp0self_password.txt >nul 2>nul
echo Press Ctrl+Shift+I in your Discord client or on the Discordapp page in your browser.
echo Then go to Application ^> Local Storage ^> http://discordapp.com ^> copy Value of token key
echo Enter your token:
set /p token=
echo %token% > %~dp0self_token.txt
goto start_bot

:set_password
del %~dp0self_token.txt >nul 2>nul
echo Enter your login:
set /p login=
echo Enter your password:
set /p password=
echo { > %~dp0self_password.txt
echo "login": "%login%", >> %~dp0self_password.txt
echo "password": "%password%" >> %~dp0self_password.txt
echo } >> %~dp0\self_password.txt
goto start_bot

:start_bot
echo "Bot launched. To exit instance press Ctrl+C"
python self_bot.py
echo Something went wrong. Possibly just wrong credentials
echo Press any key to reenter credentials or abort with Ctrl+C and make further investigations
pause
goto :ask_for_input
Exit
