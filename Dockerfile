FROM python:3.6

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG_MODE false

RUN apt-get update -y \
    &&  apt-get install netcat -y

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN mkdir /app
WORKDIR /app

COPY . .

COPY ./entrypoint.sh .

ENTRYPOINT ["sh","/app/entrypoint.sh"]
