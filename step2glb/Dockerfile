FROM balbatross/occt:latest

RUN apt-get install clang -y 

WORKDIR /step2glb

ADD step_to_gltf.cxx .
ADD make.sh .

RUN ./make.sh


RUN apt-get update && apt-get install nodejs npm -y

RUN npm i -g n && n 14.0.0

WORKDIR /step2glb/worker/

ADD worker/package.json .

RUN npm i

ADD worker/index.js .
ADD worker/ipfs.js .

WORKDIR /step2glb/
ADD wait-for-it.sh .

CMD ["./wait-for-it.sh", "${MQ_HOST}:5672", "--", "/usr/bin/node", "worker"]
#./step_to_gltf -o GA.glb GA.stp
