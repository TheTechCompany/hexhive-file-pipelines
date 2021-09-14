FROM balbatross/occt:latest

RUN apt-get update &&  apt-get install clang -y 

WORKDIR /runner/packages/pipelines/step2glb

ADD ./packages/pipelines/step2glb/step_to_gltf.cxx .
ADD ./packages/pipelines/step2glb/make.sh .

RUN ./make.sh


WORKDIR /runner/

COPY . .

CMD ["npm", "run", "start"]
#./step_to_gltf -o GA.glb GA.stp
