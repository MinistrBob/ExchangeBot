FROM python:3.11-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV USER_ID=7007
ENV USER_NAME=exchangebot

# Set timezone
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN groupadd -g $USER_ID $USER_NAME \
    && useradd -u $USER_ID -g $USER_ID -m -s /usr/sbin/nologin $USER_NAME

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

USER $USER_ID:$USER_ID

CMD ["python", "main.py"]
