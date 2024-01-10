FROM python:3.10
WORKDIR /bot
RUN pip3 install -r requirements.txt
COPY . .