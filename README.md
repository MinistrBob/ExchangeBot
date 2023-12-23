# ExchangeBot
Telegram bot для Windows Exchange Server, который пересылает новые входящие из папки Входящее сообщения в Telegram.

## Запуск программы

### Запуск без docker

```
cd c:\MyGit\ExchangeBot\
python main.py
```

### Запуск в docker

```
docker run -d --restart=always --name exchangebot -v c:\MyGit\ExchangeBot:/app/settings.py ministrbob/exchangebot:latest
```

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

### Сборка Docker

```shell
cd c:\MyGit\ExchangeBot\
docker build . --cache-from ministrbob/exchangebot:latest --build-arg BUILDKIT_INLINE_CACHE=1 --file Dockerfile --tag ministrbob/exchangebot:latest
docker push ministrbob/exchangebot:latest
```

### Проблемы

#### 1. Проблема подключения к Exchange Server

Ошибка:  
```python
exchangelib.errors.TransportError: HTTPSConnectionPool(host='mail.domain.com', port=443): Max retries exceeded with url: /EWS/Exchange.asmx (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1006)')))
17.12.2023 12:14:17|DEBUG|close| Server mail.domain.com: Closing sessions
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
Решение проблемы: Экспортировать сертификат DOMAIN.COM CA в формате Base64 и добавить его в C:\MyGit\ExchangeBot\venv\Lib\site-packages\certifi\cacert.pem.  

#### 2. Проблема форматирования текста

Exchange отдаёт текст в виде html, но Telegram не может корректно отобразить этот html, некоторые теги вызывают ошибку. Попытка использовать пакет python - sulguk тоже не помогла, т.к. в преобразованном html так же некоторые теги вызывают ошибку.
Поэтому бот работает с `parse_mode=None`, из Exchange берётся `item.text_body` (вместо `item.body`), а само сообщение для Telegram оформлятеся с помощью конструкции `content = Text(...)`.

### Полезная документация

- [exchangelib.items.item](https://ecederstrand.github.io/exchangelib/exchangelib/items/item.html)
- Sent messages are not stored on the Exchange server unless you send it to a recipient located on the same Exchange server or you explicitly choose to save it to e.g. your sent folder.  
- 