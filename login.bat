@echo off
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
del %~dp0\data\SelfBot\self_token.json >nul 2>nul
echo Press Ctrl+Shift+I in your Discord client or on the Discordapp page in your browser.
echo Then go to Application ^> Local Storage ^> http://discordapp.com ^> copy Value of token key
echo Enter your token:
set /p token=
echo { "token": "%token%" } >> %~dp0\data\SelfBot\self_token.json
goto start_bot

:set_password
del %~dp0\data\SelfBot\self_password.json >nul 2>nul
echo Enter your login:
set /p login=
echo Enter your password:
set /p password=
echo { >> %~dp0\data\SelfBot\self_password.json
echo "login": "%login%", >> %~dp0\data\SelfBot\self_password.json
echo "password": "%password%" >> %~dp0\data\SelfBot\self_password.json
echo } >> %~dp0\data\SelfBot\self_password.json
goto start_bot

:start_bot
call run.bat