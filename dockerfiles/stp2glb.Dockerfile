FROM balbatross/occt:latest

RUN apt-get update &&  apt-get install clang -y 

WORKDIR /runner

ADD ./step_to_gltf.cxx .
ADD ./make.sh .

RUN ./make.sh


WORKDIR /runner/

COPY . .

CMD ["npm", "run", "start"]
#./step_to_gltf -o GA.glb GA.stp
