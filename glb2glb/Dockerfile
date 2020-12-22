FROM nytimes/blender:2.91-cpu-ubuntu18.04

RUN apt-get update && apt-get install -y nodejs npm 

RUN npm i -g n && n 14.0.0 

WORKDIR /glb2glb/worker

ADD worker/package.json .

RUN npm i

ADD worker/index.js .
ADD worker/ipfs.js .

WORKDIR /glb2glb

ADD script.py .

ADD wait-for-it.sh .

CMD ["./wait-for-it.sh", "${MQ_HOST}:5672", "--", "/usr/local/bin/node", "worker/index.js"]
