FROM node:14-alpine3.10

RUN npm i -g gltfpack

RUN pip install pika

WORKDIR /gltfpack

ADD worker.py .
ADD wait-for-it.sh .

CMD ["./wait-for-it.sh", "rabbit1:5679", "--", "python", "worker.py"] 

