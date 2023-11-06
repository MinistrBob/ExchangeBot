# ExchangeBot

## For developer
### Update requirements (on Windows)
```commandline
cd c:\MyGit\ExchangeBot
pip freeze | Out-File -Encoding UTF8 c:\MyGit\ExchangeBot\requirements.txt
```
### Apply requirements
```commandline
c:\MyGit\ExchangeBot\venv\Scripts\activate.bat
cd c:\MyGit\ExchangeBot
python -m pip install -r c:\MyGit\ExchangeBot\requirements.txt
```