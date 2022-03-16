FROM python:3.8
WORKDIR /bot

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && pip install --upgrade pip

COPY ./requirements.txt /bot/requirements.txt
RUN pip install -r requirements.txt

COPY . /bot
