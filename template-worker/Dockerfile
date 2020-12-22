FROM node:15.4.0-alpine3.10 

RUN apk update && apk add python3 py3-pip

RUN pip3 install pika pymongo

WORKDIR /worker

ADD wait-for-it.sh .
ADD worker.py .

#ADD script.sh .

CMD ["./wait-for-it.sh", "${MQ_URL}", "--", "/usr/bin/python3", "worker.py"]

