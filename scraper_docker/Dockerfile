FROM python:3.7

WORKDIR /app

ADD . /app

RUN pip install --upgrade pip
RUN pip install newspaper3k
RUN python setup.py develop

EXPOSE 5000
CMD ["start-scraper"]
