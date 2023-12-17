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
### Проблема подключения к Exchange Server
Ошибка:  
```python
exchangelib.errors.TransportError: HTTPSConnectionPool(host='mail.i-teco.ru', port=443): Max retries exceeded with url: /EWS/Exchange.asmx (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1006)')))
17.12.2023 12:14:17|DEBUG|close| Server mail.i-teco.ru: Closing sessions
```
CA сертификаты берутся из пакета C:\MyGit\ExchangeBot\venv\Lib\site-packages\certifi\cacert.pem это можно проверить двумя путями:  
```python
-- 1
from requests.utils import DEFAULT_CA_BUNDLE_PATH
print(DEFAULT_CA_BUNDLE_PATH)

-- 2
import requests
print(requests.certs.where())
```
Решение проблемы: Экспортировать сертификат iTeco CA в формате Base64 и добавить его в C:\MyGit\ExchangeBot\venv\Lib\site-packages\certifi\cacert.pem.  

