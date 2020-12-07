FROM node:14-alpine3.10

RUN apk add python3 py3-pip bash

RUN npm i -g gltfpack

RUN pip3 install pika pymongo

WORKDIR /gltfpack

ADD worker.py .
ADD wait-for-it.sh .

CMD ["./wait-for-it.sh", "rabbit1:5672", "--", "python3", "worker.py"] 

