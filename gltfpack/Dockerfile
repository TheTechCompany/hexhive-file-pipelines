FROM node:14-buster

RUN apt-get update && apt-get install python3 python3-pip

RUN npm i -g gltfpack

RUN pip3 install pika

WORKDIR /gltfpack

ADD worker.py .
ADD wait-for-it.sh .

CMD ["./wait-for-it.sh", "rabbit1:5679", "--", "python3", "worker.py"] 

