FROM balbatross/occt:latest

RUN apt-get update &&  apt-get install clang -y 

WORKDIR /runner/packages/pipelines/step2glb

ADD ./packages/pipelines/step2glb/step_to_gltf.cxx .
ADD ./packages/pipelines/step2glb/make.sh .

RUN ./make.sh


RUN apt-get update && apt-get install nodejs npm -y

RUN npm i -g n && n 14.0.0

WORKDIR /runner/

ADD package.json .

RUN npm i

COPY packages/shared ./packages/shared
COPY packages/pipelines/step2glb ./packages/pipelines/step2glb

RUN npx lerna bootstrap 

RUN npx lerna run build --scope stp2glb

WORKDIR /runner/packages/pipelines/step2glb

CMD ["yarn", "start:prod"]
#./step_to_gltf -o GA.glb GA.stp
