@Echo off
title Discord Selfbot.py
echo "Bot launched. To exit instance press Ctrl+C"
chcp 65001
:restart
python self_bot.py
pause
goto restart
Exit
