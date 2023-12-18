FROM python:3.11-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV USER_ID=7007
ENV USER_NAME=exchangebot

# Set timezone and datatime format RU
ENV TZ=Europe/Moscow
ENV LANG ru_RU.UTF-8
ENV LANGUAGE ru_RU:ru
ENV LC_ALL ru_RU.UTF-8

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
# Generate and set the Russian locale
RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/* \
    && sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen \
    && locale-gen \
    && update-locale LANG=ru_RU.UTF-8

RUN groupadd -g $USER_ID $USER_NAME \
    && useradd -u $USER_ID -g $USER_ID -m -s /usr/sbin/nologin $USER_NAME

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

USER $USER_ID:$USER_ID

CMD ["python", "main.py"]
