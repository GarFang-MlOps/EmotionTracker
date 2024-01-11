FROM python:3.10
WORKDIR /bot
COPY . /bot
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python setup.py install
RUN chmod 755 .