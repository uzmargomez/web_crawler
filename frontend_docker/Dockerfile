FROM python:3.7

WORKDIR /app

ADD . /app
RUN pip install --upgrade pip
RUN python setup.py develop

EXPOSE 5000
CMD ["start-frontend"]
