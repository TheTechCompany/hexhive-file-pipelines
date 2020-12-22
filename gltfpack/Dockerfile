FROM node:14-alpine3.10

RUN apk add alpine-sdk bash python3 py3-pip

RUN npm i -g gltfpack

WORKDIR /gltfpack/worker

ADD worker/package.json .

RUN npm i

ADD worker/index.js .
ADD worker/ipfs.js .

WORKDIR /gltfpack

ADD wait-for-it.sh .

CMD ["./wait-for-it.sh", "${MQ_HOST}:5672", "--", "node", "worker/index.js"] 

